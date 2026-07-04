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
uv init
uv python pin 3.12
uv add openai python-dotenv
cp ../.env.example .env
```
Use `AzureOpenAI(...)` with your endpoint, deployment name, and `api_version`. Auth via
Azure AD or key; store secrets in `.env`.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| Direct OpenAI (`03`) | Simpler, no compliance layer | 2 |
| AWS Bedrock | Different cloud, incl. Claude | 3 |

## Mac vs Windows
SDK identical; only `az` CLI setup differs (Homebrew on Mac).

## Status
⬜ Scaffold only — build last.
