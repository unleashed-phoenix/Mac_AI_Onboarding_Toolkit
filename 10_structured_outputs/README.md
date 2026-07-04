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
uv init
uv python pin 3.12
uv add pydantic instructor anthropic openai python-dotenv
cp ../.env.example .env
```

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
⬜ Scaffold only.
