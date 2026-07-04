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
uv init
uv python pin 3.12
uv add openai python-dotenv
cp ../.env.example .env
```
Set `OPENAI_API_KEY` in `.env`.

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
⬜ Scaffold only.
