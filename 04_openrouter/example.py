"""04 — OpenRouter: a minimal, runnable reference.

WHY this layer: one API key, one bill, hundreds of models. A/B test Claude vs GPT vs
Gemini with a one-line model-string change. Auto-fallback if a provider is rate-limited.
Uses the OpenAI SDK — only the client init changes. Switching cost back to direct SDK = 1.
See ../compatibility_matrix.md.

OpenRouter model strings use provider/model slugs:
  anthropic/claude-haiku-4-5      openai/gpt-4o-mini
  google/gemini-2.0-flash         meta-llama/llama-3-8b-instruct

Two demos:
  1. basic       — single call, model is a parameter (default: claude-haiku-4-5)
  2. ab_compare  — same prompt → two models side-by-side (the core A/B value prop)

Run:
  uv run python example.py            # all demos
  uv run python example.py basic      # or: ab_compare
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

MODEL_A = "anthropic/claude-haiku-4-5"
MODEL_B = "openai/gpt-4o-mini"

MAX_TOKENS = 512


def _client(client: OpenAI | None = None) -> OpenAI:
    return client or OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=os.environ["OPENROUTER_API_KEY"],
    )


def demo_basic(model: str = MODEL_A, client: OpenAI | None = None) -> str:
    """Single call through OpenRouter — model is a parameter, swap to compare."""
    client = _client(client)
    response = client.chat.completions.create(
        model=model,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": "In one sentence, what is OpenRouter?"}],
    )
    text = response.choices[0].message.content or ""
    print(f"[{model}] {text}")
    return text


def demo_ab_compare(client: OpenAI | None = None) -> dict[str, str]:
    """Call two models with the same prompt and compare replies side-by-side."""
    client = _client(client)
    prompt = "Name one advantage of using a multi-model API gateway."
    results: dict[str, str] = {}
    for model in (MODEL_A, MODEL_B):
        response = client.chat.completions.create(
            model=model,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.choices[0].message.content or ""
        results[model] = text
        print(f"[{model}]\n  {text}\n")
    return results


DEMOS = {
    "basic": demo_basic,
    "ab_compare": demo_ab_compare,
}


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    if not os.getenv("OPENROUTER_API_KEY"):
        print(
            "OPENROUTER_API_KEY is not set.\n"
            "  1. cp ../.env.example .env\n"
            "  2. add your key: OPENROUTER_API_KEY=sk-or-...\n"
            "  3. re-run:       uv run python example.py",
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
