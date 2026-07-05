"""
15_evals_testing — Evaluating LLM output quality
=================================================

WHY reach for it
- LLMs are non-deterministic: CI passes today, regresses tomorrow. Evals catch that.
- Three tiers (cheapest to most expensive):
    1. Deterministic assertions — rule-based (length, keywords, JSON schema). Fast, free.
    2. Model-graded eval (LLM-as-judge) — flexible but costs tokens.
    3. Human eval + LangSmith dataset — gold standard, expensive, good for regression suites.

This module is the "system under test":
- `summarize()` — the LLM function being evaluated.
- `judge_summary()` — a lightweight LLM-as-judge that scores a summary 1-5.
- `classify_sentiment()` — a structured-output classifier (tested with golden dataset).

The actual eval test suite lives in tests/test_evals.py.

Alternative eval frameworks
| Tool | Layer | Note |
|---|---|---|
| deepeval | pytest plugin | LLM-as-judge metrics, RAG evals |
| ragas | RAG-specific | faithfulness, answer relevancy |
| promptfoo | CLI/YAML | multi-provider, no Python SDK |
| LangSmith | cloud dashboard | traces + dataset regression |

Switching cost to deepeval: 2 (add dep, wrap metrics around existing pytest assertions).
"""

from __future__ import annotations

import os

import anthropic
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL = "claude-haiku-4-5-20251001"


def summarize(text: str, client: anthropic.Anthropic | None = None) -> str:
    """Summarize *text* in one sentence. This is the function being evaluated."""
    c = client or anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = c.messages.create(
        model=MODEL,
        max_tokens=128,
        system="Summarize the following text in exactly one sentence.",
        messages=[{"role": "user", "content": text}],
    )
    return response.content[0].text.strip()


def classify_sentiment(text: str, client: anthropic.Anthropic | None = None) -> str:
    """Classify text as positive / negative / neutral. Returns lowercase label."""
    c = client or anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = c.messages.create(
        model=MODEL,
        max_tokens=16,
        system=(
            "Classify the sentiment of the following text. "
            "Reply with exactly one word: positive, negative, or neutral."
        ),
        messages=[{"role": "user", "content": text}],
    )
    return response.content[0].text.strip().lower()


def judge_summary(
    original: str, summary: str, client: anthropic.Anthropic | None = None
) -> int:
    """LLM-as-judge: rate the summary quality 1 (poor) to 5 (excellent). Returns the int."""
    c = client or anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = c.messages.create(
        model=MODEL,
        max_tokens=16,
        system=(
            "You are an evaluator. Rate the quality of the summary vs the original text.\n"
            "Reply with ONLY a single digit 1-5 where 5 is excellent. No other text."
        ),
        messages=[
            {
                "role": "user",
                "content": f"Original:\n{original}\n\nSummary:\n{summary}",
            }
        ],
    )
    raw = response.content[0].text.strip()
    try:
        score = int(raw[0])
        return max(1, min(5, score))
    except (ValueError, IndexError):
        return 1
