"""
14_mcp_servers — Model Context Protocol server
===============================================

WHY reach for it
- MCP (Model Context Protocol, by Anthropic) is the standard protocol for giving AI
  assistants (Claude Code, Cursor, etc.) access to YOUR tools and data via a lightweight
  server — instead of copy-pasting context into every prompt.
- Write once in Python, register once, every MCP-compatible client picks it up.

HOW it works
- This file defines an MCP server using FastMCP (the high-level wrapper in mcp[cli]).
- The server exposes: tools (callable functions) and resources (readable data).
- When run, it listens on stdio (default) or SSE and responds to JSON-RPC calls from the
  client (Claude Code, etc.).

Run the server
    uv run python example.py

Register in Claude Code (~/.claude/settings.json)
    {
      "mcpServers": {
        "demo_server": {
          "command": "uv",
          "args": ["run", "--directory", "/abs/path/to/14_mcp_servers", "python", "example.py"]
        }
      }
    }

WHEN NOT to
- You just need one-off tool use → pass tools= directly to the LLM API (folders 01/03).
- You need a persistent daemon with auth → consider FastAPI (11) instead.

Alternatives
| Alt | Trade-off |
|---|---|
| FastAPI + OpenAPI | HTTP REST, no MCP protocol overhead, needs custom client |
| LangChain tools | Already in LangChain graph (05/06), not reusable across clients |
"""

from __future__ import annotations

import math

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "demo_server", instructions="Demo MCP server with weather and math tools."
)


# ── tools ─────────────────────────────────────────────────────────────────────


@mcp.tool()
def get_weather(location: str) -> str:
    """Get the current weather for a city. Returns a short weather description."""
    return f"It is 22°C and partly cloudy in {location}."


@mcp.tool()
def calculate(expression: str) -> str:
    """Evaluate a simple mathematical expression safely. E.g. '2 + 2' or 'sqrt(16)'."""
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
    allowed_names.update({"abs": abs, "round": round})
    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)  # noqa: S307
        return str(result)
    except Exception as exc:
        return f"Error: {exc}"


@mcp.tool()
def list_files(directory: str = ".") -> str:
    """List files in a directory (relative to the server's working directory)."""
    import os

    try:
        entries = os.listdir(directory)
        return "\n".join(sorted(entries)) if entries else "(empty)"
    except FileNotFoundError:
        return f"Directory not found: {directory}"


# ── resources ─────────────────────────────────────────────────────────────────


@mcp.resource("data://readme")
def readme_resource() -> str:
    """Expose this folder's README as an MCP resource."""
    try:
        with open("README.md") as f:
            return f.read()
    except FileNotFoundError:
        return "README.md not found."


@mcp.resource("data://config")
def config_resource() -> str:
    """Expose a small config blob for demonstration."""
    import json

    return json.dumps(
        {
            "server": "demo_server",
            "version": "1.0.0",
            "models_supported": ["claude-*", "gpt-*"],
        },
        indent=2,
    )


if __name__ == "__main__":
    mcp.run()
