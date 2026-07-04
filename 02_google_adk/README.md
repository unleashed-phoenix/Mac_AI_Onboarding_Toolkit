# 02 — Google ADK (Agent Development Kit)

## What it is
Google's framework for building Gemini-powered agents with tools, sessions, and
multi-agent orchestration. Pairs with Gemini 3.5 (Pro = best multimodal, Flash = fastest).

## WHY reach for it
- Tight Gemini integration + huge context windows.
- Strong multimodal (image/audio/video) handling.
- Good when you're already in Google Cloud / Vertex.

## WHEN NOT to
- Non-Google models → LangGraph (`06`) or CrewAI (`07`) are more model-agnostic.
- Simple one-shot calls → just the Gemini SDK, no ADK.

## Install
```
cd 02_google_adk
uv init
uv python pin 3.12
uv add google-adk python-dotenv
cp ../.env.example .env
```
Set `GOOGLE_API_KEY` in `.env`.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| LangGraph (`06`) | Model-agnostic graphs | 3 |
| CrewAI (`07`) | Role-based, less Google-native | 3 |
| Raw Gemini SDK | No agent scaffolding | 2 |

## Mac vs Windows
No difference for the SDK. For Vertex, `gcloud` CLI installs via Homebrew on Mac.

## Status
⬜ Scaffold only.
