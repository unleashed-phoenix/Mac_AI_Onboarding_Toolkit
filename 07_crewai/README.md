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
uv init
uv python pin 3.12
uv add crewai python-dotenv
cp ../.env.example .env
```

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| LangGraph (`06`) | Explicit state machine | 4 |
| AutoGen | Conversation-centric agents | 4 |
| OpenAI Agents SDK | Handoffs, lighter | 3 |

## Mac vs Windows
No difference. Can drive local Qwen (`18`) to cut cost.

## Status
⬜ Scaffold only.
