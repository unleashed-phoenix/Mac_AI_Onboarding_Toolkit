# 05 — LangChain

## What it is
A framework of composable pieces (models, prompts, retrievers, tools, output parsers)
with a common interface across providers. The "glue" layer.

## WHY reach for it
- Swap providers behind one interface.
- Batteries-included retrieval, memory, and tool integrations.
- Huge ecosystem; most tutorials assume it.

## WHEN NOT to
- Simple single-model calls → raw SDK is leaner (fewer deps, fewer tokens).
- Complex cyclic control flow → LangGraph (`06`) is purpose-built.
- It can be over-abstracted; don't add it "just in case".

## Install
```
cd 05_langchain
uv init
uv python pin 3.12
uv add langchain langchain-anthropic langchain-openai python-dotenv
cp ../.env.example .env
```

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| Raw SDKs | Less magic, more control | 2 |
| LlamaIndex | Retrieval-first framing | 3 |
| LangGraph (`06`) | Same ecosystem, stateful | 2 |

## Mac vs Windows
No difference.

## Status
⬜ Scaffold only.
