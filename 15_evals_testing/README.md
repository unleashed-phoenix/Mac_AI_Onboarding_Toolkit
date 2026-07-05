# 15 — Evals & Testing

## What it is
Systematic evaluation and regression testing for LLM apps: datasets of inputs + expected
behavior, scored by rules, model-graders, or human review. Wrap whatever you ship.

## WHY reach for it
- LLM outputs drift — you can't ship changes safely without evals.
- Catch regressions when you swap models/prompts (ties to the compatibility matrix).
- Turns "seems better" into measured, repeatable numbers.

## WHEN NOT to
- Throwaway prototype → skip until it matters.

## Install
```
cd 15_evals_testing
uv init --python 3.12
uv add anthropic langsmith python-dotenv
uv add --dev pytest
cp ../.env.example .env
```
Note: `promptfoo-py` is not a real PyPI package — promptfoo is a Node.js CLI tool.
For Python evals, use pytest + langsmith + model-graded assertions (shown here).
Optional: `LANGSMITH_API_KEY` + `LANGSMITH_TRACING=true` for cloud tracing.

## Run
```
uv run pytest tests/               # Tier 1: 5 deterministic, no API key
uv run pytest tests/ -v            # with ANTHROPIC_API_KEY: Tier 2+3 also run
```
Three eval tiers: (1) rule-based assertions — fast, free; (2) LLM-as-judge scoring —
flexible; (3) golden dataset parametrized tests — regression suite.

## Approach
Start with `pytest` + a small golden dataset and assertion-based checks. Add model-graded
evals for open-ended outputs. Use LangSmith or promptfoo for dashboards/CI.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| promptfoo (JS/CLI) | Language-agnostic | 2 |
| Ragas | RAG-specific metrics | 2 |
| DeepEval | Pytest-style LLM asserts | 1 |

## Mac vs Windows
No difference.

## Status
✅ Deep-dive complete — `example.py` (summarizer + classifier + LLM judge) and
`tests/test_evals.py` (5 deterministic + 4 opt-in live) on Python 3.12.
Add `ANTHROPIC_API_KEY` to run Tier 2 (LLM judge) and Tier 3 (golden dataset) evals.
