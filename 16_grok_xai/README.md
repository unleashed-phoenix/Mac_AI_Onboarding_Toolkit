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
uv init --python 3.12
uv add openai python-dotenv
uv add --dev pytest
cp ../.env.example .env
```
Use the OpenAI SDK with `base_url="https://api.x.ai/v1"` and `XAI_API_KEY`.

## Run
```
uv run python example.py          # all three demos
uv run python example.py basic    # or: streaming | tools
uv run pytest                     # 3 mocked + 1 skipped (no key)
```
Same three demos as folder 03 (basic + streaming + tool-use) — identical code, different
`base_url` + key. Switching cost from OpenAI to xAI: 1 (swap two env vars).

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| Via OpenRouter (`04`) | One key, many models | 1 |
| Other providers | Different strengths | 1 |

## Mac vs Windows
No difference.

## Status
✅ Deep-dive complete — `example.py` (basic + streaming + tool-use) and `tests/`
(3 mocked, 1 opt-in live) on Python 3.12. Add `XAI_API_KEY` to run live.
