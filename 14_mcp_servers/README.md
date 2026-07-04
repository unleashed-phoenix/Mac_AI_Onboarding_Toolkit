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
uv init
uv python pin 3.12
uv add "mcp[cli]" python-dotenv
cp ../.env.example .env
```
Scaffold a server: `uv run mcp` (CLI helpers). Register it in your client's MCP config.

## Alternatives & switching
| Alt | Trade-off | Switch cost |
|---|---|---|
| Provider-native tools | No cross-client reuse | 2 |
| LangChain tools | Framework-bound | 3 |

## Mac vs Windows
No difference in Python; only the client config path differs.

## Status
⬜ Scaffold only.
