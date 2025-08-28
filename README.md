# UD Corpora Demo — Syntactic & Semantic Querying (FastAPI)

This demo parses Universal Dependencies (UD) corpora (CoNLL-U), provides syntactic queries (lemma, UPOS, deprel), pattern queries, and optional semantic embeddings. It serves as a minimal research-oriented infrastructure example.
# UD-Corpora

## 1) Requirements

Python 3.9+

(Optional) transformers + torch are listed in requirements.txt. If you don’t want embeddings, comment out those two lines before installing to speed things up.

## 2) Get the code
if you downloaded the ZIP
`unzip ud-corpora-demo.zip
cd ud-corpora-demo`

 or if you cloned the repo
`git clone <your-repo-url>.git
cd ud-corpora-demo`

## 3) Create a virtual environment & install deps
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows (PowerShell):
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt


Tip: To skip heavy installs, open requirements.txt and comment out:

transformers>=4.41.0
torch>=2.2.0

## 4) Run the API
`uvicorn app.main:app --reload`


Open the interactive docs at: http://127.0.0.1:8000/docs

## 5) Load the sample corpus

With the server running, either:

In Swagger UI → click POST /load → Try it out → Execute, or

Use curl:

`curl -X POST http://127.0.0.1:8000/load`


You should see stats from the included data/sample.conllu.

## 6) Try basic endpoints

Stats

`curl http://127.0.0.1:8000/stats`


Search by lemma

`curl "http://127.0.0.1:8000/search/lemma?lemma=dog"`


Search by UPOS

`curl "http://127.0.0.1:8000/search/upos?upos=NOUN"`


Search by dependency relation

`curl "http://127.0.0.1:8000/search/deprel?deprel=nsubj"`


POS pattern search (contiguous POS sequence within a sentence)

`curl -X POST http://127.0.0.1:8000/search/pattern \
  -H "Content-Type: application/json" \
  -d '{"pattern":["DET","ADJ","NOUN"], "limit": 5}'`


You can also run these directly in Swagger UI.

## 7) Add your own UD corpora

Download a UD treebank (e.g., UD English or UD Dutch) from https://universaldependencies.org/

Place .conllu files under the project’s data/ folder

Call POST /load again to re-index

## 8) Use the CLI (optional)
`python scripts/ingest_ud.py --stats
python scripts/ingest_ud.py --lemma dog
python scripts/ingest_ud.py --upos NOUN
python scripts/ingest_ud.py --deprel nsubj
python scripts/ingest_ud.py --pattern DET ADJ NOUN`

## 9) Troubleshooting

uvicorn: command not found → pip install uvicorn (or ensure venv is activated).

ModuleNotFoundError: conllu → pip install -r requirements.txt again.

Heavy install → comment out transformers/torch in requirements.txt (embeddings are optional in this demo).