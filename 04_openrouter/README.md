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
uv init
uv python pin 3.12
uv add openai python-dotenv
cp ../.env.example .env
```
Set `OPENROUTER_API_KEY`. Use the OpenAI SDK with
`base_url="https://openrouter.ai/api/v1"`.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| Direct SDKs (`01`–`03`) | Full features, more keys | 1 |
| LiteLLM | Self-hosted proxy alternative | 2 |

## Mac vs Windows
No difference.

## Status
⬜ Scaffold only.
