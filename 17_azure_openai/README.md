# 17 — Azure OpenAI (lowest priority)

## What it is
OpenAI models (GPT family) served through Microsoft Azure with enterprise controls:
private networking, data residency, compliance, RBAC. Same models, enterprise wrapper.

## WHY reach for it
- Required in some corporate/regulated environments.
- Data-residency and compliance guarantees direct OpenAI can't always give.

## WHEN NOT to
- Personal projects → direct OpenAI (`03`) or OpenRouter (`04`) is simpler and cheaper.
- This is the **lowest priority** folder in the toolkit — only when a job demands it.

## Install
```
cd 17_azure_openai
uv init --python 3.12
uv add openai python-dotenv
uv add --dev pytest
cp ../.env.example .env
```
Required `.env` keys: `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`,
`AZURE_OPENAI_DEPLOYMENT` (your deployment name, e.g. `gpt-4o-mini`),
`AZURE_OPENAI_API_VERSION` (e.g. `2025-01-01-preview`).

## Run
```
uv run python example.py          # all three demos (needs Azure keys)
uv run python example.py basic    # or: streaming | system
uv run pytest                     # 4 mocked + 1 skipped (no key)
```
Uses `AzureOpenAI(azure_endpoint, api_key, api_version)` — all chat/stream patterns
identical to openai.OpenAI once the client is constructed.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| Direct OpenAI (`03`) | Simpler, no compliance layer | 2 |
| AWS Bedrock | Different cloud, incl. Claude | 3 |

## Mac vs Windows
SDK identical; only `az` CLI setup differs (Homebrew on Mac).

## Status
✅ Deep-dive complete — `example.py` (basic + streaming + system prompt) and `tests/`
(4 mocked, 1 opt-in live) on Python 3.12. Add Azure keys to `.env` to run live.
