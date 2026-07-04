# 16 — Grok (xAI)

## What it is
Grok is xAI's (Elon Musk) model family, served via an **OpenAI-compatible** API. Note the
spelling: **Grok** = xAI. Never "Groq" (that's a different, unrelated hardware company).

## WHY reach for it
- Real-time/X-flavored knowledge and a distinct style.
- OpenAI-compatible → reuse `03_openai_sdk` code with a new `base_url` + key.
- Easy to add to an OpenRouter (`04`) A/B set.

## WHEN NOT to
- You need Claude-grade reasoning → `01`. Best coding/agents → GPT-5.5 (`03`).

## Install
```
cd 16_grok_xai
uv init
uv python pin 3.12
uv add openai python-dotenv
cp ../.env.example .env
```
Use the OpenAI SDK with `base_url="https://api.x.ai/v1"` and `XAI_API_KEY`.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| Via OpenRouter (`04`) | One key, many models | 1 |
| Other providers | Different strengths | 1 |

## Mac vs Windows
No difference.

## Status
⬜ Scaffold only.
