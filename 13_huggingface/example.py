"""
13_huggingface — HuggingFace Hub Inference API + model discovery
================================================================

WHY reach for it
- 1,000,000+ models on the Hub; Inference API lets you call hosted models with one token.
- Zero local download for hosted inference — good for prototyping before committing to
  a model size and spending disk/RAM.
- Same client (`InferenceClient`) handles text-gen, chat, image, audio → one import.
- `transformers.pipeline` gives a local fallback when you do want on-device inference.

WHEN NOT to
- You need frontier quality + latency → Anthropic/OpenAI/Gemini are more reliable.
- Free tier is rate-limited; paid HF Pro or private endpoints for production.
- Local heavy models (70B+) → folder 09 (Ollama MLX) fits better on 24 GB RAM.

Mac / Apple Silicon note
- `pipeline(..., device="mps")` uses Metal; faster than CPU for small models.
- `device_map="auto"` still maps to MPS on Mac.
- Never use `device="cuda"` on Mac.

Switching cost
- HF Inference API → OpenAI-compatible endpoint: change base_url + auth header pattern.
  InferenceClient also exposes chat_completion() which follows OpenAI chat format.
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from huggingface_hub import InferenceClient, list_models

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN", "")

TEXT_GEN_MODEL = "HuggingFaceH4/zephyr-7b-beta"
CHAT_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"


def demo_list_models(limit: int = 5) -> list[str]:
    """List top text-generation models by likes — no token needed."""
    models = list(
        list_models(
            filter="text-generation",
            sort="likes",
            limit=limit,
        )
    )
    return [m.id for m in models]


def demo_chat_completion(client: InferenceClient | None = None) -> str:
    """Chat completion via HF Inference API — uses OpenAI-compatible chat format."""
    c = client or InferenceClient(token=HF_TOKEN)
    response = c.chat_completion(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a concise assistant. Reply in one sentence.",
            },
            {"role": "user", "content": "What is HuggingFace?"},
        ],
        max_tokens=128,
    )
    return response.choices[0].message.content or ""


def demo_text_generation(client: InferenceClient | None = None) -> str:
    """Raw text generation (no chat template) — useful for completion-style models."""
    c = client or InferenceClient(token=HF_TOKEN)
    result = c.text_generation(
        "The capital of Japan is",
        model=TEXT_GEN_MODEL,
        max_new_tokens=32,
        do_sample=False,
    )
    return result if isinstance(result, str) else str(result)


def _get_torch_device() -> str:
    """Return 'mps' on Apple Silicon, 'cpu' otherwise. Isolated for testability."""
    import torch

    return "mps" if torch.backends.mps.is_available() else "cpu"


def _load_sentiment_pipeline(device: str):
    """Load transformers sentiment pipeline. Isolated for testability."""
    from transformers import pipeline

    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=device,
    )


def demo_local_pipeline(text: str = "I love building AI projects on Mac!") -> dict:
    """
    Local sentiment analysis with transformers.pipeline — downloads a tiny model (~67 MB).
    Uses MPS (Metal) on Apple Silicon for acceleration.
    """
    device = _get_torch_device()
    classifier = _load_sentiment_pipeline(device)
    results = classifier(text)
    return results[0] if results else {}


def main() -> None:
    target = sys.argv[1] if len(sys.argv) > 1 else "all"

    if target in ("all", "list"):
        print("\n=== Top text-gen models ===")
        for m in demo_list_models():
            print(f"  {m}")

    if target in ("all", "chat"):
        print("\n=== Chat completion ===")
        print(demo_chat_completion())

    if target in ("all", "generate"):
        print("\n=== Text generation ===")
        print(demo_text_generation())

    if target in ("all", "pipeline"):
        print("\n=== Local pipeline (downloads ~67 MB first run) ===")
        result = demo_local_pipeline()
        print(f"  label={result.get('label')}, score={result.get('score', 0):.3f}")


if __name__ == "__main__":
    main()
