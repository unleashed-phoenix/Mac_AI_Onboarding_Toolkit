"""Tests for 18_qwen_local/example.py — mocked by default, live skips without Ollama."""

from unittest.mock import MagicMock, patch

import pytest

import example


# ── helpers ───────────────────────────────────────────────────────────────────


def _mock_chat_response(content: str) -> MagicMock:
    msg = MagicMock()
    msg.content = content
    resp = MagicMock()
    resp.message = msg
    return resp


def _make_stream_chunks(tokens: list[str]) -> list[MagicMock]:
    chunks = []
    for t in tokens:
        msg = MagicMock()
        msg.content = t
        chunk = MagicMock()
        chunk.message = msg
        chunks.append(chunk)
    return chunks


# ── unit tests ────────────────────────────────────────────────────────────────


def test_demo_basic_returns_code_string():
    client = MagicMock()
    client.chat.return_value = _mock_chat_response("s[::-1]")
    result = example.demo_basic(client=client)
    assert result == "s[::-1]"
    client.chat.assert_called_once()


def test_demo_streaming_joins_chunks():
    chunks = _make_stream_chunks(["List ", "comprehensions ", "are..."])
    client = MagicMock()
    client.chat.return_value = iter(chunks)
    result = example.demo_streaming(client=client)
    assert result == "List comprehensions are..."


def test_demo_embeddings_returns_float_list():
    mock_embed = MagicMock()
    mock_embed.embeddings = [[0.1, 0.2, 0.3]]
    client = MagicMock()
    client.embed.return_value = mock_embed
    result = example.demo_embeddings(client=client)
    assert result == [0.1, 0.2, 0.3]
    client.embed.assert_called_once()


def test_ollama_running_returns_bool():
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.return_value = MagicMock()
        assert example._ollama_running() is True

    import urllib.error

    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("refused")):
        assert example._ollama_running() is False


# ── live smoke (skipped without Ollama) ───────────────────────────────────────


@pytest.mark.skipif(not example._ollama_running(), reason="Ollama not running")
def test_live_basic():
    result = example.demo_basic()
    assert isinstance(result, str)
    assert len(result) > 0
