# 01 — Anthropic SDK (Claude)

## What it is
The official Python SDK for the Claude API. Your default for reasoning, tool use, and
agentic work. Model landscape (July 2026): Claude Opus 4.8 top reasoning/agentic,
Fable 5 newest, Haiku for cheap/fast.

## WHY reach for it
- Best-in-class reasoning and instruction following.
- Native tool use, streaming, vision, and prompt caching.
- First-party MCP support (see `14_mcp_servers`).

## WHEN NOT to
- If you need to A/B many providers → use OpenRouter (`04`).
- If it's a pure retrieval/glue app → LangChain (`05`) may be simpler.

## Install
```
cd 01_anthropic_sdk
uv init
uv python pin 3.12
uv add anthropic python-dotenv
cp ../.env.example .env
```
Set `ANTHROPIC_API_KEY` in `.env`.

## Minimal usage
`client.messages.create(model="claude-opus-4-8", max_tokens=1024, messages=[...])`.
Prefer prompt caching for long system prompts to cut cost.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| OpenAI SDK (`03`) | Different model family | 2 |
| OpenRouter (`04`) | Claude + others, one key | 1 |
| Via LangChain | Provider-swappable, more deps | 2 |

## Mac vs Windows
Identical Python SDK. No platform difference; keys via `.env`, never shell history.

## Status
⬜ Scaffold only — add `example.py` on deep-dive.
