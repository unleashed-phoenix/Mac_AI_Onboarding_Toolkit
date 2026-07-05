"""Tests for example.py (05 — LangChain).

Tier 1 — Mocked (no API key): patch ChatAnthropic.invoke to return a canned AIMessage.
Tier 2 — Live smoke (opt-in): skips unless ANTHROPIC_API_KEY is set.
"""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest
from langchain_core.messages import AIMessage

import example


def _mock_anthropic(text: str = "LangChain is a framework for LLM applications."):
    """Return a patch context that makes ChatAnthropic.invoke return a canned AIMessage."""
    return patch(
        "langchain_anthropic.ChatAnthropic.invoke",
        return_value=AIMessage(content=text),
    )


# ---- Mocked unit tests ---------------------------------------------------------


def test_demo_basic_chain_mocked():
    with _mock_anthropic("LangChain is a framework for LLM apps."):
        out = example.demo_basic_chain()
    assert isinstance(out, str) and len(out) > 0


def test_demo_provider_swap_skips_without_openai_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    out = example.demo_provider_swap()
    assert "skipping" in out.lower() or "not set" in out.lower()


def test_demo_retrieval_mocked():
    with _mock_anthropic("RAG retrieves relevant chunks then passes them to the LLM."):
        out = example.demo_retrieval()
    assert isinstance(out, str) and len(out) > 0


def test_retrieval_uses_anthropic_model():
    with _mock_anthropic("answer") as mock_invoke:
        example.demo_retrieval()
    mock_invoke.assert_called_once()


# ---- Live smoke test (opt-in) --------------------------------------------------


@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set; live smoke test skipped",
)
def test_live_basic_chain_smoke():
    out = example.demo_basic_chain()
    assert isinstance(out, str) and out.strip()
