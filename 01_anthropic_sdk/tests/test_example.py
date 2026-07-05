"""Tests for example.py.

Two tiers:
  * Mocked unit tests — no API key, no network. These run in pre-commit / CI and
    verify the call shape (including the tool-use round-trip).
  * Live smoke test — opt-in. Skips unless ANTHROPIC_API_KEY is set, so it never
    burns quota or blocks a commit unexpectedly.
"""

from __future__ import annotations

import os
from unittest.mock import MagicMock

import pytest

import example


def _text_block(text: str) -> MagicMock:
    block = MagicMock()
    block.type = "text"
    block.text = text
    return block


def _tool_use_block(id_: str, name: str, tool_input: dict) -> MagicMock:
    block = MagicMock()
    block.type = "tool_use"
    block.id = id_
    block.name = name
    block.input = tool_input
    return block


# ---- Mocked unit tests ---------------------------------------------------------


def test_get_weather_stub():
    assert "Paris" in example.get_weather("Paris")


def test_demo_basic_mocked():
    client = MagicMock()
    message = MagicMock()
    message.content = [
        _text_block("The Anthropic SDK is a Python client for the Claude API.")
    ]
    client.messages.create.return_value = message

    out = example.demo_basic(client=client)

    assert "Anthropic SDK" in out
    client.messages.create.assert_called_once()


def test_demo_streaming_mocked():
    client = MagicMock()
    stream = MagicMock()
    stream.text_stream = iter(["1\n", "2\n", "3\n", "4\n", "5\n"])
    final = MagicMock()
    final.content = [_text_block("1\n2\n3\n4\n5\n")]
    stream.get_final_message.return_value = final
    # `with client.messages.stream(...) as stream:` -> __enter__ returns our mock
    client.messages.stream.return_value.__enter__.return_value = stream

    out = example.demo_streaming(client=client)

    assert out.count("\n") == 5
    assert "3" in out


def test_demo_tool_use_mocked():
    client = MagicMock()

    first = MagicMock()
    first.stop_reason = "tool_use"
    first.content = [_tool_use_block("toolu_1", "get_weather", {"location": "Paris"})]

    final = MagicMock()
    final.stop_reason = "end_turn"
    final.content = [_text_block("It is 22C and sunny in Paris.")]

    client.messages.create.side_effect = [first, final]

    out = example.demo_tool_use(client=client)

    assert "Paris" in out
    assert client.messages.create.call_count == 2

    # The second call must carry the tool_result wired to the right tool_use_id.
    second_call = client.messages.create.call_args_list[1]
    tool_result_msg = second_call.kwargs["messages"][-1]
    block = tool_result_msg["content"][0]
    assert block["type"] == "tool_result"
    assert block["tool_use_id"] == "toolu_1"
    assert "Paris" in block["content"]


# ---- Live smoke test (opt-in) --------------------------------------------------


@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set; live smoke test skipped",
)
def test_live_basic_smoke():
    out = example.demo_basic()
    assert isinstance(out, str) and out.strip()
