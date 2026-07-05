"""02 — Google ADK (Agent Development Kit): a minimal, runnable reference.

WHY this layer: ADK wraps Gemini with agent state, session management, and automatic
tool dispatch — you don't need to handle tool round-trips manually (contrast with 01).
If you don't need persistent sessions or multi-turn agents, raw google-generativeai
is 50% less code. Switching cost to LangGraph = 3 (different graph model).
See ../compatibility_matrix.md.

Two demos:
  1. basic     — a single-turn agent with no tools
  2. tool_use  — ADK automatically dispatches get_weather and returns the final answer

Run:
  uv run python example.py            # all demos
  uv run python example.py basic      # or: tool_use
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()

SMOKE_MODEL = "gemini-2.0-flash"
QUALITY_MODEL = "gemini-2.5-pro"
MODEL = SMOKE_MODEL

MAX_TOKENS = 1024


def _run_agent(agent: Agent, prompt: str) -> str:
    """Run one turn through an ADK agent and return the text reply."""
    session_service = InMemorySessionService()
    runner = Runner(app_name="demo", agent=agent, session_service=session_service)
    session = session_service.create_session_sync(app_name="demo", user_id="user1")
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    text_parts: list[str] = []
    for event in runner.run(
        user_id="user1", session_id=session.id, new_message=message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    text_parts.append(part.text)
    return "\n".join(text_parts)


def demo_basic() -> str:
    """Single-turn agent with no tools — shows the minimal ADK setup."""
    agent = Agent(
        name="basic_agent",
        model=MODEL,
        instruction="You are a helpful assistant. Answer in one sentence.",
    )
    reply = _run_agent(agent, "In one sentence, what is the Google ADK?")
    print(reply)
    return reply


# ---- Tool use ------------------------------------------------------------------


def get_weather(location: str) -> dict:
    """Stub weather tool. A real impl would call a weather API.

    Args:
        location: City name, e.g. 'Paris'.

    Returns:
        A dict with temperature and condition.
    """
    return {"location": location, "temperature": 22, "condition": "sunny"}


def demo_tool_use() -> str:
    """ADK agent with get_weather — ADK handles tool dispatch automatically."""
    agent = Agent(
        name="weather_agent",
        model=MODEL,
        instruction="You are a weather assistant. Use get_weather when asked about weather.",
        tools=[get_weather],
    )
    reply = _run_agent(agent, "What's the weather in Tokyo right now?")
    print(reply)
    return reply


DEMOS = {
    "basic": demo_basic,
    "tool_use": demo_tool_use,
}


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    if not os.getenv("GOOGLE_API_KEY"):
        print(
            "GOOGLE_API_KEY is not set.\n"
            "  1. cp ../.env.example .env\n"
            "  2. add your key: GOOGLE_API_KEY=AIza...\n"
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
