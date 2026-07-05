"""Tests for example.py (02 — Google ADK).

Tier 1 — Mocked (no API key, no network): patches Runner and InMemorySessionService
at the module level so _run_agent never makes a real call.

Tier 2 — Live smoke (opt-in): skips unless GOOGLE_API_KEY is set.
"""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

import example


def _fake_event(text: str, final: bool = True) -> MagicMock:
    part = MagicMock()
    part.text = text
    content = MagicMock()
    content.parts = [part]
    event = MagicMock()
    event.is_final_response.return_value = final
    event.content = content
    return event


def _patch_adk(reply: str):
    """Context manager that patches InMemorySessionService + Runner to return reply."""
    mock_session = MagicMock()
    mock_session.id = "sess-test"

    mock_svc = MagicMock()
    mock_svc.create_session_sync.return_value = mock_session

    mock_runner = MagicMock()
    mock_runner.run.return_value = iter([_fake_event(reply)])

    patch_svc = patch("example.InMemorySessionService", return_value=mock_svc)
    patch_runner = patch("example.Runner", return_value=mock_runner)
    return patch_svc, patch_runner


# ---- Mocked unit tests ---------------------------------------------------------


def test_get_weather_stub():
    result = example.get_weather("Tokyo")
    assert isinstance(result, dict)
    assert "Tokyo" in str(result)


def test_demo_basic_mocked():
    p_svc, p_runner = _patch_adk("The Google ADK is Google's agent framework.")
    with p_svc, p_runner:
        result = example.demo_basic()
    assert isinstance(result, str)
    assert len(result) > 0


def test_demo_tool_use_mocked():
    p_svc, p_runner = _patch_adk("It is 22C and sunny in Tokyo.")
    with p_svc, p_runner:
        result = example.demo_tool_use()
    assert isinstance(result, str)
    assert len(result) > 0


def test_run_agent_returns_empty_when_no_final_event():
    part = MagicMock()
    part.text = "intermediate"
    content = MagicMock()
    content.parts = [part]
    non_final = MagicMock()
    non_final.is_final_response.return_value = False
    non_final.content = content

    mock_session = MagicMock()
    mock_session.id = "s"
    mock_svc = MagicMock()
    mock_svc.create_session_sync.return_value = mock_session
    mock_runner = MagicMock()
    mock_runner.run.return_value = iter([non_final])

    agent = MagicMock()
    with patch("example.InMemorySessionService", return_value=mock_svc):
        with patch("example.Runner", return_value=mock_runner):
            result = example._run_agent(agent, "hello")
    assert result == ""


# ---- Live smoke test (opt-in) --------------------------------------------------


@pytest.mark.skipif(
    not os.getenv("GOOGLE_API_KEY"),
    reason="GOOGLE_API_KEY not set; live smoke test skipped",
)
def test_live_basic_smoke():
    out = example.demo_basic()
    assert isinstance(out, str) and out.strip()
