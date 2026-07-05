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
uv init --python 3.12
uv add fastapi "uvicorn[standard]" anthropic python-dotenv
uv add --dev pytest httpx
cp ../.env.example .env
```

## Run
```
uv run uvicorn app:app --reload    # starts server at http://127.0.0.1:8000
uv run pytest                      # 5 mocked tests (no server, no key needed)
```
Open `http://127.0.0.1:8000/docs` for automatic Swagger UI. Test endpoints with Bruno using `api.bru`.

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
✅ Deep-dive complete — `app.py` (GET /health, POST /chat, POST /chat/stream SSE),
`api.bru` Bruno collection, and `tests/test_app.py` (5 mocked) on Python 3.12.
Add `ANTHROPIC_API_KEY` to run live.
