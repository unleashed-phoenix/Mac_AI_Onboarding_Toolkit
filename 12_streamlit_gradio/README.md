# 12 — Streamlit + Gradio

## What it is
Two Python-only ways to build a UI for an AI app with zero front-end code. Streamlit =
data apps/dashboards; Gradio = quick ML/chat demos (and free HF Spaces hosting).

## WHY reach for it
- Ship a usable demo in minutes, all in Python (Python > JS here, per project rule).
- Great for internal tools and stakeholder demos.
- Gradio deploys free to Hugging Face Spaces (`13`).

## WHEN NOT to
- Production consumer app → real front end + FastAPI (`11`).

## Install
```
cd 12_streamlit_gradio
uv init --python 3.12
uv add streamlit gradio anthropic python-dotenv
uv add --dev pytest
cp ../.env.example .env
```

## Run
```
uv run streamlit run streamlit_app.py   # Streamlit chat (opens browser)
uv run python gradio_app.py             # Gradio chat (prints URL)
uv run pytest                           # tests LLM helper only (UI can't be pytest'd)
```
UI files can't be unit-tested without a headless browser; `tests/` covers `example.py`
(the shared LLM helper that both UI files import).

## Which one
Dashboards, multi-widget data apps → Streamlit. Chatbots, model demos, shareable Spaces →
Gradio.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| Reflex | Full-stack Python | 3 |
| NiceGUI | Richer widgets | 3 |

## Mac vs Windows
No difference.

## Status
✅ Deep-dive complete — `streamlit_app.py`, `gradio_app.py`, `example.py` (shared LLM
helper), and `tests/` (5 mocked, 1 opt-in live) on Python 3.12. Add `ANTHROPIC_API_KEY`
to run live. Note: UI frames themselves cannot be pytest'd without a headless browser.
