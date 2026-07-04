# Mac_AI_Onboarding_Toolkit

A living boilerplate reference for AI development on macOS (MacBook Pro M4 Pro, 24 GB
unified RAM). Each numbered sub-folder covers **one** framework or tool: what it is,
**why** you'd reach for it, how to install and run it the current (July 2026) way, honest
alternatives, and Mac-vs-Windows gotchas. Every folder is meant to become a working,
reusable starting point for real projects.

Built during **Phase 5** of the Mac onboarding roadmap. Right now this is the **scaffold
+ instructions** — each folder has a README you can act on. Runnable code gets filled in
per-folder as you deep-dive each one.

## Conventions used everywhere in this toolkit

These follow the project's non-negotiable teaching rules:

- **Environments:** `uv` only. Never `pip` (raw), `poetry`, `pyenv`, or system Python.
- **Python:** 3.12 is primary for AI/DS work (3.13 is less stable for some ML wheels).
- **One `.venv` per sub-folder**, one `.env` per sub-folder (gitignored).
- **Commands are one per line** — never backslash line-continuation.
- **API testing:** Bruno. Never Postman.
- **Grok** = xAI (Elon Musk). Never write "Groq".
- **Local models:** always sized for 24 GB RAM (~20–22 GB usable). See
  `09_ollama_mlx_local/` and `18_qwen_local/`.
- **Philosophy:** WHY before HOW, always compare alternatives, always note ease of
  switching.

## Standard setup for any sub-folder

Each folder is self-contained. To start working in one:

```
cd 01_anthropic_sdk
uv init
uv python pin 3.12
uv add <packages listed in that folder's README>
cp ../.env.example .env
```

Then edit `.env` with the keys you need. Run examples with:

```
uv run python example.py
```

> Note: `uv python pin 3.12` is safe **inside a project folder**. Never pin Python or set
> `UV_PYTHON` in your home directory or global `.zshrc`.

## Folder map

| # | Folder | Covers |
|---|--------|--------|
| 01 | `01_anthropic_sdk` | Claude API — the default reasoning/agent model |
| 02 | `02_google_adk` | Google Agent Development Kit (Gemini agents) |
| 03 | `03_openai_sdk` | OpenAI SDK + Agents SDK |
| 04 | `04_openrouter` | One API key, hundreds of models; routing/fallback |
| 05 | `05_langchain` | Chains, prompts, model-agnostic glue |
| 06 | `06_langgraph` | Stateful, cyclic agent graphs |
| 07 | `07_crewai` | Multi-agent "crews" with roles |
| 08 | `08_chromadb_rag` | Local vector DB + retrieval-augmented generation |
| 09 | `09_ollama_mlx_local` | Local models on Apple Silicon (MLX backend) |
| 10 | `10_structured_outputs` | Guaranteed JSON / Pydantic-typed responses |
| 11 | `11_fastapi_serving` | Serve models/agents as an API |
| 12 | `12_streamlit_gradio` | Fast UIs for AI demos |
| 13 | `13_huggingface` | Models, datasets, `transformers`, Inference |
| 14 | `14_mcp_servers` | Model Context Protocol — tools for Claude/agents |
| 15 | `15_evals_testing` | Evaluating and regression-testing LLM apps |
| 16 | `16_grok_xai` | Grok via xAI API |
| 17 | `17_azure_openai` | OpenAI models through Azure (enterprise) — lowest priority |
| 18 | `18_qwen_local` | Qwen family locally, sized for 24 GB |

See `compatibility_matrix.md` for how these interoperate and how easily you can swap one
for another.

## Roadmap position

Phases 0–2 complete · Phase 3 (frameworks) and Phase 4 (coding assistants) skimmed,
4·1 Claude Code done in depth · **Phase 5 = this toolkit** · Phases 6–9 upcoming.
