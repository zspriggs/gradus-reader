import xml.etree.ElementTree as ET
from typing import Dict, Optional
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

def parse_postag(postag: str) -> Dict[str, Optional[str]]:
    """Parse a Perseus postag string into linguistic features."""
    if len(postag) < 9:
        postag = postag.ljust(9, '-')
    
    features = {}
    mappings = [
        ('pos', 0), ('person', 1), ('number', 2), ('tense', 3),
        ('mood', 4), ('voice', 5), ('gender', 6), ('case', 7), ('degree', 8)
    ]
    
    for feature_name, index in mappings:
        char = postag[index]
        if char != '-':
            features[feature_name] = postag_mappings_latin[feature_name].get(char)
        # else:
        #     features[feature_name] = None
    
    return features

def get_annotations(file: str) -> Dict:
    """Parse an XML Dependency Treebank file into a dictionary form"""
    try:
        tree = ET.parse(file)
    except:
        print(f"Failed to parse {file}. Aborting")
        return None
    root = tree.getroot()

    doc = {}

    for sentence in root.findall('.//sentence'):
        sentence_id = sentence.get('id') #subdoc may be needed later
        words = {}
        for word in sentence.findall('.//word'):
            #    <word id="9201802" form="μῆνιν" lemma="μῆνις" postag="n-s---fa-" head="9201803" relation="OBJ" line="1"/>
            #head and relation might be needed later

            id = word.get('id')
            form = word.get('form')
            lemma = word.get('lemma')
            postag = word.get('postag')
            # if postag and postag[0] == 'u':
            #     continue

            #tags = parse_postag(postag)

            words[id] = {
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

            words[id]["morphology"] = morphology

        doc[sentence_id] = words

    with open(f"{file}.json", "w") as f:
        json.dump(doc, f, indent=4)
        
    return doc

get_annotations("./phi0474.phi013.perseus-lat1.tb.xml")