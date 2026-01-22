import xml.etree.ElementTree as ET
from typing import Dict
from engine import QueryEngine
import pandas as pd
import json

# urn_mappings_greek = pd.read_csv('greek_urns.csv', dtype={"URN": str})
# urn_mappings_latin = None

#format: (type, query, clause?)
queries = {
    "grc": {
        ("Dative of possession", "εἰμί > :noun:dative, εἰμί > :pronoun:dative, εἰμί > [relation=SBJ] > :noun:dative, εἰμί > [relation=SBJ] > :pronoun:dative", False),
        ("Relative clause", ":verb[relation=ATR] > ὅς, :verb[relation=ATR] > ὅστις, :verb[relation=ATR] > οἷος, :verb[relation=ATR] > ὅσος", True)
        #conditional clauses
        #genitive absolute
        #accusative infinitive constructions
    },
    "lat": {
        #abl abs
        ("Accusative/Infinitive construction", ":verb:infinitive[relation=OBJ]", True),
        ("Relative clause", ":verb[relation=ATR] > qui1", True)
        #conditional clauses
        #maybe adverbial uses of non adverbs
        #prepositional phrases (might not be as useful)
        #highlight complex tags when applicable (ellipsis)
    }
}

documents = [
    ("../tb_data/tlg0012.tlg001.perseus-grc1.tb.xml", "grc", "0012-001", "Iliad", "Homer"),
    ("../tb_data/v1.0032-002.xml", "grc", "0032-002", "Memorabilia", "Xenophon"),
    ("../tb_data/tlg0016.tlg001.perseus-grc1.1.tb.xml", "grc", "0016-001", "Histories", "Herodotus"),
    ("../tb_data/phi0474.phi013.perseus-lat1.tb.xml", "lat", "0016-001", "In Catilinam I", "Cicero")         
]

def get_annotations(file: str, lang: str, urn: str, title: str, author: str) -> Dict:
    """Parse an XML Dependency Treebank file into a dictionary form"""

    try:
        tree = ET.parse(file)
    except FileNotFoundError:
        print(f"{file} not found. Processing for this document has been stopped.")
        return None
    except ET.ParseError:
        print(f"Failed to parse {file} due to XML error. Aborting")
        return None
    
    root = tree.getroot()

    #Open the data for the query engine
    try:
        with open(file, 'rb') as doc:
            xml_content = doc.read().decode('utf-8')
    except: 
        print(f"Error opening document with urn {urn}.")  
        return None
    
    query_engine = QueryEngine({urn: xml_content}, lang)

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
    current_subdoc = None
    subdoc_words = []
    pending_punc = None

    for sentence in root.findall('.//sentence'):
        if current_subdoc == None: #first pass
            current_subdoc = sentence.get('subdoc')
        elif current_subdoc != sentence.get('subdoc'): #entering new subdoc
            doc['text'][current_subdoc] = subdoc_words
            current_subdoc = sentence.get('subdoc')
            subdoc_words = [] #reset for new subdoc


        for word in sentence.findall('.//word'):
            #    <word id="9201802" form="μῆνιν" lemma="μῆνις" postag="n-s---fa-" head="9201803" relation="OBJ" line="1"/>
            #head and relation might be needed later

            unique_id += 1
            long_id = (sentence.get('id'), word.get('id'))
            uid_map[long_id] = unique_id
            
            form = word.get('form')
            lemma = word.get('lemma')
            postag = word.get('postag')
            insertion = word.get('artificial')

            if insertion:
                continue
            if postag == None or postag == '':
                continue
            if postag[0] == 'u': #if punctuation, append to previous word and move on
                try:
                    subdoc_words[-1]["form"] += form
                except IndexError: #punctuation is first word in subdoc, so we save it for next word
                    pending_punc = form
                continue
            if pending_punc:
                form = pending_punc + form
                pending_punc = None
            if len(postag) < 9:
                postag = postag.ljust(9, '-')
            
            #TODO: handle enclitics better

            postag_names = query_engine.parser.postag_names
            postag_mappings = query_engine.parser.postag_mappings

            morphology = {}
            for feature_name, index in postag_mappings:
                char = postag[index]
                if char != '-':
                    if feature_name == "part_of_speech": #remap for consistent casing
                        morphology["pos"] = postag_names[feature_name].get(char)
                    else: 
                        morphology[feature_name] = postag_names[feature_name].get(char)

            subdoc_words.append({
                "uid": unique_id,
                "form": form,
                "lemma": lemma,
                "postag": postag,
                "morphology": morphology
            })

            
    #remap ids onto each otherr
    #todo: refactor so the IDs are handled better from the beginning
    for syntax in doc['passage']['syntaxPhrases']:
        syntax['uids'] = [uid_map[(str(long_id[0]), str(long_id[1]))] for long_id in syntax['longIds']]
        del syntax['longIds']

    new_filename = file[:-4]
    with open(f"{new_filename}.json", "w") as f:
        json.dump(doc, f, indent=4)
        
    return doc

def query_grammar(query_engine: QueryEngine):
    language = query_engine.parser.lang
    syntax_phrases = []
    syntax_id = 0

    for type, query, is_clause in queries[language]:
        results = query_engine.query(query)
 
        for word in results:
            if is_clause:
                clause = query_engine.get_subtree_and_head(word)
                first_word = clause[0].form
                last_word = clause[-1].form
                
                syntax_phrases.append({
                    "syntax_id": syntax_id,
                    "longIds": [(w.sentence_id, w.id) for w in clause],
                    "type": type,
                    "isClause": is_clause,
                    "firstWord": first_word,
                    "lastWord": last_word
                })
            else:
                first_word = word.form
                syntax_phrases.append({
                    "syntax_id": syntax_id,
                    "longIds": [(word.sentence_id, word.id)],
                    "type": type,
                    "isClause": is_clause,
                    "firstWord": first_word,
                })
            syntax_id+=1
    
    return syntax_phrases
    
def run_preprocessing():
    for doc in documents:
        get_annotations(*doc)
        print(f"Finished processing document {doc[0]}")

run_preprocessing()


#add this in later
#converts urns INCLUDING .xml file extension
    # df = pd.read_csv(csv_path, dtype={"URN": str})
    # urn = urn.split('.')[0]
    # if urn not in df['URN'].values:
    #     return "URN Not Found"
    
    # row = df.loc[df['URN'] == urn].iloc[0]
    # #return f"{row['Author']}, {row['Title']}" 