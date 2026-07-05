"""Tests for 13_huggingface/example.py — all mocked, no HF_TOKEN or downloads needed."""

import os
from unittest.mock import MagicMock, patch

import pytest

os.environ.setdefault("HF_TOKEN", "test-token")

import example  # noqa: E402

_HAS_TOKEN = bool(os.getenv("HF_TOKEN")) and os.getenv("HF_TOKEN") != "test-token"


# ── unit tests ────────────────────────────────────────────────────────────────


def test_demo_list_models_returns_list_of_strings():
    fake_model = MagicMock()
    fake_model.id = "meta-llama/Llama-3-8B"
    with patch("example.list_models", return_value=iter([fake_model, fake_model])):
        result = example.demo_list_models(limit=2)
    assert isinstance(result, list)
    assert all(isinstance(m, str) for m in result)
    assert "meta-llama/Llama-3-8B" in result


def test_demo_chat_completion_returns_string():
    msg = MagicMock()
    msg.content = "HuggingFace is an AI platform with 1M+ models."
    choice = MagicMock()
    choice.message = msg
    resp = MagicMock()
    resp.choices = [choice]

    mock_client = MagicMock()
    mock_client.chat_completion.return_value = resp
    result = example.demo_chat_completion(client=mock_client)
    assert result == "HuggingFace is an AI platform with 1M+ models."
    mock_client.chat_completion.assert_called_once()


def test_demo_text_generation_returns_string():
    mock_client = MagicMock()
    mock_client.text_generation.return_value = " Tokyo."
    result = example.demo_text_generation(client=mock_client)
    assert isinstance(result, str)
    mock_client.text_generation.assert_called_once()


def test_demo_local_pipeline_returns_dict():
    fake_result = [{"label": "POSITIVE", "score": 0.999}]
    with patch("example._get_torch_device", return_value="cpu"):
        with patch(
            "example._load_sentiment_pipeline", return_value=lambda x: fake_result
        ):
            result = example.demo_local_pipeline("I love this!")
    assert result["label"] == "POSITIVE"
    assert 0 <= result["score"] <= 1


# ── live (opt-in, requires HF_TOKEN + network) ────────────────────────────────


@pytest.mark.skipif(not _HAS_TOKEN, reason="HF_TOKEN not set to a real token")
def test_live_list_models():
    models = example.demo_list_models(limit=3)
    assert len(models) >= 1
    assert all("/" in m for m in models)
