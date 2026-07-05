"""
17_azure_openai — Azure OpenAI via AzureOpenAI client
======================================================

WHY reach for it
- Enterprise / regulated orgs that must keep data inside Azure's compliance boundary.
- Private endpoints, VNet integration, content filtering, Azure AD auth — all Azure-native.
- AzureOpenAI class is in the same `openai` package; no new SDK to learn.

Key differences from openai.OpenAI
- Need azure_endpoint (not base_url), api_version, and a deployment_name (not model slug).
  The deployment name is what YOU named the model in Azure AI Studio, e.g. "gpt-4o".
- Auth: api_key OR DefaultAzureCredential (keyless, managed identity).

WHEN NOT to
- Personal / startup projects → direct OpenAI (03) is simpler; no Azure subscription needed.
- Multi-provider A/B → OpenRouter (04) is easier.

Switching cost from openai.OpenAI (03)
- 2: swap class + add endpoint + api_version. All chat/stream/tool code is identical.

Required .env keys
- AZURE_OPENAI_ENDPOINT   e.g. https://my-resource.openai.azure.com/
- AZURE_OPENAI_API_KEY
- AZURE_OPENAI_DEPLOYMENT  your deployment name, e.g. "gpt-4o-mini"
- AZURE_OPENAI_API_VERSION e.g. 2025-01-01-preview
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

AZURE_ENDPOINT = os.getenv(
    "AZURE_OPENAI_ENDPOINT", "https://placeholder.openai.azure.com/"
)
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")


def _client(client: AzureOpenAI | None) -> AzureOpenAI:
    if client is not None:
        return client
    return AzureOpenAI(
        azure_endpoint=AZURE_ENDPOINT,
        api_key=AZURE_API_KEY,
        api_version=API_VERSION,
    )


def demo_basic(client: AzureOpenAI | None = None) -> str:
    """Single chat completion using the Azure deployment."""
    c = _client(client)
    response = c.chat.completions.create(
        model=DEPLOYMENT,
        max_tokens=256,
        messages=[
            {"role": "user", "content": "What is the capital of France? One sentence."}
        ],
    )
    return response.choices[0].message.content or ""


def demo_streaming(client: AzureOpenAI | None = None) -> str:
    """Streaming chat — same pattern as openai.OpenAI (03)."""
    c = _client(client)
    chunks: list[str] = []
    with c.chat.completions.stream(
        model=DEPLOYMENT,
        max_tokens=256,
        messages=[
            {"role": "user", "content": "List 3 European capitals, one per line."}
        ],
    ) as stream:
        for event in stream:
            delta = event.choices[0].delta.content if event.choices else None
            if delta:
                chunks.append(delta)
                print(delta, end="", flush=True)
    print()
    return "".join(chunks)


def demo_system_prompt(client: AzureOpenAI | None = None) -> str:
    """Demonstrate system prompt + user message pattern."""
    c = _client(client)
    response = c.chat.completions.create(
        model=DEPLOYMENT,
        max_tokens=256,
        messages=[
            {
                "role": "system",
                "content": "You are a concise assistant. Reply in ≤2 sentences.",
            },
            {"role": "user", "content": "Explain what Azure OpenAI Service is."},
        ],
    )
    return response.choices[0].message.content or ""


def main() -> None:
    target = sys.argv[1] if len(sys.argv) > 1 else "all"

    if target in ("all", "basic"):
        print("\n=== Basic ===")
        print(demo_basic())

    if target in ("all", "streaming"):
        print("\n=== Streaming ===")
        demo_streaming()

    if target in ("all", "system"):
        print("\n=== System prompt ===")
        print(demo_system_prompt())


if __name__ == "__main__":
    main()
