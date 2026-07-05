"""08 — ChromaDB + RAG: a minimal, runnable reference.

WHY this layer: Chroma runs embedded (same process, SQLite-backed) — no server, no cloud,
fully private. Ideal for personal knowledge bases on this Mac. The embedding step uses
nomic-embed-text via Ollama (local, free, 0.3 GB already installed). Switching to
Pinecone = 3 (swap the Chroma client; the LangChain retriever interface is the same).
See ../compatibility_matrix.md.

NOTE on langchain-community: this package is being sunset in favour of standalone
integration packages (e.g. langchain-ollama). It still works today; the migration path
is: `uv add langchain-ollama` and change the OllamaEmbeddings import.

Three demos:
  1. embed_and_store  — embed 5 docs into an in-memory Chroma collection (no API key)
  2. retrieve         — query the collection, return top-3 chunks (no API key)
  3. rag              — embed → retrieve → Haiku answers (needs ANTHROPIC_API_KEY)

Run:
  uv run python example.py              # all three (step 3 needs Ollama + key)
  uv run python example.py embed_and_store
"""

from __future__ import annotations

import os
import sys

import chromadb
from dotenv import load_dotenv
from langchain_community.embeddings import OllamaEmbeddings  # type: ignore[import-untyped]

load_dotenv()

SMOKE_MODEL = "claude-haiku-4-5-20251001"
OLLAMA_EMBED_MODEL = "nomic-embed-text"
OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")

SAMPLE_DOCS = [
    "LangChain is a framework for building LLM applications.",
    "ChromaDB is a local, embedded vector database written in Python.",
    "RAG stands for Retrieval-Augmented Generation — retrieve relevant chunks, then answer.",
    "nomic-embed-text is a fast, open embedding model that runs on Ollama.",
    "Apple Silicon MLX accelerates local model inference with unified memory.",
]


def _embeddings() -> OllamaEmbeddings:
    return OllamaEmbeddings(model=OLLAMA_EMBED_MODEL, base_url=OLLAMA_BASE_URL)


def demo_embed_and_store() -> chromadb.Collection:
    """Embed SAMPLE_DOCS with nomic-embed-text and store in an in-memory Chroma collection.

    Requires Ollama running at localhost:11434 with nomic-embed-text pulled.
    Returns the collection so demo_retrieve can reuse it.
    """
    client = chromadb.EphemeralClient()
    # get_or_create so this is idempotent within the same process (chromadb 1.5.x
    # shares a Rust-backed store across EphemeralClient instances in one process).
    collection = client.get_or_create_collection("demo_docs")
    if collection.count() == 0:
        emb = _embeddings()
        vectors = emb.embed_documents(SAMPLE_DOCS)
        collection.upsert(
            embeddings=vectors,
            documents=SAMPLE_DOCS,
            ids=[f"doc{i}" for i in range(len(SAMPLE_DOCS))],
        )
    print(f"Stored {len(SAMPLE_DOCS)} docs in Chroma (in-memory).")
    return collection


def demo_retrieve(collection: chromadb.Collection | None = None) -> list[str]:
    """Query the Chroma collection by text and return the top-3 matching chunks.

    No LLM — shows the pure retrieval step.
    """
    if collection is None:
        collection = demo_embed_and_store()

    query = "What is RAG and how does it work?"
    emb = _embeddings()
    query_vector = emb.embed_query(query)

    results = collection.query(query_embeddings=[query_vector], n_results=3)
    chunks = results["documents"][0]
    print(f"Query: {query}")
    for i, chunk in enumerate(chunks, 1):
        print(f"  {i}. {chunk}")
    return chunks


def demo_rag() -> str:
    """Full RAG: embed docs → retrieve → format prompt → Claude Haiku answers.

    Requires both Ollama (nomic-embed-text) and ANTHROPIC_API_KEY.
    """
    from langchain_anthropic import ChatAnthropic
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate

    chunks = demo_retrieve()
    context = "\n".join(f"- {c}" for c in chunks)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer the question using only the context below.\n\nContext:\n{context}",
            ),
            ("human", "{question}"),
        ]
    )
    chain = (
        prompt | ChatAnthropic(model=SMOKE_MODEL, max_tokens=512) | StrOutputParser()
    )
    answer = chain.invoke({"context": context, "question": "What is RAG?"})
    print(f"\nRAG answer: {answer}")
    return answer


DEMOS = {
    "embed_and_store": demo_embed_and_store,
    "retrieve": demo_retrieve,
    "rag": demo_rag,
}


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    if argv:
        name = argv[0]
        if name not in DEMOS:
            print(
                f"Unknown demo '{name}'. Choose from: {', '.join(DEMOS)}",
                file=sys.stderr,
            )
            return 2
        DEMOS[name]()
        return 0

    if not os.getenv("ANTHROPIC_API_KEY"):
        print(
            "Note: ANTHROPIC_API_KEY not set — running embed + retrieve only (skipping rag)."
        )
        demo_embed_and_store()
        demo_retrieve()
        return 0

    for name, fn in DEMOS.items():
        print(f"\n=== {name} ===")
        fn()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
