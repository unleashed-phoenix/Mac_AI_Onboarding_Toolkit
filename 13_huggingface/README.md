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
uv init
uv python pin 3.12
uv add huggingface_hub transformers datasets python-dotenv
cp ../.env.example .env
```
Set `HF_TOKEN`. Login: `uv run huggingface-cli login`.

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
⬜ Scaffold only.
