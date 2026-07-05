"""Tests for example.py (08 — ChromaDB RAG).

Tier 1 — Mocked (no Ollama, no API key):
  - demo_embed_and_store + demo_retrieve: mock OllamaEmbeddings; Chroma runs in-memory.
  - demo_rag: mock both OllamaEmbeddings and ChatAnthropic.invoke.

Tier 2 — Live smoke (opt-in): skips unless ANTHROPIC_API_KEY is set
  (Ollama + nomic-embed-text must also be running for the embed steps).
"""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.messages import AIMessage

import example

FAKE_DIM = 16
FAKE_VECTOR = [0.1] * FAKE_DIM


def _patch_embeddings():
    """Patch OllamaEmbeddings so no Ollama server is needed."""
    mock_emb = MagicMock()
    mock_emb.embed_documents.return_value = [FAKE_VECTOR] * len(example.SAMPLE_DOCS)
    mock_emb.embed_query.return_value = FAKE_VECTOR
    return patch("example._embeddings", return_value=mock_emb)


# ---- Mocked unit tests ---------------------------------------------------------


def test_embed_and_store_mocked():
    with _patch_embeddings():
        collection = example.demo_embed_and_store()
    assert collection is not None
    # Collection may already have docs from a prior test in the same process
    # (chromadb 1.5.x shares a Rust backend); just check it's non-empty.
    assert collection.count() >= len(example.SAMPLE_DOCS)


def test_retrieve_returns_chunks():
    with _patch_embeddings():
        collection = example.demo_embed_and_store()
        chunks = example.demo_retrieve(collection=collection)
    assert isinstance(chunks, list)
    assert len(chunks) == 3


def test_retrieve_chunks_are_strings():
    with _patch_embeddings():
        collection = example.demo_embed_and_store()
        chunks = example.demo_retrieve(collection=collection)
    assert all(isinstance(c, str) for c in chunks)


def test_rag_mocked():
    mock_answer = AIMessage(
        content="RAG retrieves relevant context before generating an answer."
    )
    with _patch_embeddings():
        with patch(
            "langchain_anthropic.ChatAnthropic.invoke", return_value=mock_answer
        ):
            out = example.demo_rag()
    assert "RAG" in out or len(out) > 0


# ---- Live smoke test (opt-in) --------------------------------------------------


@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set; live smoke test skipped (also needs Ollama)",
)
def test_live_rag_smoke():
    out = example.demo_rag()
    assert isinstance(out, str) and out.strip()
