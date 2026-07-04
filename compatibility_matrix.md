# Compatibility Matrix

How the pieces of this toolkit fit together, and how painful it is to swap one for
another. Goal: never get locked in. July 2026 view.

## Provider ↔ SDK

| You want to call... | Native SDK | Also reachable via |
|---|---|---|
| Claude (Anthropic) | `01_anthropic_sdk` | OpenRouter, LangChain, LangGraph, CrewAI |
| GPT / OpenAI | `03_openai_sdk` | OpenRouter, LangChain, LangGraph, CrewAI |
| Gemini (Google) | `02_google_adk` | OpenRouter, LangChain |
| Grok (xAI) | `16_grok_xai` (OpenAI-compatible) | OpenRouter |
| Local (Ollama/MLX) | `09_ollama_mlx_local` | LangChain, CrewAI (OpenAI-compatible endpoint) |
| Qwen local | `18_qwen_local` | Ollama / MLX |
| Azure-hosted OpenAI | `17_azure_openai` | LangChain (AzureOpenAI class) |

**Key insight:** most providers now expose an **OpenAI-compatible** endpoint. That means
`03_openai_sdk` code often works against Grok, local Ollama, and OpenRouter just by
changing `base_url` and `api_key`. This is your cheapest escape hatch from lock-in.

## Orchestration layers — when to use which

| Layer | Reach for it when | Folder |
|---|---|---|
| Raw SDK | One model, simple call, max control, fewest deps | 01 / 02 / 03 |
| OpenRouter | You want to A/B models or need automatic fallback | 04 |
| LangChain | You need retrieval, tools, and provider-swapping glue | 05 |
| LangGraph | You need loops, branching, human-in-loop, durable state | 06 |
| CrewAI | You want role-based multi-agent collaboration | 07 |

Rule of thumb: **start at the lowest layer that works.** Every abstraction adds tokens,
latency, and a dependency to maintain. Add LangChain/LangGraph only when raw SDK calls
start getting tangled.

## Switching cost (1 = trivial, 5 = painful)

| From → To | Cost | Notes |
|---|---|---|
| OpenAI SDK → Grok / local | 1 | Change `base_url` + key; same code |
| Direct SDK → OpenRouter | 1 | Swap client init, keep call shape |
| LangChain → raw SDK | 2 | Unwind chains, but prompts port over |
| LangChain → LangGraph | 2 | Same ecosystem; add graph/state |
| CrewAI → LangGraph | 4 | Different mental model (roles vs graph) |
| Cloud model → local Qwen | 3 | Quality drop; prompt tuning needed |
| ChromaDB → other vector DB | 2 | LangChain abstracts the retriever |

## Local model fit (24 GB unified RAM)

| Model | Approx RAM | Verdict |
|---|---|---|
| qwen2.5-coder:14b Q4 | ~9 GB | ✅ daily coding driver |
| gemma4:12b Q4 | ~7.6 GB | ✅ general reasoning |
| nomic-embed-text | ~0.3 GB | ✅ embeddings for RAG |
| qwen3.6:27b dense | ~17 GB | ⚠️ best quality, close other apps |
| qwen3.5:35b-a3b MoE | ~20 GB | ⚠️ tight but possible |
| 70B+ / DeepSeek V3+ | 40 GB+ | ❌ won't fit locally |

## Cross-cutting tools

- `10_structured_outputs` works with 01/02/03/04 — request typed JSON from any provider.
- `08_chromadb_rag` pairs with `13_huggingface` (embeddings) and `09_ollama_mlx_local`
  (local embeddings via `nomic-embed-text`).
- `14_mcp_servers` exposes your tools to Claude Code and other MCP clients.
- `11_fastapi_serving` + `12_streamlit_gradio` wrap any of the above for deployment/demo.
- `15_evals_testing` should wrap whatever you ship — provider-agnostic.
