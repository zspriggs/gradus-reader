import xml.etree.ElementTree as ET
from typing import Dict
from engine import QueryEngine
import pandas as pd
import json

# urn_mappings_greek = pd.read_csv('greek_urns.csv', dtype={"URN": str})
# urn_mappings_latin = None

queries = {
    "grc": {
        "Dative of possession": "εἰμί > :noun:dative, εἰμί > :pronoun:dative, εἰμί > [relation=SBJ] > :noun:dative, εἰμί > [relation=SBJ] > :pronoun:dative"
    },
    "lat": {

    }
}

documents = [
    ("../tb_data/tlg0012.tlg001.perseus-grc1.tb.xml", "grc", "0012-001", "Iliad", "Homer"),
    ("../tb_data/tlg0016.tlg001.perseus-grc1.tb.xml", "grc", "0016-001", "Histories", "Herodotus"),
    ("../tb_data/phi0474.phi013.perseus-lat1.tb.xml", "lat", "0016-001", "In Catilinam I", "Cicero")         
]

def get_annotations(file: str, lang: str, urn: str, title: str, author: str) -> Dict:
    """Parse an XML Dependency Treebank file into a dictionary form"""

    #Parse the tree
    try:
        tree = ET.parse(file)
    except:
        print(f"Failed to parse {file}. Aborting")
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
    current_subdoc = None
    subdoc_words = []

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
            long_id = word.id
            form = word.get('form')
            lemma = word.get('lemma')
            postag = word.get('postag')

            if postag == None:
                continue
            if postag[0] == 'u': #if punctuation, append to previous word and move on
                subdoc_words[-1]["form"] += form
                continue
            if len(postag) < 9:
                postag = postag.ljust(9, '-')
            
            #TODO: handle enclitics better

            postag_names = query_engine.parser.postag_names
            postag_mappings = query_engine.parser.postag_mappings

            morphology = {}
            for feature_name, index in postag_mappings:
                char = postag[index]
                if char != '-':
                    morphology[feature_name] = postag_names[feature_name].get(char)

            subdoc_words.append({
                "uid": unique_id,
                "long_id": long_id,
                "form": form,
                "lemma": lemma,
                "postag": postag,
                "morphology": morphology
            })

    new_filename = file[:-7]
    with open(f"./TESTER_{new_filename}.json", "w") as f:
        json.dump(doc, f, indent=4)
        
    return doc

def query_grammar(query_engine: QueryEngine):
    language = QueryEngine.parser.lang
    syntax_phrases = []

    for type, query in queries[language]:
        results = query_engine.query(query)
 
        for word in results:
            start_id = word.id
            syntax_phrases.append({
                "long_id": start_id,
                "type": type
            })
    
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