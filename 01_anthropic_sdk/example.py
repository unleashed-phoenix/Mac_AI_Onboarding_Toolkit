"""01 — Anthropic SDK (Claude): a minimal, runnable reference.

WHY this layer: the first-party SDK is the lowest layer that works — max control,
fewest deps, native streaming + tool use. Reach higher (OpenRouter → LangChain →
LangGraph) only when raw calls get tangled. See ../compatibility_matrix.md.
Switching cost to OpenRouter ≈ 1: swap the client init, keep the call shape.

Three demos:
  1. basic     — a single Claude message
  2. streaming — token-by-token output
  3. tool_use  — full round-trip: model asks for a tool, we run it, model answers

Run:
  uv run python example.py            # runs all three
  uv run python example.py basic      # or: streaming | tool_use
"""

from __future__ import annotations

import os
import sys

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# Cheap model for these smoke demos — protects quota. Swap MODEL to QUALITY_MODEL
# (Opus 4.8) for real reasoning/agentic work; it's a one-line change.
SMOKE_MODEL = "claude-haiku-4-5-20251001"
QUALITY_MODEL = "claude-opus-4-8"
MODEL = SMOKE_MODEL

MAX_TOKENS = 1024


def _client(client: Anthropic | None = None) -> Anthropic:
    """Return the injected client (tests) or a real one (reads ANTHROPIC_API_KEY)."""
    return client or Anthropic()


def demo_basic(client: Anthropic | None = None) -> str:
    """A single, non-streaming Claude call. Returns the text reply."""
    client = _client(client)
    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "user", "content": "In one sentence, what is the Anthropic SDK?"}
        ],
    )
    text = message.content[0].text
    print(text)
    return text


def demo_streaming(client: Anthropic | None = None) -> str:
    """Stream the reply token-by-token. Returns the full text once complete."""
    client = _client(client)
    print("Streaming: ", end="", flush=True)
    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "user", "content": "Count from 1 to 5, one number per line."}
        ],
    ) as stream:
        for chunk in stream.text_stream:
            print(chunk, end="", flush=True)
        final = stream.get_final_message()
    print()  # newline after the stream finishes
    return "".join(block.text for block in final.content if block.type == "text")


# ---- Tool use ------------------------------------------------------------------

WEATHER_TOOL = {
    "name": "get_weather",
    "description": "Get the current weather for a given location. Returns a short summary.",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City name, e.g. 'Paris' or 'Tokyo'.",
            }
        },
        "required": ["location"],
    },
}


def get_weather(location: str) -> str:
    """Local stub. A real impl would call a weather API; canned so demos stay deterministic."""
    return f"It is 22C and sunny in {location}."


def demo_tool_use(client: Anthropic | None = None) -> str:
    """Full tool-use round-trip: model requests get_weather, we run it, model replies."""
    client = _client(client)
    messages: list[dict] = [
        {"role": "user", "content": "What's the weather in Paris right now?"}
    ]

    first = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        tools=[WEATHER_TOOL],
        messages=messages,
    )

    # The model may just answer without reaching for the tool.
    if first.stop_reason != "tool_use":
        text = "".join(b.text for b in first.content if b.type == "text")
        print(text)
        return text

    tool_use = next(b for b in first.content if b.type == "tool_use")
    result = get_weather(**tool_use.input)
    print(f"[tool] get_weather({tool_use.input}) -> {result}")

    # Echo the assistant's turn back, then hand it the tool result to compose a reply.
    messages.append({"role": "assistant", "content": first.content})
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": result,
                }
            ],
        }
    )

    final = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        tools=[WEATHER_TOOL],
        messages=messages,
    )
    text = "".join(b.text for b in final.content if b.type == "text")
    print(text)
    return text


DEMOS = {
    "basic": demo_basic,
    "streaming": demo_streaming,
    "tool_use": demo_tool_use,
}


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    if not os.getenv("ANTHROPIC_API_KEY"):
        print(
            "ANTHROPIC_API_KEY is not set.\n"
            "  1. cp ../.env.example .env\n"
            "  2. add your key:  ANTHROPIC_API_KEY=sk-ant-...\n"
            "  3. re-run:        uv run python example.py",
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
