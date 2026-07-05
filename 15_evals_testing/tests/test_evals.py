"""
Eval suite for 15_evals_testing/example.py.

Three eval tiers demonstrated:
  Tier 1 — Deterministic: rule-based assertions (no LLM cost).
  Tier 2 — Model-graded: LLM-as-judge scoring (opt-in, requires API key).
  Tier 3 — Live golden dataset: real LLM outputs against expected labels (opt-in).
"""

from __future__ import annotations

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


def _mock_client(response_text: str) -> MagicMock:
    content_block = MagicMock()
    content_block.text = response_text
    resp = MagicMock()
    resp.content = [content_block]
    client = MagicMock()
    client.messages.create.return_value = resp
    return client


# ── Tier 1: deterministic assertions ─────────────────────────────────────────

LONG_TEXT = (
    "The James Webb Space Telescope (JWST) is a space telescope designed to conduct "
    "infrared astronomy. Its high-resolution and high-sensitivity instruments allow it "
    "to view objects too old, distant, or faint for the Hubble Space Telescope. It was "
    "launched in December 2021 and reached its destination at the Sun–Earth L2 point."
)

SENTIMENT_CASES = [
    ("I love this product, it works perfectly!", "positive"),
    ("This is terrible, worst experience ever.", "negative"),
    ("The package arrived on Tuesday.", "neutral"),
]


def test_summarize_returns_single_sentence():
    mock = _mock_client("The JWST is an infrared telescope that surpasses Hubble.")
    result = example.summarize(LONG_TEXT, client=mock)
    assert isinstance(result, str)
    assert len(result) > 10
    assert result.count(".") >= 1
    mock.messages.create.assert_called_once()


def test_summarize_is_shorter_than_original():
    mock = _mock_client("The JWST is an advanced infrared space telescope.")
    result = example.summarize(LONG_TEXT, client=mock)
    assert len(result) < len(LONG_TEXT)


def test_classify_sentiment_returns_valid_label():
    for text, expected in SENTIMENT_CASES:
        mock = _mock_client(expected)
        label = example.classify_sentiment(text, client=mock)
        assert label in ("positive", "negative", "neutral"), (
            f"Unexpected label: {label!r}"
        )


def test_judge_summary_returns_int_in_range():
    mock = _mock_client("4")
    score = example.judge_summary(
        LONG_TEXT, "JWST is an infrared telescope.", client=mock
    )
    assert isinstance(score, int)
    assert 1 <= score <= 5


def test_judge_summary_clamps_bad_output():
    """Judge is robust to malformed LLM output."""
    mock = _mock_client("excellent!")  # not a digit
    score = example.judge_summary("original", "summary", client=mock)
    assert 1 <= score <= 5


# ── Tier 2: model-graded eval (opt-in, requires API key) ─────────────────────


@pytest.mark.skipif(not _HAS_KEY, reason="ANTHROPIC_API_KEY not set")
def test_live_judge_gives_high_score_for_good_summary():
    good_summary = (
        "The James Webb Space Telescope is an infrared observatory that exceeds Hubble."
    )
    score = example.judge_summary(LONG_TEXT, good_summary)
    assert score >= 3, f"Expected score ≥ 3, got {score}"


# ── Tier 3: live golden dataset (opt-in) ─────────────────────────────────────

GOLDEN_SENTIMENT = [
    ("I absolutely love this, it exceeded all expectations!", "positive"),
    ("Broken on arrival. Complete waste of money.", "negative"),
    ("The meeting is scheduled for 3pm.", "neutral"),
]


@pytest.mark.skipif(not _HAS_KEY, reason="ANTHROPIC_API_KEY not set")
@pytest.mark.parametrize("text,expected", GOLDEN_SENTIMENT)
def test_live_sentiment_golden_dataset(text: str, expected: str):
    label = example.classify_sentiment(text)
    assert label == expected, f"For {text!r}: expected {expected!r}, got {label!r}"
