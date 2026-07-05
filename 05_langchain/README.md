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
uv init --python 3.12
uv add langchain langchain-anthropic langchain-openai numpy python-dotenv
uv add --dev pytest
cp ../.env.example .env
```
Set `ANTHROPIC_API_KEY` in `.env`; `OPENAI_API_KEY` optional (for provider-swap demo).
Note: `numpy` is required by `InMemoryVectorStore` for cosine similarity.

## Run
```
uv run python example.py              # all three demos
uv run python example.py basic_chain  # or: provider_swap | retrieval
uv run pytest                         # mocked tests (no key); live skips without key
```
`example.py` shows: (1) LCEL `ChatAnthropic | StrOutputParser` chain, (2) same chain
swapped to `ChatOpenAI` in one line, (3) `InMemoryVectorStore` retrieve-then-answer RAG.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| Raw SDKs | Less magic, more control | 2 |
| LlamaIndex | Retrieval-first framing | 3 |
| LangGraph (`06`) | Same ecosystem, stateful | 2 |

## Mac vs Windows
No difference.

## Status
✅ Deep-dive complete — `example.py` (LCEL chain + provider swap + retrieval) and
`tests/` (4 mocked, 1 opt-in live) on Python 3.12. Add `ANTHROPIC_API_KEY` to run live.
