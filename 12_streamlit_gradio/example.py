"""
12_streamlit_gradio — Quick Chat UIs
=====================================

WHY reach for it
- Get a usable UI in ~10 lines without any HTML/CSS/JS.
- Streamlit: best for data apps, dashboards, multi-step forms with state.
- Gradio: best for demo interfaces, one-function UIs, fast HuggingFace Spaces deploys.

WHEN NOT to
- Production web app → FastAPI (11) + a real frontend.
- Embedded in a larger app → use a component library (React, Svelte).

Run
    uv run streamlit run streamlit_app.py  # opens browser automatically
    uv run python gradio_app.py            # prints local URL, opens browser

Testing note
- Streamlit and Gradio apps are UI frameworks; their render path cannot be
  unit-tested with pytest without a headless browser.
- This module (`example.py`) contains the shared LLM helper so it CAN be tested.
- The UI files (streamlit_app.py, gradio_app.py) import and call these helpers.

Switching cost Streamlit ↔ Gradio
- 2: they're different paradigms (Streamlit = script reruns; Gradio = event callbacks).
  Both call the same LLM helper below, so the logic is portable.
"""

from __future__ import annotations

import os

import anthropic
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL = "claude-haiku-4-5-20251001"
SYSTEM_PROMPT = "You are a helpful assistant. Be concise."


def chat_once(
    user_message: str,
    history: list[dict] | None = None,
    client: anthropic.Anthropic | None = None,
) -> str:
    """
    Send one user message (with optional prior history) and return the assistant reply.

    history format: [{"role": "user"|"assistant", "content": "..."}]
    """
    c = client or anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    messages = list(history or [])
    messages.append({"role": "user", "content": user_message})
    response = c.messages.create(
        model=MODEL,
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=messages,
    )
    return response.content[0].text


def chat_stream(
    user_message: str,
    history: list[dict] | None = None,
    client: anthropic.Anthropic | None = None,
):
    """
    Streaming version — yields text chunks.
    Used by Gradio's gr.ChatInterface with streaming=True.
    """
    c = client or anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    messages = list(history or [])
    messages.append({"role": "user", "content": user_message})
    with c.messages.stream(
        model=MODEL,
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=messages,
    ) as stream:
        yield from stream.text_stream
