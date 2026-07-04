# 11 — FastAPI Serving

## What it is
Wrap any model, agent, or RAG pipeline behind a fast, typed HTTP API using FastAPI +
Uvicorn. The standard way to turn a script into a service.

## WHY reach for it
- Async, high-performance, automatic OpenAPI docs + validation via Pydantic.
- Clean boundary between your AI logic and whatever calls it.
- Streams tokens over SSE/WebSocket.

## WHEN NOT to
- Just a demo UI → Streamlit/Gradio (`12`) is faster to stand up.

## Install
```
cd 11_fastapi_serving
uv init
uv python pin 3.12
uv add fastapi uvicorn pydantic python-dotenv
cp ../.env.example .env
```
Run: `uv run uvicorn app:app --reload`.

## Test the endpoints with Bruno
Use **Bruno** (installed via Brewfile) for API testing — never Postman. Save a `.bru`
collection alongside the code.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| Litestar | Similar, less common | 2 |
| Flask | Sync, older | 2 |

## Mac vs Windows
No difference.

## Status
⬜ Scaffold only.
