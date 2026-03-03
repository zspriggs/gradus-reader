import xml.etree.ElementTree as ET
from typing import Dict
from processing.grammar import query_grammar
from processing.engine import QueryEngine, AncientTextParser

"""Create exception for docs without poetry line nums"""
class LineNumberError(Exception):
    pass

def init_query_engine(file, urn: str, lang: str) -> QueryEngine:
    """ Opens the XML data for the query engine and initializes a new query engine. """
    #Open the data for the query engine
    try:
        with open(file, 'rb') as doc:
            xml_content = doc.read().decode('utf-8')
    except: 
        print(f"Error opening document with urn {urn}.")  
        return None
    
    return QueryEngine({urn: xml_content}, lang)

def init_tree(file) -> ET:
    """ Opens the XML data for as a tree and returns the tree """
    try:
        tree = ET.parse(file)
    except FileNotFoundError:
        print(f"{file} not found. Processing for this document has been stopped.")
        return None
    except ET.ParseError:
        print(f"Failed to parse {file} due to XML error. Aborting")
        return None

    return tree
 
def map_morphology(postag: str, parser: AncientTextParser) -> Dict:
    """Maps part of speech tags to human readable format """
    postag_names = parser.postag_names
    postag_mappings = parser.postag_mappings

    morphology = {}
    for feature_name, index in postag_mappings:
        char = postag[index]
        if char != '-':
            if feature_name == "part_of_speech": #remap for consistent casing
                morphology["pos"] = postag_names[feature_name].get(char)
            else: 
                morphology[feature_name] = postag_names[feature_name].get(char)
    
    return morphology

def process_treebank(file: str, lang: str, urn: str, title: str, author: str, source: str, prose: bool=True) -> Dict:
    """Parse an XML Dependency Treebank file into json format"""

    root = init_tree(file).getroot()
    query_engine = init_query_engine(file, urn, lang)

    doc = {
        "passage": {
            "title": title,
            "author": author,
            "urn": urn,
            "source": source,
            "syntaxPhrases": query_grammar(query_engine)
        },
        "text": {

        }
    }

    unique_id = 0
    uid_map = {}
    current_section = None
    section_words = []
    pending_punc = None
    
    for sentence in root.findall('.//sentence'):
        words = sorted(sentence.findall('.//word'), key=lambda w: int(w.get('id')))
        words = reorder_enclitics(words)

        for word in words:
            if prose:
                section_key = sentence.get('subdoc')
            else:
                section_key = word.get('cite', current_section)
                if section_key=="": #sometimes cite="", sometimes cite doesn't exist
                    section_key = current_section

            if current_section == None: #first pass
                current_section = section_key
            elif current_section != section_key:
                if not prose:
                    unique_id += 1
                    section_words.append({"uid": unique_id, "linebreak": True})
                doc['text'][current_section] = section_words
                current_section = section_key
                section_words = []

            #NOTE: Skipped words *are* assigned a uid, for ease of syntax re-mapping and 
            #for dependency parsing applications that will later be implemented
            unique_id += 1
            long_id = (sentence.get('id'), word.get('id'))
            head_long_id = (sentence.get('id'), word.get('head'))
            uid_map[long_id] = unique_id
            
            form = word.get('form')
            lemma = word.get('lemma')
            postag = word.get('postag')

            #skip conditions
            if word.get('artificial') or word.get('insertion_id'): #If this word is an insertion, ignore
                continue
            if postag == None or postag == '': #If this word does not have a postag, ignore
                continue
            if postag[0] == 'u': #if this word is punctuation, append to previous word and continue
                if form == '(' or form == '\'' or form == '\"': #some punc appends to NEXT word
                    pending_punc = form
                else:
                    try:
                        section_words[-1]["form"] += form
                    except IndexError: #punctuation is first word in subdoc, appends to next word
                        pending_punc = form
                continue
            if pending_punc:
                form = pending_punc + form
                pending_punc = None

            if len(postag) < 9:
                postag = postag.ljust(9, '-')
            
            #TODO: handle enclitics better

            morphology = map_morphology(postag, query_engine.parser)

            section_words.append({
                "uid": unique_id,
                "form": form,
                "lemma": lemma,
                "postag": postag,
                "head": head_long_id,
                "morphology": morphology
            })

    doc['text'][current_section] = section_words

    #remap ids onto each otherr
    #TODO: refactor so the IDs are handled better?
    for syntax in doc['passage']['syntaxPhrases']:
        syntax['uids'] = [uid_map[(str(long_id[0]), str(long_id[1]))] for long_id in syntax['longIds']]
        del syntax['longIds']

    # TODO: Continue on dependency implementation
    # for section in doc['text']:
    #     for word in doc['text'][section]:
    #         head = word.get('head')
    #         if head:
    #             if head[1] == '0': #this word is root
    #                 word['head'] = 0
    #             else:
    #                 word['head'] = uid_map[head]

    if not prose:
        doc = chunk_poetry(doc, urn)

    return doc

