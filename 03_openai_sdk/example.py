"""03 — OpenAI SDK: a minimal, runnable reference.

WHY this layer: the official SDK for GPT-5.5 (best coding/autonomous agents, July 2026).
Also the de-facto wire format — swap base_url + api_key to reach Ollama, Grok, or
OpenRouter without changing the rest of the code. Switching cost to OpenRouter = 1.
See ../compatibility_matrix.md.

PORTABILITY TRICK — reuse this exact file against other providers:
  Ollama (local):   OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
  Grok (xAI):       OpenAI(base_url="https://api.x.ai/v1", api_key=XAI_API_KEY)
  OpenRouter:       OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)

Three demos:
  1. basic      — client.chat.completions.create()
  2. streaming  — client.chat.completions.stream() context manager
  3. tool_use   — get_weather, full function-calling round-trip

Run:
  uv run python example.py            # all three
  uv run python example.py basic      # or: streaming | tool_use
"""

from __future__ import annotations

import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SMOKE_MODEL = "gpt-4o-mini"
QUALITY_MODEL = "gpt-5.5"
MODEL = SMOKE_MODEL

MAX_TOKENS = 1024


def _client(client: OpenAI | None = None) -> OpenAI:
    return client or OpenAI()


def demo_basic(client: OpenAI | None = None) -> str:
    """Single non-streaming call — most common pattern."""
    client = _client(client)
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "user", "content": "In one sentence, what is the OpenAI SDK?"}
        ],
    )
    text = response.choices[0].message.content or ""
    print(text)
    return text


def demo_streaming(client: OpenAI | None = None) -> str:
    """Token-by-token streaming via the .stream() context manager (openai >= 2.x)."""
    client = _client(client)
    print("Streaming: ", end="", flush=True)
    chunks: list[str] = []
    with client.chat.completions.stream(
        model=MODEL,
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


# ---- Tool use ------------------------------------------------------------------

WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a given location. Returns a short summary.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, e.g. 'Paris' or 'Tokyo'.",
                }
            },
            "required": ["location"],
        },
    },
}


def get_weather(location: str) -> str:
    """Local stub — keeps the demo deterministic without a real weather API."""
    return f"It is 22C and sunny in {location}."


def demo_tool_use(client: OpenAI | None = None) -> str:
    """Full function-calling round-trip: model calls get_weather, we run it, model replies."""
    client = _client(client)
    messages: list = [
        {"role": "user", "content": "What's the weather in Paris right now?"}
    ]

    first = client.chat.completions.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        tools=[WEATHER_TOOL],
        messages=messages,
    )

    if first.choices[0].finish_reason != "tool_calls":
        text = first.choices[0].message.content or ""
        print(text)
        return text

    tool_call = first.choices[0].message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    result = get_weather(**args)
    print(f"[tool] get_weather({args}) -> {result}")

    messages.append(first.choices[0].message)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result,
        }
    )

    final = client.chat.completions.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        tools=[WEATHER_TOOL],
        messages=messages,
    )
    text = final.choices[0].message.content or ""
    print(text)
    return text


DEMOS = {
    "basic": demo_basic,
    "streaming": demo_streaming,
    "tool_use": demo_tool_use,
}


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    if not os.getenv("OPENAI_API_KEY"):
        print(
            "OPENAI_API_KEY is not set.\n"
            "  1. cp ../.env.example .env\n"
            "  2. add your key: OPENAI_API_KEY=sk-...\n"
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
