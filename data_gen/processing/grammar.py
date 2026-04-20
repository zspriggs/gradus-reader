from typing import List, Dict
from processing.engine import QueryEngine

#TODO: add grammar paragraphs to queries
QUERIES = {
    "grc": [
        {
            "type": "Dative of possession", 
            "query": "εἰμί > :noun:dative, εἰμί > :pronoun:dative, εἰμί > [relation=SBJ] > :noun:dative, εἰμί > [relation=SBJ] > :pronoun:dative",
            "is_clause": False,
            "grammar_ref": "§DatPos"
        },
        {
            "type": "Relative clause",
            "query": ":verb[relation=ATR]:has_child(ὅς), "
            ":verb[relation=ATR]:has_child(ὅστις), "
            ":verb[relation=ATR]:has_child(οἷος), "
            ":verb[relation=ATR]:has_child(ὅσος)",
            "is_clause": True,
            "grammar_ref": ""
        },
        {
            "type": "Genitive absolute",
            "query": ":genitive[relation=SBJ]",
            "is_clause": True,
            "grammar_ref": "§PartGen"
        },
        {
            "type": "Indirect discourse",
            "query": ":verb:infinitive[relation=OBJ], :verb:infinitive[relation=SBJ]",
            "is_clause": True,
            "grammar_ref": ""
        },
        {
            "type": "Conditional clause",
            "query": "εἰ[relation=AuxC] > :verb[relation=ADV], ἐάν[relation=AuxC] > :verb[relation=ADV]",
            "is_clause": True
        }
        #prepositional phrases
    ],
    "lat": [
        {
            "type": "Indirect discourse", 
            "query": ":verb:infinitive[relation=OBJ]", #need to add sbj?
            "is_clause": True
        },
        {
            "type": "Relative clause",
            "query": ":verb[relation=ATR]:has_child(qui)",
            "is_clause": True
        },
        {
            "type": "Ablative absolute",
            "query": ":ablative[relation=ADV] > :ablative[relation=SBJ]",
            "is_clause": True
        },
        {
            "type": "Conditional clause",
            "query": "si[relation=AuxC] > :verb[relation=ADV]",
            "is_clause": True
        },
        {
            "type": "Conditional clause",
            "query": "nisi[relation=AuxC] > :verb[relation=ADV]",
            "is_clause": True
        }
        #maybe adverbial uses of non adverbs
        #prepositional phrases
        #highlight complex tags when applicable (ellipsis)
    ]
}

def query_grammar(query_engine: QueryEngine, custom_queries: List[Dict] = [], use_defaults: bool = True):
    language = query_engine.parser.lang
    queries = []

    if use_defaults: 
        queries = QUERIES[language]
    if custom_queries:
        queries.extend(custom_queries)

    syntax_phrases = []
    syntax_id = 0

    for query in queries:
        results = query_engine.query(query["query"])

        for word in results:
            if query["is_clause"]:
                clause = query_engine.get_subtree_and_head(word)
                first_word = clause[0].form
                last_word = clause[-1].form
                
                syntax_phrases.append({
                    "syntax_id": syntax_id,
                    "longIds": [(w.sentence_id, w.id) for w in clause],
                    "type": query["type"],
                    "isClause": query["is_clause"],
                    "firstWord": first_word,
                    "lastWord": last_word,
                    "grammar_ref": query.get("grammar_ref", "")
                })
            else:
                first_word = word.form
                syntax_phrases.append({
                    "syntax_id": syntax_id,
                    "longIds": [(word.sentence_id, word.id)],
                    "type": query["type"],
                    "isClause": query["is_clause"],
                    "firstWord": first_word,
                })
            syntax_id += 1
    
    return syntax_phrases