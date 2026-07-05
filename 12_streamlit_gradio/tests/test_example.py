"""
Tests for 12_streamlit_gradio/example.py (the shared LLM helper).

Streamlit and Gradio UIs cannot be unit-tested with pytest without a headless browser.
We test only the helper functions in example.py that both UI files import.
"""

import os
from unittest.mock import MagicMock

import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")

import example  # noqa: E402

_HAS_KEY = (
    bool(os.getenv("ANTHROPIC_API_KEY"))
    and os.getenv("ANTHROPIC_API_KEY") != "test-key"
)


# ── helpers ───────────────────────────────────────────────────────────────────


def _mock_client(text: str) -> MagicMock:
    content = MagicMock()
    content.text = text
    resp = MagicMock()
    resp.content = [content]
    client = MagicMock()
    client.messages.create.return_value = resp
    return client


def _mock_stream_client(tokens: list[str]) -> MagicMock:
    from contextlib import contextmanager

    @contextmanager
    def fake_stream(*args, **kwargs):
        class FakeStream:
            @property
            def text_stream(self):
                yield from tokens

        yield FakeStream()

    client = MagicMock()
    client.messages.stream = fake_stream
    return client


# ── unit tests ────────────────────────────────────────────────────────────────


def test_chat_once_returns_string():
    client = _mock_client("Paris.")
    result = example.chat_once("What is the capital of France?", client=client)
    assert result == "Paris."
    client.messages.create.assert_called_once()


def test_chat_once_with_history_passes_messages():
    client = _mock_client("It is blue.")
    history = [
        {"role": "user", "content": "What color is the sky?"},
        {"role": "assistant", "content": "The sky can appear many colors."},
    ]
    example.chat_once("Really, what color?", history=history, client=client)
    _, kwargs = client.messages.create.call_args
    msgs = kwargs["messages"]
    assert len(msgs) == 3
    assert msgs[-1]["content"] == "Really, what color?"


def test_chat_once_empty_history():
    client = _mock_client("Hello!")
    result = example.chat_once("Hi", history=[], client=client)
    assert result == "Hello!"


def test_chat_stream_yields_chunks():
    client = _mock_stream_client(["Hello", " world", "!"])
    chunks = list(example.chat_stream("Say hello", client=client))
    assert chunks == ["Hello", " world", "!"]


def test_chat_stream_with_history():
    client = _mock_stream_client(["ok"])
    history = [
        {"role": "user", "content": "prev"},
        {"role": "assistant", "content": "ans"},
    ]
    chunks = list(example.chat_stream("next", history=history, client=client))
    assert chunks == ["ok"]


# ── live (opt-in) ─────────────────────────────────────────────────────────────


@pytest.mark.skipif(not _HAS_KEY, reason="ANTHROPIC_API_KEY not set")
def test_live_chat_once():
    reply = example.chat_once("What is 2 + 2?")
    assert isinstance(reply, str)
    assert len(reply) > 0
