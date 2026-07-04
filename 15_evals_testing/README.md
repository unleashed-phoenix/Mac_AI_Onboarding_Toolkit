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
uv init
uv python pin 3.12
uv add pytest promptfoo-py langsmith python-dotenv
cp ../.env.example .env
```
(LangSmith tracing: set `LANGSMITH_API_KEY` + `LANGSMITH_TRACING=true` in `.env`.)

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
⬜ Scaffold only.
