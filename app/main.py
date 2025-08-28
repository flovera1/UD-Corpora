from fastapi import FastAPI, Query
from pydantic import BaseModel
from pathlib import Path
from typing import List
from .ud_index import UDIndex

app=FastAPI(title='UD Corpora Demo',version='0.1.0')
INDEX=UDIndex(); DATA_DIR=Path(__file__).resolve().parent.parent/'data'

class PatternRequest(BaseModel): pattern:List[str]; limit:int=50

@app.get('/health')
def health(): return {'status':'ok'}

@app.post('/load')
def load_corpus(): INDEX.load_from_dir(DATA_DIR); return {'status':'loaded','stats':INDEX.stats()}

@app.get('/stats')
def stats(): return INDEX.stats()

@app.get('/search/lemma')
def lemma(lemma:str,limit:int=50): return {'matches':INDEX.search_lemma(lemma,limit)}

@app.get('/search/upos')
def upos(upos:str,limit:int=50): return {'matches':INDEX.search_upos(upos,limit)}

@app.get('/search/deprel')
def deprel(deprel:str,limit:int=50): return {'matches':INDEX.search_deprel(deprel,limit)}

@app.post('/search/pattern')
def pattern(req:PatternRequest): return {'matches':INDEX.pos_pattern(req.pattern,req.limit)}
