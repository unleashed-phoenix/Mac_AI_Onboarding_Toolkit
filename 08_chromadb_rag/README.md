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
uv init
uv python pin 3.12
uv add chromadb langchain-community python-dotenv
cp ../.env.example .env
```
Local embeddings: `ollama pull nomic-embed-text` (already installed here).

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
⬜ Scaffold only.
