# 04 — OpenRouter

## What it is
A single API (OpenAI-compatible) in front of hundreds of models across providers. One
key, one bill, per-request model choice, automatic fallback.

## WHY reach for it
- A/B test Claude vs GPT vs Gemini vs Qwen with a one-line model string change.
- Fallback routing if a provider is down or rate-limited.
- No lock-in — great default while prototyping.

## WHEN NOT to
- Production where you need provider-specific features (prompt caching, native tool
  formats) → go direct (`01`/`02`/`03`).
- Data-residency constraints → direct provider or Azure (`17`).

## Install
```
cd 04_openrouter
uv init --python 3.12
uv add openai python-dotenv
uv add --dev pytest
cp ../.env.example .env
```
Set `OPENROUTER_API_KEY`. Uses the OpenAI SDK with
`base_url="https://openrouter.ai/api/v1"` — no lock-in.

## Run
```
uv run python example.py            # all demos
uv run python example.py basic      # or: ab_compare
uv run pytest                       # mocked tests (no key); live skips without key
```
`example.py` shows: (1) single call with a swappable model param, (2) A/B comparison —
same prompt, two models side-by-side (`anthropic/claude-haiku-4-5` vs `openai/gpt-4o-mini`).

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| Direct SDKs (`01`–`03`) | Full features, more keys | 1 |
| LiteLLM | Self-hosted proxy alternative | 2 |

## Mac vs Windows
No difference.

## Status
✅ Deep-dive complete — `example.py` (basic + A/B compare) and `tests/` (4 mocked,
1 opt-in live) on Python 3.12. Add `OPENROUTER_API_KEY` to `.env` to run live.
