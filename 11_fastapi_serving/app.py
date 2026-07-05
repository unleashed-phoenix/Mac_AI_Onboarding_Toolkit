"""
11_fastapi_serving — Serve an LLM as a REST API with FastAPI
============================================================

WHY reach for it
- You want other services, mobile apps, or teammates to call your LLM without touching
  your Python code — a standard HTTP endpoint is the universal interface.
- FastAPI gives OpenAPI docs for free (visit /docs after starting the server).
- Streaming via Server-Sent Events (SSE) lets the client render tokens progressively.

WHEN NOT to
- Quick internal demo → Streamlit/Gradio (12) is faster to stand up.
- Production scale → add auth, rate-limiting, and a proper ASGI deployment (Gunicorn
  + Uvicorn workers) or a managed platform (Railway, Fly.io, Modal).

Run
    uv run uvicorn app:app --reload

Test with Bruno
    Open api.bru collection in Bruno → send requests to http://127.0.0.1:8000

Endpoints
    GET  /health       — liveness check
    POST /chat         — synchronous chat response
    POST /chat/stream  — SSE streaming chat response
"""

from __future__ import annotations

import os
from typing import AsyncGenerator

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL = "claude-haiku-4-5-20251001"

app = FastAPI(title="LLM Chat API", version="1.0.0")
_anthropic_client: anthropic.Anthropic | None = None


def get_client() -> anthropic.Anthropic:
    global _anthropic_client
    if _anthropic_client is None:
        _anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _anthropic_client


# ── request / response models ─────────────────────────────────────────────────


class ChatRequest(BaseModel):
    message: str
    system: str = "You are a helpful assistant. Reply concisely."
    max_tokens: int = 512


class ChatResponse(BaseModel):
    reply: str
    model: str
    input_tokens: int
    output_tokens: int


# ── endpoints ─────────────────────────────────────────────────────────────────


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    """Synchronous chat — returns the full reply once generation is complete."""
    c = get_client()
    response = c.messages.create(
        model=MODEL,
        max_tokens=req.max_tokens,
        system=req.system,
        messages=[{"role": "user", "content": req.message}],
    )
    return ChatResponse(
        reply=response.content[0].text,
        model=response.model,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
    )


async def _sse_stream(
    req: ChatRequest, anth_client: anthropic.Anthropic
) -> AsyncGenerator[str, None]:
    """Yield SSE-formatted text chunks."""
    with anth_client.messages.stream(
        model=MODEL,
        max_tokens=req.max_tokens,
        system=req.system,
        messages=[{"role": "user", "content": req.message}],
    ) as stream:
        for text in stream.text_stream:
            yield f"data: {text}\n\n"
    yield "data: [DONE]\n\n"


@app.post("/chat/stream")
def chat_stream(req: ChatRequest) -> StreamingResponse:
    """Streaming chat via Server-Sent Events — renders tokens as they arrive."""
    return StreamingResponse(
        _sse_stream(req, get_client()),
        media_type="text/event-stream",
    )
