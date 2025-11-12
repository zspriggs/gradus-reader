import xml.etree.ElementTree as ET
from typing import Dict, Optional
import pandas as pd
import json


postag_mappings_latin = {
    #NOTE 'r' is technically "adposition"
    'pos': {
        'n': 'noun', 'v': 'verb', 'a': 'adjective',
        'd': 'adverb', 'c': 'conjunction', 'r': 'preposition',
        'p': 'pronoun', 'm': 'numeral', 'i': 'interjection',
        'e': 'exclamation', 'u': 'punctuation'
    },
    'person': {'1': 'first', '2': 'second', '3': 'third'},
    'number': {'s': 'singular', 'p': 'plural'},
    'tense': {
        'p': 'present', 'i': 'imperfect', 'r': 'perfect', 'l': 'pluperfect',
        't': 'future perfect', 'f': 'future'
    },
    'mood': {
        'i': 'indicative', 's': 'subjunctive', 'n': 'infinitive',
        'm': 'imperative', 'd': 'gerund', 'g': 'gerundive', 'p': 'participle'
    },
    'voice': {'a': 'active', 'p': 'passive', 'd': 'deponent'},
    'gender': {'m': 'masculine', 'f': 'feminine', 'n': 'neuter'},
    'case': {
        'n': 'nominative', 'g': 'genitive', 'd': 'dative', 'a': 'accusative', 
        'b': 'ablative', 'v': 'vocative', 'l': 'locative'
    },
    'degree': {'p': 'positive', 'c': 'comparative', 's': 'superlative'}
}

postag_mappings_greek = {
    'pos': {
        'n': 'noun', 'v': 'verb', 't': 'participle', 'a': 'adjective',
        'd': 'adverb', 'l': 'article', 'g': 'particle', 'c': 'conjunction',
        'r': 'preposition', 'p': 'pronoun', 'm': 'numeral', 'i': 'interjection',
        'e': 'exclamation', 'u': 'punctuation', 'x': 'irregular'
    },
    'person': {'1': 'first', '2': 'second', '3': 'third'},
    'number': {'s': 'singular', 'd': 'dual', 'p': 'plural'},
    'tense': {
        'p': 'present', 'i': 'imperfect', 'r': 'perfect', 'l': 'pluperfect',
        't': 'future perfect', 'f': 'future', 'a': 'aorist'
    },
    'mood': {
        'i': 'indicative', 's': 'subjunctive', 'o': 'optative', 'n': 'infinitive',
        'm': 'imperative', 'd': 'gerund', 'g': 'gerundive'
    },
    'voice': {'a': 'active', 'p': 'passive', 'm': 'middle', 'e': 'mediopassive'},
    'gender': {'m': 'masculine', 'f': 'feminine', 'n': 'neuter'},
    'case': {
        'n': 'nominative', 'g': 'genitive', 'd': 'dative', 'a': 'accusative',
        'v': 'vocative', 'l': 'locative'
    },
    'degree': {'c': 'comparative', 's': 'superlative'}
}

urn_mappings_greek = pd.read_csv('greek_urns.csv', dtype={"URN": str})
urn_mappings_latin = None

def parse_postag(postag: str, lang='Latin') -> Dict[str, Optional[str]]:
    """Parse a Perseus postag string into linguistic features."""
    if len(postag) < 9:
        postag = postag.ljust(9, '-')
    
    features = {}
    mappings = [
        ('pos', 0), ('person', 1), ('number', 2), ('tense', 3),
        ('mood', 4), ('voice', 5), ('gender', 6), ('case', 7), ('degree', 8)
    ]

    postag_mappings={}
    if lang == 'Latin':
        postag_mappings = postag_mappings_latin
    elif lang == 'Greek':
        postag_mappings = postag_mappings_greek
    
    for feature_name, index in mappings:
        char = postag[index]
        if char != '-':
            features[feature_name] = postag_mappings[feature_name].get(char)
        # else:
        #     features[feature_name] = None
    
    return features

#add this in later
#converts urns INCLUDING .xml file extension
    # df = pd.read_csv(csv_path, dtype={"URN": str})
    # urn = urn.split('.')[0]
    # if urn not in df['URN'].values:
    #     return "URN Not Found"
    
    # row = df.loc[df['URN'] == urn].iloc[0]
    # #return f"{row['Author']}, {row['Title']}" 


def get_annotations(file: str) -> Dict:
    """Parse an XML Dependency Treebank file into a dictionary form"""
    try:
        tree = ET.parse(file)
    except:
        print(f"Failed to parse {file}. Aborting")
        return None
    root = tree.getroot()

    doc = {
        "passage": {
            "syntaxPhrases": {

            }
        },
        "text": {

        }
    }
    unique_id = 0
    current_subdoc = None
    subdoc_words = {}

    #get document metadata

    for sentence in root.findall('.//sentence'):
        if current_subdoc == None: #first pass
            current_subdoc = sentence.get('subdoc')
        elif current_subdoc != sentence.get('subdoc'): #entering new subdoc
            doc['text'][current_subdoc] = subdoc_words
            current_subdoc = sentence.get('subdoc')
            subdoc_words = {} #reset for new subdoc

        for word in sentence.findall('.//word'):
            #    <word id="9201802" form="μῆνιν" lemma="μῆνις" postag="n-s---fa-" head="9201803" relation="OBJ" line="1"/>
            #head and relation might be needed later

            unique_id += 1
            form = word.get('form')
            lemma = word.get('lemma')
            postag = word.get('postag')
            # if postag and postag[0] == 'u':
            #     continue

            subdoc_words[unique_id] = {
                "form": form,
                "lemma": lemma,
                "postag": postag
            }

            morphology = {}
            if len(postag) < 9:
                postag = postag.ljust(9, '-')
    
            mappings = [
                ('pos', 0), ('person', 1), ('number', 2), ('tense', 3),
                ('mood', 4), ('voice', 5), ('gender', 6), ('case', 7), ('degree', 8)
            ]
            
            for feature_name, index in mappings:
                char = postag[index]
                if char != '-':
                    morphology[feature_name] = postag_mappings_latin[feature_name].get(char)

            subdoc_words[unique_id]["morphology"] = morphology


    with open(f"{file}.json", "w") as f:
        json.dump(doc, f, indent=4)
        
    return doc

get_annotations("./phi0474.phi013.perseus-lat1.tb.xml")