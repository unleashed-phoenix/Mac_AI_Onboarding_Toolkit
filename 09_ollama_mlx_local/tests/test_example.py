"""Tests for example.py (09 — Ollama MLX Local).

Tier 1 — Mocked (no Ollama needed): inject mock OpenAI client via demo_x(client=...).
Tier 2 — Live smoke (opt-in): skips unless Ollama is running at localhost:11434.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

import example


def _make_chat_completion(text: str) -> MagicMock:
    msg = MagicMock()
    msg.content = text
    choice = MagicMock()
    choice.message = msg
    resp = MagicMock()
    resp.choices = [choice]
    return resp


def _make_embedding_response(dim: int = 768) -> MagicMock:
    data = MagicMock()
    data.embedding = [0.01] * dim
    resp = MagicMock()
    resp.data = [data]
    return resp


# ---- Mocked unit tests ---------------------------------------------------------


def test_ollama_running_helper_returns_bool():
    result = example._ollama_running()
    assert isinstance(result, bool)


def test_demo_basic_mocked():
    client = MagicMock()
    client.chat.completions.create.return_value = _make_chat_completion(
        "Ollama runs open-source models locally."
    )
    out = example.demo_basic(client=client)
    assert "Ollama" in out or len(out) > 0
    call_model = client.chat.completions.create.call_args.kwargs["model"]
    assert call_model == example.CHAT_MODEL


def test_demo_streaming_mocked():
    client = MagicMock()
    chunks = []
    for text in ["1\n", "2\n", "3\n", "4\n", "5\n"]:
        chunk = MagicMock()
        chunk.choices[0].delta.content = text
        chunks.append(chunk)

    stream_ctx = MagicMock()
    stream_ctx.__enter__.return_value = iter(chunks)
    stream_ctx.__exit__.return_value = False
    client.chat.completions.stream.return_value = stream_ctx

    out = example.demo_streaming(client=client)
    assert "3" in out


def test_demo_embeddings_mocked():
    client = MagicMock()
    client.embeddings.create.return_value = _make_embedding_response(dim=768)
    vec = example.demo_embeddings(client=client)
    assert isinstance(vec, list)
    assert len(vec) == 768
    call_model = client.embeddings.create.call_args.kwargs["model"]
    assert call_model == example.EMBED_MODEL


# ---- Live smoke test (opt-in) --------------------------------------------------


@pytest.mark.skipif(
    not example._ollama_running(),
    reason="Ollama not running at localhost:11434; live smoke test skipped",
)
def test_live_basic_smoke():
    out = example.demo_basic()
    assert isinstance(out, str) and out.strip()
