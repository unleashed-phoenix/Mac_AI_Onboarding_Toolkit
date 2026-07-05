# 13 — Hugging Face

## What it is
The hub for open models and datasets, plus `transformers`/`datasets` libraries and hosted
Inference. Your source for embeddings, small task models, and fine-tuning bases.

## WHY reach for it
- Enormous catalog of open weights + datasets.
- `transformers` runs locally; Inference API for hosted calls.
- Embeddings for RAG (`08`); Spaces hosting for Gradio (`12`).

## WHEN NOT to
- You only need chat completions → a provider SDK is simpler.
- Big local models → prefer Ollama/MLX (`09`) for Apple-Silicon efficiency.

## Install
```
cd 13_huggingface
uv init --python 3.12
uv add huggingface_hub transformers datasets python-dotenv
uv add --dev pytest
cp ../.env.example .env
```
Set `HF_TOKEN`. Login: `uv run huggingface-cli login`.

## Run
```
uv run python example.py           # all demos (chat + generate need HF_TOKEN)
uv run python example.py list      # or: chat | generate | pipeline
uv run pytest                      # 4 mocked + 1 skipped (no token needed)
```
`example.py` shows: (1) list trending models, (2) chat completion via Inference API,
(3) text generation via Inference API, (4) local pipeline with sentiment model.
Note: `demo_local_pipeline` downloads ~67 MB on first run (distilbert).

## 24 GB RAM note
On Apple Silicon prefer MLX-format models or run via Ollama. Full-precision
`transformers` models can blow past RAM fast — check model size before loading.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| Ollama/MLX (`09`) | Local, Apple-optimized | 2 |
| Replicate | Hosted inference | 2 |

## Mac vs Windows
`transformers` uses MPS (Metal) on Mac vs CUDA on Windows/NVIDIA. Device string differs.

## Status
✅ Deep-dive complete — `example.py` (list models + Inference API + local pipeline) and
`tests/` (4 mocked, 1 opt-in live) on Python 3.12. Add `HF_TOKEN` for Inference API calls.
