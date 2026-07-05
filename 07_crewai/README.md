# 07 — CrewAI

## What it is
A framework for **role-based multi-agent** teams: each agent has a role, goal, and tools;
a "crew" coordinates them on tasks sequentially or hierarchically.

## WHY reach for it
- Natural fit when a problem decomposes into roles (researcher → writer → reviewer).
- Fast to prototype collaborative agents.
- Model-agnostic (works with local models via OpenAI-compatible endpoint).

## WHEN NOT to
- You need precise, debuggable control flow → LangGraph (`06`).
- Single agent → raw SDK or Agents SDK.

## Install
```
cd 07_crewai
uv init --python 3.12
uv add "crewai[anthropic]" python-dotenv
uv add --dev pytest
cp ../.env.example .env
```
Set `ANTHROPIC_API_KEY` in `.env`.
Note: `crewai[anthropic]` installs the native Anthropic provider. For local Ollama
instead, see the swap note in `example.py` (no key needed, zero cost).

## Run
```
uv run python example.py    # researcher + writer crew
uv run pytest               # mocked tests (no key); live skips without key
```
`example.py` shows a 2-agent sequential crew: Researcher gathers facts, Writer
produces a paragraph. Drop-in Ollama swap is documented in the module docstring.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| LangGraph (`06`) | Explicit state machine | 4 |
| AutoGen | Conversation-centric agents | 4 |
| OpenAI Agents SDK | Handoffs, lighter | 3 |

## Mac vs Windows
No difference. Can drive local Qwen (`18`) to cut cost.

## Status
✅ Deep-dive complete — `example.py` (Researcher + Writer crew) and `tests/`
(4 mocked, 1 opt-in live) on Python 3.12. Add `ANTHROPIC_API_KEY` to run live.
