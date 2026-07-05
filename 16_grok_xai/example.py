"""
16_grok_xai — xAI Grok via OpenAI-compatible endpoint
=======================================================

WHY reach for it
- xAI (Elon Musk's lab) exposes Grok models with an OpenAI-compatible API → zero new
  SDK needed, swap base_url + key and every OpenAI pattern from folder 03 works as-is.
- Grok has access to real-time X/Twitter data (on paid tiers), making it strong for
  current-events tasks other models can't do from training data alone.

NOT to confuse with
- Groq (groq.com) — a different company, ultra-fast inference chip, also OAI-compatible.
  Swap: base_url="https://api.groq.com/openai/v1", key=GROQ_API_KEY, model="llama-3.3-70b-versatile".

Switching cost from OpenAI (03)
- 1: change base_url + key env var + model slug. All chat/stream/tool patterns identical.
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

XAI_API_KEY = os.getenv("XAI_API_KEY", "")
BASE_URL = "https://api.x.ai/v1"
MODEL = "grok-3-mini"  # cheaper smoke model; swap to "grok-3" for quality


def _client(client: OpenAI | None) -> OpenAI:
    if client is not None:
        return client
    return OpenAI(base_url=BASE_URL, api_key=XAI_API_KEY)


def demo_basic(client: OpenAI | None = None) -> str:
    """Single chat completion — identical to openai SDK usage."""
    c = _client(client)
    response = c.chat.completions.create(
        model=MODEL,
        max_tokens=256,
        messages=[{"role": "user", "content": "What is 7 × 6? Reply in one sentence."}],
    )
    return response.choices[0].message.content or ""


def demo_streaming(client: OpenAI | None = None) -> str:
    """Streaming chat — yields tokens as they arrive."""
    c = _client(client)
    chunks: list[str] = []
    with c.chat.completions.stream(
        model=MODEL,
        max_tokens=256,
        messages=[{"role": "user", "content": "Count from 1 to 5 slowly."}],
    ) as stream:
        for event in stream:
            delta = event.choices[0].delta.content if event.choices else None
            if delta:
                chunks.append(delta)
                print(delta, end="", flush=True)
    print()
    return "".join(chunks)


def demo_tool_use(client: OpenAI | None = None) -> str:
    """Tool-use (function calling) — same JSON schema as OpenAI."""
    import json

    c = _client(client)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather for a location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "City name"},
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    response = c.chat.completions.create(
        model=MODEL,
        max_tokens=256,
        tools=tools,
        messages=[{"role": "user", "content": "What's the weather in San Francisco?"}],
    )

    msg = response.choices[0].message
    if msg.tool_calls:
        call = msg.tool_calls[0]
        args = json.loads(call.function.arguments)
        fake_weather = f"72°F and foggy in {args['location']}."
        return fake_weather

    return msg.content or ""


def main() -> None:
    target = sys.argv[1] if len(sys.argv) > 1 else "all"

    if target in ("all", "basic"):
        print("\n=== Basic ===")
        print(demo_basic())

    if target in ("all", "streaming"):
        print("\n=== Streaming ===")
        demo_streaming()

    if target in ("all", "tools"):
        print("\n=== Tool use ===")
        print(demo_tool_use())


if __name__ == "__main__":
    main()
