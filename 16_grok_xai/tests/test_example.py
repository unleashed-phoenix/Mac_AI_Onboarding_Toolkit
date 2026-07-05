"""Tests for 16_grok_xai/example.py — all mocked, no XAI_API_KEY needed."""

import json
import os
from unittest.mock import MagicMock

import pytest

os.environ.setdefault("XAI_API_KEY", "test-key")

import example  # noqa: E402


def _make_chat_response(content: str) -> MagicMock:
    msg = MagicMock()
    msg.content = content
    msg.tool_calls = None
    choice = MagicMock()
    choice.message = msg
    choice.delta = MagicMock()
    choice.delta.content = None
    resp = MagicMock()
    resp.choices = [choice]
    return resp


def test_demo_basic_returns_string():
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _make_chat_response("42")
    result = example.demo_basic(client=mock_client)
    assert result == "42"
    mock_client.chat.completions.create.assert_called_once()


def test_demo_streaming_returns_joined_string():
    from contextlib import contextmanager

    chunk1 = MagicMock()
    chunk1.choices = [MagicMock()]
    chunk1.choices[0].delta.content = "hello "
    chunk2 = MagicMock()
    chunk2.choices = [MagicMock()]
    chunk2.choices[0].delta.content = "world"

    @contextmanager
    def fake_stream(*args, **kwargs):
        yield iter([chunk1, chunk2])

    mock_client = MagicMock()
    mock_client.chat.completions.stream = fake_stream
    result = example.demo_streaming(client=mock_client)
    assert "hello" in result
    assert "world" in result


def test_demo_tool_use_returns_weather_string():
    mock_client = MagicMock()
    tool_call = MagicMock()
    tool_call.function.name = "get_weather"
    tool_call.function.arguments = json.dumps({"location": "San Francisco"})
    msg = MagicMock()
    msg.tool_calls = [tool_call]
    msg.content = None
    resp = MagicMock()
    resp.choices = [MagicMock()]
    resp.choices[0].message = msg
    mock_client.chat.completions.create.return_value = resp

    result = example.demo_tool_use(client=mock_client)
    assert "San Francisco" in result


@pytest.mark.skipif(
    not os.getenv("XAI_API_KEY") or os.getenv("XAI_API_KEY") == "test-key",
    reason="XAI_API_KEY not set",
)
def test_live_basic():
    result = example.demo_basic()
    assert isinstance(result, str)
    assert len(result) > 0
