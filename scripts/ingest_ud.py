#!/usr/bin/env python3
import sys; from pathlib import Path; import argparse
sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.ud_index import UDIndex

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--data-dir',default='data')
    ap.add_argument('--stats',action='store_true'); ap.add_argument('--lemma'); ap.add_argument('--upos'); ap.add_argument('--deprel'); ap.add_argument('--pattern',nargs='+'); ap.add_argument('--limit',type=int,default=20)
    a=ap.parse_args(); idx=UDIndex(); idx.load_from_dir(Path(a.data_dir))
    if a.stats: print(idx.stats()); return
    if a.lemma: print(idx.search_lemma(a.lemma,a.limit))
    if a.upos: print(idx.search_upos(a.upos,a.limit))
    if a.deprel: print(idx.search_deprel(a.deprel,a.limit))
    if a.pattern: print(idx.pos_pattern(a.pattern,a.limit))

if __name__=='__main__': main()
