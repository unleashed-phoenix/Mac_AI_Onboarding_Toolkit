# 14 — MCP Servers (Model Context Protocol)

## What it is
MCP is the open standard for giving LLMs/agents tools, data, and prompts through a uniform
protocol. Build a server once; Claude Code, Cursor, and other MCP clients can all use it.

## WHY reach for it
- Write a tool once, reuse across every MCP-aware client.
- First-class in Claude Code (Phase 4·1) and this project's Cowork setup.
- Clean separation between agent and capabilities.

## WHEN NOT to
- One app, one tool, no reuse → a plain function call is enough.

## Install
```
cd 14_mcp_servers
uv init --python 3.12
uv add "mcp[cli]" python-dotenv
uv add --dev pytest
```

## Run / Register
```
uv run python example.py          # starts MCP server on stdio
uv run pytest                     # 10 tests, no server needed (tool fns tested directly)
```

Register in Claude Code (`~/.claude/settings.json`):
```json
{
  "mcpServers": {
    "demo_server": {
      "command": "uv",
      "args": ["run", "--directory", "/abs/path/to/14_mcp_servers", "python", "example.py"]
    }
  }
}
```
`example.py` exposes: `get_weather`, `calculate`, `list_files` tools and `data://readme`,
`data://config` resources. Tool functions are pure Python — no MCP protocol needed to test.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| Provider-native tools | No cross-client reuse | 2 |
| LangChain tools | Framework-bound | 3 |

## Mac vs Windows
No difference in Python; only the client config path differs.

## Status
✅ Deep-dive complete — `example.py` (3 tools + 2 resources via FastMCP) and `tests/`
(10 tests, all passing) on Python 3.12. No API key or running server needed for tests.
