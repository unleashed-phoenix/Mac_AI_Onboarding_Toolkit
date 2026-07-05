# 10 — Structured Outputs

## What it is
Techniques to force an LLM to return **valid, typed** data (JSON matching a schema),
usually via Pydantic models + provider "structured output" / "tool" modes.

## WHY reach for it
- Stop parsing free-text; get objects you can trust.
- Fewer retries, safer pipelines, easy validation.
- Works across providers (native JSON mode or Instructor library).

## WHEN NOT to
- Pure prose generation → no schema needed.

## Install
```
cd 10_structured_outputs
uv init --python 3.12
uv add pydantic instructor anthropic openai python-dotenv
uv add --dev pytest
cp ../.env.example .env
```

## Run
```
uv run python example.py          # all three demos
uv run python example.py native   # or: instructor | list
uv run pytest                     # 4 mocked + 1 skipped (no key)
```
`example.py` shows: (1) native Anthropic tool-use → Pydantic parse, (2) Instructor
single-item extraction with auto-retry, (3) Instructor list extraction.

## Pattern
Define a `pydantic.BaseModel`, pass it as the response schema (native structured output on
Claude/GPT/Gemini) or wrap the client with `instructor` for provider-agnostic parsing +
automatic re-ask on validation failure.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| Native JSON mode | Provider-specific | 1 |
| Instructor lib | Uniform across providers | 1 |
| Outlines / guidance | Local-model constrained decoding | 3 |

## Mac vs Windows
No difference.

## Status
✅ Deep-dive complete — `example.py` (native tool-use + Instructor) and `tests/`
(4 mocked, 1 opt-in live) on Python 3.12. Add `ANTHROPIC_API_KEY` to run live.
