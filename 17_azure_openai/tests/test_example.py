"""Tests for 17_azure_openai/example.py — all mocked, no Azure keys needed."""

import os
from contextlib import contextmanager
from unittest.mock import MagicMock

import pytest

os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "https://placeholder.openai.azure.com/")
os.environ.setdefault("AZURE_OPENAI_API_KEY", "test-key")
os.environ.setdefault("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
os.environ.setdefault("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")

import example  # noqa: E402


def _make_mock_client(content: str) -> MagicMock:
    msg = MagicMock()
    msg.content = content
    choice = MagicMock()
    choice.message = msg
    resp = MagicMock()
    resp.choices = [choice]
    client = MagicMock()
    client.chat.completions.create.return_value = resp
    return client


def test_demo_basic_returns_string():
    client = _make_mock_client("Paris is the capital of France.")
    result = example.demo_basic(client=client)
    assert result == "Paris is the capital of France."
    client.chat.completions.create.assert_called_once()


def test_demo_streaming_returns_string():
    chunk = MagicMock()
    chunk.choices = [MagicMock()]
    chunk.choices[0].delta.content = "Berlin\nParis\nRome"

    @contextmanager
    def fake_stream(*args, **kwargs):
        yield iter([chunk])

    client = MagicMock()
    client.chat.completions.stream = fake_stream
    result = example.demo_streaming(client=client)
    assert "Berlin" in result


def test_demo_system_prompt_returns_string():
    client = _make_mock_client(
        "Azure OpenAI Service provides REST API access to OpenAI models."
    )
    result = example.demo_system_prompt(client=client)
    assert isinstance(result, str)
    assert len(result) > 0


def test_deployment_env_var_used():
    """AzureOpenAI uses DEPLOYMENT, not a model slug — verify env var is read."""
    assert example.DEPLOYMENT == "gpt-4o-mini"


@pytest.mark.skipif(
    not os.getenv("AZURE_OPENAI_API_KEY")
    or os.getenv("AZURE_OPENAI_API_KEY") == "test-key",
    reason="AZURE_OPENAI_API_KEY not set to a real key",
)
def test_live_basic():
    result = example.demo_basic()
    assert isinstance(result, str)
    assert len(result) > 0
