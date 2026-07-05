"""Tests for example.py (06 — LangGraph).

Tier 1 — Mocked (no API key): patch ChatAnthropic to return canned messages so the
graph runs without any network calls. The graph compilation and routing logic is
exercised even under the mock.

Tier 2 — Live smoke (opt-in): skips unless ANTHROPIC_API_KEY is set.
"""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.messages import AIMessage

import example


def _make_ai_message(text: str, tool_calls: list | None = None) -> AIMessage:
    return AIMessage(content=text, tool_calls=tool_calls or [])


# ---- Mocked unit tests ---------------------------------------------------------


def test_demo_simple_graph_mocked():
    with patch(
        "langchain_anthropic.ChatAnthropic.invoke",
        return_value=_make_ai_message("LangGraph is a stateful graph framework."),
    ):
        out = example.demo_simple_graph()
    assert isinstance(out, str) and len(out) > 0


def test_demo_react_loop_no_tool_call():
    """When the model returns no tool_calls, the graph should route to END immediately."""
    with patch("langchain_anthropic.ChatAnthropic.bind_tools") as mock_bind:
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = _make_ai_message("It is sunny in Paris.")
        mock_bind.return_value = mock_llm
        out = example.demo_react_loop()
    assert isinstance(out, str) and len(out) > 0


def test_get_weather_tool():
    result = example.get_weather.invoke({"location": "Paris"})
    assert "Paris" in result
    assert "22C" in result


def test_simple_graph_returns_string():
    with patch(
        "langchain_anthropic.ChatAnthropic.invoke",
        return_value=_make_ai_message("answer"),
    ):
        out = example.demo_simple_graph()
    assert isinstance(out, str)


# ---- Live smoke test (opt-in) --------------------------------------------------


@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set; live smoke test skipped",
)
def test_live_simple_graph_smoke():
    out = example.demo_simple_graph()
    assert isinstance(out, str) and out.strip()
