"""Tests for 10_structured_outputs/example.py — all mocked, no API key needed."""

import os

import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")

import example  # noqa: E402


# ── helpers ──────────────────────────────────────────────────────────────────


def _make_native_mock(mocker_or_mock):
    """Return a mock Anthropic client that returns a valid WeatherReport tool_use block."""
    from unittest.mock import MagicMock

    tool_block = MagicMock()
    tool_block.type = "tool_use"
    tool_block.input = {
        "location": "Tokyo",
        "temperature_celsius": 22,
        "condition": "Sunny",
        "humidity_percent": 60,
        "summary": "Warm and pleasant.",
    }
    resp = MagicMock()
    resp.content = [tool_block]
    client = MagicMock()
    client.messages.create.return_value = resp
    return client


# ── unit tests ────────────────────────────────────────────────────────────────


def test_demo_native_tool_use_returns_weather_report():
    client = _make_native_mock(None)
    result = example.demo_native_tool_use(client=client)
    assert isinstance(result, example.WeatherReport)
    assert result.location == "Tokyo"
    assert 0 <= result.humidity_percent <= 100
    client.messages.create.assert_called_once()


def test_demo_instructor_single_returns_book_info():
    from unittest.mock import MagicMock

    mock_client = MagicMock()
    mock_client.messages.create.return_value = example.BookInfo(
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        year=1979,
        genre="Science Fiction",
        one_line_summary="A hapless Earthling travels the universe.",
    )
    result = example.demo_instructor_single(client=mock_client)
    assert isinstance(result, example.BookInfo)
    assert result.year == 1979
    mock_client.messages.create.assert_called_once()


def test_demo_instructor_list_returns_list_of_book_info():
    from unittest.mock import MagicMock

    books = [
        example.BookInfo(
            title="Dune",
            author="Frank Herbert",
            year=1965,
            genre="Sci-Fi",
            one_line_summary="Desert planet epic.",
        ),
        example.BookInfo(
            title="Foundation",
            author="Isaac Asimov",
            year=1951,
            genre="Sci-Fi",
            one_line_summary="Fall of a galactic empire.",
        ),
        example.BookInfo(
            title="Neuromancer",
            author="William Gibson",
            year=1984,
            genre="Cyberpunk",
            one_line_summary="Console cowboy meets AI.",
        ),
    ]
    mock_client = MagicMock()
    mock_client.messages.create.return_value = example.BookList(books=books)
    result = example.demo_instructor_list(client=mock_client)
    assert len(result) == 3
    assert all(isinstance(b, example.BookInfo) for b in result)


def test_weather_report_validates_humidity_bounds():
    """Pydantic Field(ge=0, le=100) rejects out-of-range humidity."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        example.WeatherReport(
            location="X",
            temperature_celsius=20,
            condition="Clear",
            humidity_percent=150,
            summary="bad",
        )


# ── live smoke (skipped without key) ─────────────────────────────────────────


@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY") == "test-key",
    reason="ANTHROPIC_API_KEY not set",
)
def test_live_native_tool_use():
    report = example.demo_native_tool_use()
    assert isinstance(report, example.WeatherReport)
    assert report.location
    assert report.summary
