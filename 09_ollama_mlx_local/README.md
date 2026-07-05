# 09 — Ollama + MLX (local models on Apple Silicon)

## What it is
Ollama runs open models locally with a clean CLI/API; on Apple Silicon it uses the **MLX**
backend for fast, memory-efficient inference. Already installed and working on this Mac.

## WHY reach for it
- Free, private, offline. No per-token cost, no data leaving the machine.
- OpenAI-compatible endpoint at `localhost:11434/v1` → reuse `03` code.
- MLX is tuned for unified memory on M-series chips.

## WHEN NOT to
- You need frontier quality → cloud (Claude/GPT/Gemini).
- Model won't fit in 24 GB (see below).

## Already installed
```
qwen2.5-coder:14b   # ~9 GB   daily coding driver
gemma4:12b          # ~7.6 GB general reasoning
nomic-embed-text    # ~0.3 GB embeddings for RAG (08)
```
Pull more: `ollama pull <model>`. Serve is automatic.

## 24 GB RAM guidance
Fits: 12–14B Q4 comfortably. Tight (close apps): `qwen3.6:27b` (~17 GB, best quality),
`qwen3.5:35b-a3b` MoE (~20 GB). Do NOT install 70B+ or DeepSeek V3+ — won't fit.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| LM Studio | GUI, same models | 1 |
| MLX directly | Lower-level, more control | 3 |
| llama.cpp | Manual, maximal control | 3 |

## Mac vs Windows
**Big difference:** MLX is Apple-Silicon-only. On Windows you'd use CUDA/llama.cpp instead.

## Install (example only — Ollama/MLX already set up)
```
cd 09_ollama_mlx_local
uv init --python 3.12
uv add openai python-dotenv
uv add --dev pytest
```
No API key needed. Requires Ollama running (`ollama serve`).

## Run
```
uv run python example.py            # all three demos
uv run python example.py basic      # or: streaming | embeddings
uv run pytest                       # mocked tests run without Ollama; live skips if not running
```
`example.py` shows: (1) chat via OpenAI-compatible endpoint, (2) streaming,
(3) embeddings with nomic-embed-text — same client, same endpoint, different model.

## Status
✅ Deep-dive complete — `example.py` (basic + streaming + embeddings) and `tests/`
(4 mocked, 1 opt-in live) on Python 3.12. Ollama live tests pass when server is running.
