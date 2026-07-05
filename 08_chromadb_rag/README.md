# 08 — ChromaDB + RAG

## What it is
A local, embedded vector database plus a retrieval-augmented-generation pattern: embed
your docs, store vectors, retrieve relevant chunks, feed them to an LLM.

## WHY reach for it
- Runs fully local — no server, no cloud, private by default.
- Perfect on this Mac: use `nomic-embed-text` via Ollama for free local embeddings.
- Simple API; great for personal knowledge bases.

## WHEN NOT to
- Massive scale / multi-tenant → hosted vector DB (Pinecone, Weaviate).
- LlamaIndex (`Phase 9`) if you want a retrieval-first framework.

## Install
```
cd 08_chromadb_rag
uv init --python 3.12
uv add chromadb langchain-community langchain-anthropic python-dotenv
uv add --dev pytest
cp ../.env.example .env
```
Local embeddings: `ollama pull nomic-embed-text` (already installed on this Mac).
`ANTHROPIC_API_KEY` only needed for the final RAG step; embed + retrieve run without it.
Note: `langchain-community` is being sunset — migration path is `uv add langchain-ollama`.

## Run
```
uv run python example.py              # all demos (steps 1–2 need Ollama; step 3 + key)
uv run python example.py embed_and_store   # or: retrieve | rag
uv run pytest                         # mocked tests (no Ollama, no key needed)
```
`example.py` shows: (1) embed 5 docs with nomic-embed-text into Chroma, (2) query
by text → top-3 chunks, (3) full RAG — retrieve → Claude Haiku answers.

## 24 GB RAM note
Keep the `chroma_db/` folder out of git (already in `.gitignore`). Local embedding model
adds ~0.3 GB — negligible alongside a 9–17 GB chat model.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| LanceDB / Qdrant local | More features | 2 |
| Pinecone (cloud) | Scale, not private | 3 |

## Mac vs Windows
No difference; Chroma is pure Python + SQLite.

## Status
✅ Deep-dive complete — `example.py` (embed + retrieve + RAG) and `tests/` (4 mocked,
1 opt-in live) on Python 3.12. Mocked tests need neither Ollama nor an API key.
