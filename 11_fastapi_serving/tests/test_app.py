"""Tests for 11_fastapi_serving/app.py — uses FastAPI TestClient, no API key needed."""

import os
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")

import app as app_module  # noqa: E402
from app import app  # noqa: E402

client = TestClient(app)


# ── helpers ───────────────────────────────────────────────────────────────────


def _mock_anthropic_response(
    text: str = "Paris is the capital of France.",
) -> MagicMock:
    content_block = MagicMock()
    content_block.text = text
    usage = MagicMock()
    usage.input_tokens = 10
    usage.output_tokens = 8
    resp = MagicMock()
    resp.content = [content_block]
    resp.model = "claude-haiku-4-5-20251001"
    resp.usage = usage
    return resp


# ── health endpoint ───────────────────────────────────────────────────────────


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ── /chat endpoint ────────────────────────────────────────────────────────────


def test_chat_returns_reply():
    mock_anthropic = MagicMock()
    mock_anthropic.messages.create.return_value = _mock_anthropic_response()

    with patch.object(app_module, "get_client", return_value=mock_anthropic):
        response = client.post(
            "/chat", json={"message": "What is the capital of France?"}
        )

    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert data["reply"] == "Paris is the capital of France."
    assert "input_tokens" in data
    assert "output_tokens" in data


def test_chat_missing_message_returns_422():
    response = client.post("/chat", json={})
    assert response.status_code == 422


def test_chat_custom_system_prompt():
    mock_anthropic = MagicMock()
    mock_anthropic.messages.create.return_value = _mock_anthropic_response("Oui.")

    with patch.object(app_module, "get_client", return_value=mock_anthropic):
        response = client.post(
            "/chat",
            json={
                "message": "Capital?",
                "system": "Reply in French only.",
            },
        )

    assert response.status_code == 200
    _, kwargs = mock_anthropic.messages.create.call_args
    assert kwargs.get("system") == "Reply in French only."


# ── /chat/stream endpoint ─────────────────────────────────────────────────────


def test_chat_stream_returns_sse_content():
    from contextlib import contextmanager

    @contextmanager
    def fake_stream(*args, **kwargs):
        class FakeStream:
            @property
            def text_stream(self):
                yield "1\n"
                yield "2\n"
                yield "3\n"

        yield FakeStream()

    mock_anthropic = MagicMock()
    mock_anthropic.messages.stream = fake_stream

    with patch.object(app_module, "get_client", return_value=mock_anthropic):
        response = client.post("/chat/stream", json={"message": "Count to 3."})

    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    body = response.text
    assert "data:" in body
    assert "[DONE]" in body
