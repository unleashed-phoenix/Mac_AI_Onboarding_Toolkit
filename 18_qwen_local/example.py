"""
18_qwen_local — Qwen local models via the ollama Python client
==============================================================

WHY reach for it
- Free, private, offline — no API key, no per-token cost, nothing leaves the machine.
- `qwen2.5-coder:14b` (~9 GB Q4) is the daily coding driver on this M4 Pro (24 GB RAM).
- The `ollama` Python package gives a clean typed API; `ollama.chat()` mirrors the
  openai.chat pattern but is native (no HTTP shim to reason about).

Difference from folder 09 (ollama_mlx_local)
- Folder 09 uses the OpenAI-compatible HTTP endpoint (base_url swap on `openai` SDK).
- This folder uses the `ollama` Python package directly: typed responses, no requests/httpx,
  and access to Ollama-specific fields (eval_count, load_duration, etc.).
- Both work; pick based on whether you want the OpenAI shim (09) or the native client (18).

Models pre-installed on this Mac
- qwen2.5-coder:14b   (~9 GB)  — daily coding, fastest for code tasks
- gemma4:12b          (~7.6 GB) — general reasoning
- nomic-embed-text    (~0.3 GB) — embeddings for RAG

24 GB RAM guidance — fits comfortably: 12–14B Q4. Do NOT install 70B+.
"""

from __future__ import annotations

import os
import sys

import ollama
from dotenv import load_dotenv

load_dotenv()

CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "qwen2.5-coder:14b")
EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")


def _ollama_running() -> bool:
    """Return True if Ollama server is reachable."""
    import urllib.error
    import urllib.request

    try:
        urllib.request.urlopen("http://localhost:11434", timeout=2)
        return True
    except (urllib.error.URLError, OSError):
        return False


def demo_basic(client: ollama.Client | None = None) -> str:
    """Single chat completion using the ollama Python client."""
    c = client or ollama.Client()
    response = c.chat(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "user",
                "content": "Write a Python one-liner that reverses a string. Reply with just the code.",
            }
        ],
    )
    return response.message.content or ""


def demo_streaming(client: ollama.Client | None = None) -> str:
    """Streaming chat — yields tokens as they arrive."""
    c = client or ollama.Client()
    chunks: list[str] = []
    stream = c.chat(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "user",
                "content": "Explain list comprehensions in Python in 2 sentences.",
            }
        ],
        stream=True,
    )
    for chunk in stream:
        token = chunk.message.content or ""
        if token:
            chunks.append(token)
            print(token, end="", flush=True)
    print()
    return "".join(chunks)


def demo_embeddings(client: ollama.Client | None = None) -> list[float]:
    """Text embedding with nomic-embed-text — useful for RAG (see folder 08)."""
    c = client or ollama.Client()
    response = c.embed(model=EMBED_MODEL, input="Hello, Qwen!")
    return response.embeddings[0]


def main() -> None:
    target = sys.argv[1] if len(sys.argv) > 1 else "all"

    if not _ollama_running():
        print("Ollama not running. Start with: ollama serve")
        sys.exit(1)

    if target in ("all", "basic"):
        print("\n=== Basic ===")
        print(demo_basic())

    if target in ("all", "streaming"):
        print("\n=== Streaming ===")
        demo_streaming()

    if target in ("all", "embeddings"):
        print("\n=== Embeddings ===")
        vec = demo_embeddings()
        print(f"Vector dims: {len(vec)}, first 5: {vec[:5]}")


if __name__ == "__main__":
    main()