def reorder_enclitics(words):
    """Reorders words to handle cases when Latin enclitics are treebanked before the word they actually append to"""
    #check for que bc usually (or maybe always) form is -que when enclitic is properly ordered
    word_list = list(words)
    just_reordered = False
    for i, word in enumerate(word_list):
        if just_reordered: 
            just_reordered = False
            continue
        if word.get('form') in {'que', 've', 'c'} and i + 1 < len(word_list):
            word_list[i], word_list[i+1] = word_list[i+1], word_list[i]
            just_reordered = True
    return word_list

def chunk_poetry(doc: dict, urn: str, lines_per_chunk: int=30):
    """Chunks poetry into groups of at least lines_per_chunk lines, always ending on a sentence break"""
    doc_copy = doc.copy()
    doc_copy['text'] = {}

    section_count = 0
    section = []

    #assumes section title format is like "urn:cts:latinLit:phi0959.phi006:1.344"
    section_start_book = None
    section_start_line = None

    for line in doc['text']:
        if not line:
            #If line is None type, this means this is poetry but without a "cite" element with line nums
            #so we do not process the document due to inability to recover lines
            raise LineNumberError(f"Document does not appear to have line numbers -- cannot recover line positions")
        
        book_num, line_num = split_cite_urn(line)

        if not section_start_book or not section_start_line: #first go-around
            section_start_book = book_num
            section_start_line = line_num

        line_text = doc['text'][line]

        #end punc checks line_text[-2] bc line_text[-1] should be linebreak
        end_punc = \
            line_text[-2].get('form')[-1] == '.' or \
            line_text[-2].get('form')[-1] == ';' or \
            line_text[-2].get('form')[-1] == ':'

        new_book = section_start_book != book_num
        try:
            skipped_lines = int(line_num) - section_count > int(section_start_line)
        except ValueError:
            skipped_lines = False #if we can't derive an int from the start_line or line_num, just trust the treebank

        if (section_count >= lines_per_chunk and end_punc) or new_book or skipped_lines:
            section_start = f"{section_start_book}.{section_start_line}"

            section_end = f"{section_start_book}.{int(section_start_line)+section_count-2}"

            section_title = f"{section_start}-{section_end}"
            doc_copy['text'][section_title] = section

            #reset to current line
            section = []
            section_count = 0
            section_start_book = book_num
            section_start_line = line_num

        section.extend(line_text)
        section_count += 1

    return doc_copy

def split_cite_urn(urn: str):
    passage = urn.split(':')[-1]  # "1.344" or "344"
    parts = passage.split('.')
    
    if len(parts) == 2:
        return parts[0], parts[1]  # book_num, line_num
    elif len(parts) == 1:
        return None, parts[0]      # no book, just line_num
    elif len(parts) == 3: # sometimes we see something like 1.929.1 when there's insertions
        return parts[0], f"{parts[1]}.{parts[2]}"
    else:
        #sometimes there's a cite with a line/book, followed by a cite without
        chunks = urn.split(' ')
        if len(chunks) > 1:
            return split_cite_urn(chunks[0])
        else:
            return None, None


