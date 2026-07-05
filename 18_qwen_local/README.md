# 18 — Qwen Local

## What it is
Running the Qwen model family locally on this Mac, sized for 24 GB unified RAM. Qwen is a
top open-source line; `qwen2.5-coder:14b` is already the daily local coding driver here.

## WHY reach for it
- Strong open weights, especially for coding (`qwen2.5-coder`).
- Free, private, offline via Ollama/MLX (`09`).
- Cloud Qwen 3.7 Max exists as a budget option, but this folder = local.

## WHEN NOT to
- Need frontier quality → cloud Claude/GPT/Gemini.
- Model exceeds RAM budget (see below).

## Install / pull
```
cd 18_qwen_local
uv init --python 3.12
uv add ollama python-dotenv
uv add --dev pytest
```
Models (via Ollama — both already installed on this Mac):
```
ollama pull qwen2.5-coder:14b
ollama pull qwen3.6:27b
```

## Run
```
uv run python example.py              # all three demos (needs Ollama running)
uv run python example.py basic        # or: streaming | embeddings
uv run pytest                         # mocked tests run without Ollama; live if running
```
Uses the `ollama` Python package (native API) — different from folder 09 which uses the
OpenAI-compatible HTTP shim. Demos: (1) chat, (2) streaming, (3) embeddings.

## 24 GB RAM guidance
- `qwen2.5-coder:14b` Q4 (~9 GB) — ✅ comfortable, daily driver.
- `qwen3.6:27b` dense (~17 GB) — ⚠️ best quality, close other apps first.
- `qwen3.5:35b-a3b` MoE (~20 GB, 3B active) — ⚠️ tight but possible.
- Anything 70B+ — ❌ won't fit.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| gemma4:12b (`09`) | General vs coding | 1 |
| Qwen cloud (Phase 9) | Bigger, not private | 2 |

## Mac vs Windows
MLX backend is Apple-Silicon-only; on Windows you'd use CUDA/llama.cpp.

## Status
✅ Deep-dive complete — `example.py` (chat + streaming + embeddings via ollama Python
client) and `tests/` (4 mocked, 1 live with Ollama running) on Python 3.12.
