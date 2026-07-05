"""Tests for example.py (03 — OpenAI SDK).

Tier 1 — Mocked (no API key): mock client injected via the demo_x(client=...) param.
Tier 2 — Live smoke (opt-in): skips unless OPENAI_API_KEY is set.
"""

from __future__ import annotations

import json
import os
from unittest.mock import MagicMock

import pytest

import example


def _make_completion(text: str) -> MagicMock:
    msg = MagicMock()
    msg.content = text
    msg.tool_calls = None
    choice = MagicMock()
    choice.finish_reason = "stop"
    choice.message = msg
    resp = MagicMock()
    resp.choices = [choice]
    return resp


def _make_tool_call_completion(tool_name: str, args: dict) -> MagicMock:
    fn = MagicMock()
    fn.name = tool_name
    fn.arguments = json.dumps(args)
    tc = MagicMock()
    tc.id = "call_123"
    tc.function = fn
    msg = MagicMock()
    msg.content = None
    msg.tool_calls = [tc]
    choice = MagicMock()
    choice.finish_reason = "tool_calls"
    choice.message = msg
    resp = MagicMock()
    resp.choices = [choice]
    return resp


# ---- Mocked unit tests ---------------------------------------------------------


def test_get_weather_stub():
    assert "Paris" in example.get_weather("Paris")


def test_demo_basic_mocked():
    client = MagicMock()
    client.chat.completions.create.return_value = _make_completion(
        "OpenAI SDK is the official Python client."
    )
    out = example.demo_basic(client=client)
    assert "OpenAI SDK" in out
    client.chat.completions.create.assert_called_once()


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


def test_demo_tool_use_mocked():
    client = MagicMock()
    first = _make_tool_call_completion("get_weather", {"location": "Paris"})
    final = _make_completion("It is 22C and sunny in Paris.")
    client.chat.completions.create.side_effect = [first, final]

    out = example.demo_tool_use(client=client)
    assert "Paris" in out
    assert client.chat.completions.create.call_count == 2

    second_call_messages = client.chat.completions.create.call_args_list[1].kwargs[
        "messages"
    ]
    tool_result_msg = second_call_messages[-1]
    assert tool_result_msg["role"] == "tool"
    assert tool_result_msg["tool_call_id"] == "call_123"
    assert "Paris" in tool_result_msg["content"]


# ---- Live smoke test (opt-in) --------------------------------------------------


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set; live smoke test skipped",
)
def test_live_basic_smoke():
    out = example.demo_basic()
    assert isinstance(out, str) and out.strip()
