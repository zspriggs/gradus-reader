import xml.etree.ElementTree as ET
from typing import Dict
from processing.grammar import query_grammar
from processing.engine import QueryEngine, AncientTextParser

# documents = [
#     ("../tb_data/tlg0012.tlg001.perseus-grc1.tb.xml", "./temp_data/iliad.json", "grc", "0012-001", "Iliad", "Homer"),
#     ("../tb_data/v1.0032-002.xml", "./temp_data/memorabilia.json", "grc", "0032-002", "Memorabilia", "Xenophon"),
#     ("../tb_data/tlg0016.tlg001.perseus-grc1.1.tb.xml", "./temp_data/histories.json", "grc", "0016-001", "Histories", "Herodotus"),
#     ("../tb_data/phi0474.phi013.perseus-lat1.tb.xml", "./temp_data/incatilinam.json", "lat", "0016-001", "In Catilinam I", "Cicero")         
# ]

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
                section_key = word.get('cite')

            if current_section == None: #first pass
                current_section = section_key
            elif current_section != section_key:
                doc['text'][current_section] = section_words
                current_section = section_key
                section_words = []

            unique_id += 1
            long_id = (sentence.get('id'), word.get('id'))
            uid_map[long_id] = unique_id
            
            form = word.get('form')
            lemma = word.get('lemma')
            postag = word.get('postag')

            if word.get('artificial') or word.get('insertion_id'): #If this word is an insertion, ignore
                continue
            if postag == None or postag == '': #If this word does not have a postag, ignore
                continue
            if postag[0] == 'u': #if this word is punctuation, append to previous word and continue
                try:
                    section_words[-1]["form"] += form
                except IndexError: #punctuation is first word in subdoc, so we save it for next word
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
                "morphology": morphology
            })

    doc['text'][current_section] = section_words

    #remap ids onto each otherr
    #TODO: refactor so the IDs are handled better from the beginning ? 
    for syntax in doc['passage']['syntaxPhrases']:
        syntax['uids'] = [uid_map[(str(long_id[0]), str(long_id[1]))] for long_id in syntax['longIds']]
        del syntax['longIds']
        
    return doc

