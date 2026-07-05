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
uv init --python 3.12
uv add langgraph langchain-anthropic python-dotenv
uv add --dev pytest
cp ../.env.example .env
```
Set `ANTHROPIC_API_KEY` in `.env`.

## Run
```
uv run python example.py               # all demos
uv run python example.py simple_graph  # or: react_loop
uv run pytest                          # mocked tests (no key); live skips without key
```
`example.py` shows: (1) linear `START → llm → END` graph, (2) ReAct loop with
`get_weather` tool — `tools_condition` routes back to `llm_node` until done.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| CrewAI (`07`) | Roles vs explicit graph | 4 |
| OpenAI Agents SDK | Lighter, OpenAI-centric | 3 |
| LangChain (`05`) | No cycles/state | 2 |

## Mac vs Windows
No difference.

## Status
✅ Deep-dive complete — `example.py` (simple graph + ReAct loop) and `tests/`
(4 mocked, 1 opt-in live) on Python 3.12. Add `ANTHROPIC_API_KEY` to run live.
