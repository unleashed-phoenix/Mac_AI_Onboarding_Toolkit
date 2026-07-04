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
uv init
uv python pin 3.12
uv add streamlit gradio python-dotenv
cp ../.env.example .env
```
Run: `uv run streamlit run app.py`  or  `uv run python gradio_app.py`.

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
⬜ Scaffold only.
