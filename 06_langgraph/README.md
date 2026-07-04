# 06 — LangGraph

## What it is
LangChain's graph engine for **stateful, cyclic** agent workflows: nodes, edges,
branching, loops, human-in-the-loop, and durable checkpointed state.

## WHY reach for it
- Real control flow (loops/retries/branches) that plain chains can't express.
- Persistent state + resume; good for long-running agents.
- Interops with all LangChain models/tools.

## WHEN NOT to
- Linear pipeline → LangChain (`05`) chains are simpler.
- Role-play multi-agent → CrewAI (`07`) is more ergonomic for that framing.

## Install
```
cd 06_langgraph
uv init
uv python pin 3.12
uv add langgraph langchain-anthropic python-dotenv
cp ../.env.example .env
```

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| CrewAI (`07`) | Roles vs explicit graph | 4 |
| OpenAI Agents SDK | Lighter, OpenAI-centric | 3 |
| LangChain (`05`) | No cycles/state | 2 |

## Mac vs Windows
No difference.

## Status
⬜ Scaffold only.
