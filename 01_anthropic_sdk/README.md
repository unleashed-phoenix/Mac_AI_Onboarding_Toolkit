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
uv init --python 3.12
uv add anthropic python-dotenv
uv add --dev pytest
cp ../.env.example .env
```
Set `ANTHROPIC_API_KEY` in `.env`.
Note: `uv init` now defaults to Python 3.13; `--python 3.12` keeps this repo on 3.12.

## Minimal usage
`client.messages.create(model="claude-opus-4-8", max_tokens=1024, messages=[...])`.
Prefer prompt caching for long system prompts to cut cost.

## Run
```
uv run python example.py            # all three demos
uv run python example.py basic      # or: streaming | tool_use
uv run pytest                       # mocked tests; live test skips without a key
```
`example.py` defaults to Haiku 4.5 (`SMOKE_MODEL`) to protect quota — swap `MODEL`
to `QUALITY_MODEL` (Opus 4.8) for real work. It shows a single call, streaming, and
a full `get_weather` tool-use round-trip.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| OpenAI SDK (`03`) | Different model family | 2 |
| OpenRouter (`04`) | Claude + others, one key | 1 |
| Via LangChain | Provider-swappable, more deps | 2 |

## Mac vs Windows
Identical Python SDK. No platform difference; keys via `.env`, never shell history.

## Status
✅ Deep-dive complete — `example.py` (basic + streaming + tool use) and `tests/`
(4 mocked, 1 opt-in live) on Python 3.12. Add your `ANTHROPIC_API_KEY` to run live.
