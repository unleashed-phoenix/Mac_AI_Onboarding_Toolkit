# 03 — OpenAI SDK + Agents SDK

## What it is
Official OpenAI Python SDK plus the Agents SDK for tool-calling agents. Also the de-facto
*wire format*: Grok, Ollama, OpenRouter, and Azure all speak "OpenAI-compatible".

## WHY reach for it
- GPT-5.5 leads coding + autonomous agents (July 2026).
- The `base_url` trick makes this code portable across many providers.
- Mature Agents SDK: handoffs, guardrails, tracing.

## WHEN NOT to
- Multi-provider routing/fallback → OpenRouter (`04`).
- Heavy stateful graphs → LangGraph (`06`).

## Install
```
cd 03_openai_sdk
uv init --python 3.12
uv add openai python-dotenv
uv add --dev pytest
cp ../.env.example .env
```
Set `OPENAI_API_KEY` in `.env`.

## Run
```
uv run python example.py            # all three demos
uv run python example.py basic      # or: streaming | tool_use
uv run pytest                       # mocked tests (no key); live skips without key
```
`example.py` shows: (1) basic call, (2) streaming via `.stream()`, (3) full
`get_weather` function-calling round-trip. The portability trick is in the docstring.

## The portability trick
Point the same client at other providers:
`OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")` → local models.
`base_url="https://api.x.ai/v1"` + `XAI_API_KEY` → Grok (`16`).

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| Anthropic SDK (`01`) | Claude models | 2 |
| OpenRouter (`04`) | Many models, one key | 1 |

## Mac vs Windows
Identical. No platform difference.

## Status
✅ Deep-dive complete — `example.py` (basic + streaming + tool use) and `tests/`
(4 mocked, 1 opt-in live) on Python 3.12. Add `OPENAI_API_KEY` to `.env` to run live.
