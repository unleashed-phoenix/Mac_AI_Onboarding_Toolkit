"""Tests for example.py (04 — OpenRouter).

Tier 1 — Mocked (no API key): inject mock OpenAI client via demo_x(client=...).
Tier 2 — Live smoke (opt-in): skips unless OPENROUTER_API_KEY is set.
"""

from __future__ import annotations

import os
from unittest.mock import MagicMock

import pytest

import example


def _make_completion(text: str) -> MagicMock:
    msg = MagicMock()
    msg.content = text
    choice = MagicMock()
    choice.message = msg
    resp = MagicMock()
    resp.choices = [choice]
    return resp


# ---- Mocked unit tests ---------------------------------------------------------


def test_demo_basic_default_model_mocked():
    client = MagicMock()
    client.chat.completions.create.return_value = _make_completion(
        "OpenRouter is a multi-model API gateway."
    )
    out = example.demo_basic(client=client)
    assert len(out) > 0
    call_kwargs = client.chat.completions.create.call_args.kwargs
    assert call_kwargs["model"] == example.MODEL_A


def test_demo_basic_custom_model_mocked():
    client = MagicMock()
    client.chat.completions.create.return_value = _make_completion("Answer from GPT.")
    out = example.demo_basic(model=example.MODEL_B, client=client)
    assert len(out) > 0
    call_kwargs = client.chat.completions.create.call_args.kwargs
    assert call_kwargs["model"] == example.MODEL_B


def test_demo_ab_compare_mocked():
    client = MagicMock()
    client.chat.completions.create.side_effect = [
        _make_completion("Claude says: no lock-in."),
        _make_completion("GPT says: automatic fallback."),
    ]
    results = example.demo_ab_compare(client=client)
    assert len(results) == 2
    assert example.MODEL_A in results
    assert example.MODEL_B in results
    assert client.chat.completions.create.call_count == 2


def test_demo_ab_compare_calls_different_models():
    client = MagicMock()
    client.chat.completions.create.return_value = _make_completion("response")
    example.demo_ab_compare(client=client)
    models_called = [
        c.kwargs["model"] for c in client.chat.completions.create.call_args_list
    ]
    assert models_called[0] != models_called[1]


# ---- Live smoke test (opt-in) --------------------------------------------------


@pytest.mark.skipif(
    not os.getenv("OPENROUTER_API_KEY"),
    reason="OPENROUTER_API_KEY not set; live smoke test skipped",
)
def test_live_basic_smoke():
    out = example.demo_basic()
    assert isinstance(out, str) and out.strip()
