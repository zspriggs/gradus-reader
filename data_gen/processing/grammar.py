from typing import List, Dict
from processing.engine import QueryEngine

QUERIES = {
    "grc": [
        {
            "type": "Dative of possession", 
            "query": "εἰμί > :noun:dative, εἰμί > :pronoun:dative, εἰμί > [relation=SBJ] > :noun:dative, εἰμί > [relation=SBJ] > :pronoun:dative",
            "is_clause": False
        },
        {
            "type": "Relative clause",
            "query": ":verb[relation=ATR] > ὅς, :verb[relation=ATR] > ὅστις, :verb[relation=ATR] > οἷος, :verb[relation=ATR] > ὅσος",
            "is_clause": True
        }

        #conditional clauses
        #genitive absolute
        #accusative infinitive constructions
    ],
    "lat": [
        {
            "type": "Accusative/Infinitive construction", 
            "query": ":verb:infinitive[relation=OBJ]", 
            "is_clause": True
        },
        {
            "type": "Relative clause",
            "query": ":verb[relation=ATR] > qui1",
            "is_clause": True
        }

        #abl abs
        #conditional clauses
        #maybe adverbial uses of non adverbs
        #prepositional phrases (might not be as useful)
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
                    "lastWord": last_word
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