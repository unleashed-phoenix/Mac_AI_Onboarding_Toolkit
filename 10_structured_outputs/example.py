"""
10_structured_outputs — Force typed JSON from any LLM
======================================================

WHY reach for it
- Raw LLM output is text; downstream code needs typed data → parse failures + retries.
- Two reliable patterns:
  1. Native tool-use: ask the model to call a function whose input schema IS your Pydantic
     model. Anthropic/OpenAI both support this; model can't output prose instead.
  2. Instructor (pip: instructor): wraps the client, injects the schema automatically, and
     retries automatically on Pydantic ValidationError (default max_retries=3).

Compared to prompt-only JSON instructions
- Tool-use enforces valid JSON structure at the API level.
- Instructor adds Pydantic field validation + retry loop on bad data.

Switching cost
- Anthropic ↔ OpenAI via Instructor: swap instructor.from_anthropic for
  instructor.from_openai — same Pydantic models work unchanged.
- Native tool-use: each provider has slightly different tool-call response shape, but
  the Pydantic models themselves are always portable.
"""

from __future__ import annotations

import os
import sys

import anthropic
import instructor
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL = "claude-haiku-4-5-20251001"


class WeatherReport(BaseModel):
    location: str
    temperature_celsius: int
    condition: str
    humidity_percent: int = Field(ge=0, le=100)
    summary: str


class BookInfo(BaseModel):
    title: str
    author: str
    year: int
    genre: str
    one_line_summary: str


class BookList(BaseModel):
    books: list[BookInfo]


def demo_native_tool_use(client: anthropic.Anthropic | None = None) -> WeatherReport:
    """Native Anthropic structured output: Pydantic → JSON schema → tool_use → parse."""
    if client is None:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    response = client.messages.create(
        model=MODEL,
        max_tokens=512,
        tools=[
            {
                "name": "record_weather",
                "description": "Record a weather report for a location.",
                "input_schema": WeatherReport.model_json_schema(),
            }
        ],
        tool_choice={"type": "tool", "name": "record_weather"},
        messages=[
            {
                "role": "user",
                "content": "What's the weather like in Tokyo right now? Make up a plausible report.",
            }
        ],
    )
    tool_block = next(b for b in response.content if b.type == "tool_use")
    return WeatherReport.model_validate(tool_block.input)


def demo_instructor_single(client: instructor.Instructor | None = None) -> BookInfo:
    """Instructor wraps the client: automatic schema injection + validation retry."""
    if client is None:
        client = instructor.from_anthropic(
            anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        )

    return client.messages.create(
        model=MODEL,
        max_tokens=512,
        response_model=BookInfo,
        messages=[
            {
                "role": "user",
                "content": "Tell me about 'The Hitchhiker's Guide to the Galaxy'.",
            }
        ],
    )


def demo_instructor_list(client: instructor.Instructor | None = None) -> list[BookInfo]:
    """Instructor: extract a list of structured items in a single call."""
    if client is None:
        client = instructor.from_anthropic(
            anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        )

    result = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        response_model=BookList,
        messages=[
            {
                "role": "user",
                "content": "Name 3 classic science fiction books with full details.",
            }
        ],
    )
    return result.books


def main() -> None:
    target = sys.argv[1] if len(sys.argv) > 1 else "all"

    if target in ("all", "native"):
        report = demo_native_tool_use()
        print("\n=== Native tool-use ===")
        print(report.model_dump_json(indent=2))

    if target in ("all", "instructor"):
        book = demo_instructor_single()
        print("\n=== Instructor single ===")
        print(book.model_dump_json(indent=2))

    if target in ("all", "list"):
        books = demo_instructor_list()
        print("\n=== Instructor list ===")
        for b in books:
            print(f"  {b.title} ({b.year}) by {b.author}")


if __name__ == "__main__":
    main()
