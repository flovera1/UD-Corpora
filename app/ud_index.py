from pathlib import Path
from typing import List, Dict, Any, Iterable
from conllu import parse_incr

class UDIndex:
    def __init__(self):
        self.sentences=[]; self.lemma_index={}; self.upos_index={}; self.deprel_index={}
    def load_from_dir(self, data_dir: Path):
        self.clear()
        for path in sorted(data_dir.glob('*.conllu')):
            with path.open(encoding='utf-8') as f:
                for sent in parse_incr(f):
                    text = sent.metadata.get('text','')
                    tokens=[t for t in sent if isinstance(t.get('id'), int)]
                    idx=len(self.sentences)
                    self.sentences.append({'text':text,'tokens':tokens})
                    for t in tokens:
                        lemma=(t.get('lemma') or '').lower(); upos=(t.get('upostag') or '').upper(); deprel=(t.get('deprel') or '').lower()
                        if lemma: self.lemma_index.setdefault(lemma,[]).append(idx)
                        if upos: self.upos_index.setdefault(upos,[]).append(idx)
                        if deprel: self.deprel_index.setdefault(deprel,[]).append(idx)
    def clear(self):
        self.sentences.clear(); self.lemma_index.clear(); self.upos_index.clear(); self.deprel_index.clear()
    def stats(self):
        return {'num_sentences':len(self.sentences),'num_tokens':sum(len(s['tokens']) for s in self.sentences),'num_lemmas':len(self.lemma_index),'num_upos':len(self.upos_index),'num_deprels':len(self.deprel_index)}
    def search_lemma(self,lemma,limit=50):
        return self._collect(self.lemma_index.get(lemma.lower(),[]),limit)
    def search_upos(self,upos,limit=50):
        return self._collect(self.upos_index.get(upos.upper(),[]),limit)
    def search_deprel(self,deprel,limit=50):
        return self._collect(self.deprel_index.get(deprel.lower(),[]),limit)
    def _collect(self,idxs,limit):
        out=[]; seen=set()
        for i in idxs:
            if i in seen: continue; seen.add(i); s=self.sentences[i]
            out.append({'sent_id':i,'text':s['text'],'tokens':s['tokens']})
            if len(out)>=limit: break
        return out
    def pos_pattern(self,pattern,limit=50):
        pat=[p.upper() for p in pattern]; out=[]
        for i,s in enumerate(self.sentences):
            seq=[(t.get('upostag') or '').upper() for t in s['tokens']]
            if self._contains(seq,pat): out.append({'sent_id':i,'text':s['text'],'upos_seq':seq})
            if len(out)>=limit: break
        return out
    def _contains(self,seq,sub):
        L,l=len(seq),len(sub)
        for i in range(L-l+1):
            if seq[i:i+l]==sub: return True
        return False
