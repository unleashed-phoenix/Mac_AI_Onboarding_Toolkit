"""Tests for example.py (07 — CrewAI).

Tier 1 — Mocked (no API key): patch Crew at the module boundary so no LLM calls happen.
We verify that the crew is constructed with the right number of agents/tasks and that
kickoff is called.

Tier 2 — Live smoke (opt-in): skips unless ANTHROPIC_API_KEY is set.
"""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

import example


# ---- Mocked unit tests ---------------------------------------------------------


def test_demo_crew_creates_two_agents():
    with patch("example.Crew") as mock_crew_cls:
        mock_crew = MagicMock()
        mock_crew.kickoff.return_value = MagicMock(raw="Research and writing complete.")
        mock_crew_cls.return_value = mock_crew

        example.demo_research_write_crew()

    call_kwargs = mock_crew_cls.call_args.kwargs
    assert len(call_kwargs["agents"]) == 2


def test_demo_crew_creates_two_tasks():
    with patch("example.Crew") as mock_crew_cls:
        mock_crew = MagicMock()
        mock_crew.kickoff.return_value = MagicMock(raw="done")
        mock_crew_cls.return_value = mock_crew

        example.demo_research_write_crew()

    call_kwargs = mock_crew_cls.call_args.kwargs
    assert len(call_kwargs["tasks"]) == 2


def test_demo_crew_kickoff_called():
    with patch("example.Crew") as mock_crew_cls:
        mock_crew = MagicMock()
        mock_result = MagicMock()
        mock_result.raw = "Final output."
        mock_crew.kickoff.return_value = mock_result
        mock_crew_cls.return_value = mock_crew

        out = example.demo_research_write_crew()

    mock_crew.kickoff.assert_called_once()
    assert out == "Final output."


def test_demo_crew_custom_topic():
    with patch("example.Crew") as mock_crew_cls:
        mock_crew = MagicMock()
        mock_crew.kickoff.return_value = MagicMock(raw="Custom topic output.")
        mock_crew_cls.return_value = mock_crew

        example.demo_research_write_crew(topic="vector databases")

    researcher_agent = mock_crew_cls.call_args.kwargs["agents"][0]
    assert "vector databases" in researcher_agent.goal


# ---- Live smoke test (opt-in) --------------------------------------------------


@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set; live smoke test skipped",
)
def test_live_crew_smoke():
    out = example.demo_research_write_crew()
    assert isinstance(out, str) and out.strip()
