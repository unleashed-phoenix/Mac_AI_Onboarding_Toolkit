"""09 — Ollama + MLX Local: a minimal, runnable reference.

WHY this layer: free, private, offline. No per-token cost; data never leaves the machine.
Ollama exposes an OpenAI-compatible endpoint at localhost:11434, so the code from
03_openai_sdk works here unchanged — just swap base_url and api_key. MLX backend
on Apple Silicon gives fast, memory-efficient inference with no quality loss vs CUDA
at the same bit-width. Switching cost to cloud = 1 (change base_url + real api_key).
See ../compatibility_matrix.md.

Three demos:
  1. basic       — single call to qwen2.5-coder:14b via OpenAI-compatible endpoint
  2. streaming   — same model, token-by-token output
  3. embeddings  — nomic-embed-text via the same client (embeddings API)

Run:
  # Ensure Ollama is running: `ollama serve` (usually starts automatically)
  uv run python example.py            # all three
  uv run python example.py basic      # or: streaming | embeddings
"""

from __future__ import annotations

import os
import sys
import urllib.error
import urllib.request

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434") + "/v1"
CHAT_MODEL = "qwen2.5-coder:14b"
EMBED_MODEL = "nomic-embed-text"

MAX_TOKENS = 512


def _ollama_running() -> bool:
    """Return True if Ollama is reachable at its default endpoint."""
    try:
        urllib.request.urlopen(
            os.getenv("OLLAMA_HOST", "http://localhost:11434"), timeout=2
        )
        return True
    except (urllib.error.URLError, OSError):
        return False


def _client(client: OpenAI | None = None) -> OpenAI:
    return client or OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")


def demo_basic(client: OpenAI | None = None) -> str:
    """Single call to a local Ollama model — same API as 03_openai_sdk."""
    client = _client(client)
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": "In one sentence, what is Ollama?"}],
    )
    text = response.choices[0].message.content or ""
    print(text)
    return text


def demo_streaming(client: OpenAI | None = None) -> str:
    """Token-by-token streaming from a local model."""
    client = _client(client)
    print("Streaming: ", end="", flush=True)
    chunks: list[str] = []
    with client.chat.completions.stream(
        model=CHAT_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "user", "content": "Count from 1 to 5, one number per line."}
        ],
    ) as stream:
        for chunk in stream:
            delta = (
                chunk.choices[0].delta.content if chunk.choices[0].delta.content else ""
            )
            if delta:
                print(delta, end="", flush=True)
                chunks.append(delta)
    print()
    return "".join(chunks)


def demo_embeddings(client: OpenAI | None = None) -> list[float]:
    """Generate embeddings via nomic-embed-text — same client, same endpoint, different model.

    The embedding vector can be fed directly into ChromaDB (see 08_chromadb_rag).
    """
    client = _client(client)
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input="Hello, world!",
    )
    vector = response.data[0].embedding
    print(
        f"Embedding dim: {len(vector)}, first 5 values: {[round(v, 4) for v in vector[:5]]}"
    )
    return vector


DEMOS = {
    "basic": demo_basic,
    "streaming": demo_streaming,
    "embeddings": demo_embeddings,
}


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    if not _ollama_running():
        print(
            "Ollama is not running at localhost:11434.\n"
            "  Start it:  ollama serve\n"
            "  Or set:    OLLAMA_HOST=http://... in .env",
            file=sys.stderr,
        )
        return 1

    if argv:
        name = argv[0]
        if name not in DEMOS:
            print(
                f"Unknown demo '{name}'. Choose from: {', '.join(DEMOS)}",
                file=sys.stderr,
            )
            return 2
        DEMOS[name]()
        return 0

    for name, fn in DEMOS.items():
        print(f"\n=== {name} ===")
        fn()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
