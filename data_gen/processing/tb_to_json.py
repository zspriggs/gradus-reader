import xml.etree.ElementTree as ET
from typing import Dict
from processing.grammar import query_grammar
from processing.engine import QueryEngine, AncientTextParser

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

def process_treebank(file: str, lang: str, urn: str, title: str, author: str, prose: bool=True) -> Dict:
    """Parse an XML Dependency Treebank file into json format"""

    root = init_tree(file).getroot()
    query_engine = init_query_engine(file, urn, lang)

    doc = {
        "passage": {
            "title": title,
            "author": author,
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
        for word in sentence.findall('.//word'):
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

            unique_id += 1
            long_id = (sentence.get('id'), word.get('id'))
            head_long_id = (sentence.get('id'), word.get('head'))
            uid_map[long_id] = unique_id
            
            form = word.get('form')
            lemma = word.get('lemma')
            postag = word.get('postag')

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
            
            #TODO: handle enclitics better?

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
    #TODO: refactor so the IDs are handled better !!! EWWW PLS REFACTOR
    for syntax in doc['passage']['syntaxPhrases']:
        syntax['uids'] = [uid_map[(str(long_id[0]), str(long_id[1]))] for long_id in syntax['longIds']]
        del syntax['longIds']
    for section in doc['text']:
        for word in doc['text'][section]:
            head = word.get('head')
            if head:
                if head[1] == '0': #this word is root
                    word['head'] = 0
                else:
                    try:
                        word['head'] = uid_map[head]
                    except:
                        word['head'] = 999
                        #TODO: Figure out if the invisible heads are mistakes or not??

    if not prose:
        doc = chunk_poetry(doc, urn)

    return doc

def chunk_poetry(doc: dict, urn: str, lines_per_chunk: int=30):
    doc_copy = doc.copy()
    doc_copy['text'] = {}

    section_count = 0
    total_count = 1
    section = []

    #assumes section title format is like "urn:cts:latinLit:phi0959.phi006:1.344"
    #print(doc["text"])
    section_start_book = None
    section_start_line = None

    for line in doc['text']:
        book_num = line.split(':')[-1].split('.')[0]
        line_num = line.split(':')[-1].split('.')[-1]

        if not section_start_book or not section_start_line: #first go-around
            section_start_book = book_num
            section_start_line = line_num
            #= f"{book_num}.{line_num}"

        line_text = doc['text'][line]
        #end punch checks line_text[-2] bc line_text[-1] should be linebreak
        end_punc = \
            line_text[-2].get('form')[-1] == '.' or \
            line_text[-2].get('form')[-1] == ';' or \
            line_text[-2].get('form')[-1] == ':'

        new_book = section_start_book != book_num
        skipped_lines = int(line_num) - section_count > int(section_start_line)

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

def handle_gap():
    return



