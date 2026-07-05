"""Tests for 14_mcp_servers/example.py — test tool functions directly (no MCP protocol)."""

import example


# ── tool function tests ───────────────────────────────────────────────────────


def test_get_weather_contains_location():
    result = example.get_weather("Paris")
    assert "Paris" in result
    assert isinstance(result, str)


def test_get_weather_different_locations():
    for city in ("Tokyo", "New York", "Sydney"):
        result = example.get_weather(city)
        assert city in result


def test_calculate_basic_arithmetic():
    assert example.calculate("2 + 2") == "4"
    assert example.calculate("10 * 5") == "50"
    assert example.calculate("100 / 4") == "25.0"


def test_calculate_math_functions():
    result = example.calculate("sqrt(16)")
    assert result == "4.0"


def test_calculate_invalid_expression_returns_error():
    result = example.calculate("import os")
    assert "Error" in result or result == ""


def test_list_files_returns_string():
    result = example.list_files(".")
    assert isinstance(result, str)
    assert "example.py" in result or "pyproject.toml" in result


def test_list_files_nonexistent_directory():
    result = example.list_files("/nonexistent/path/xyz")
    assert "not found" in result.lower()


# ── resource function tests ───────────────────────────────────────────────────


def test_config_resource_is_valid_json():
    import json

    result = example.config_resource()
    data = json.loads(result)
    assert "server" in data
    assert data["server"] == "demo_server"


def test_readme_resource_returns_string():
    result = example.readme_resource()
    assert isinstance(result, str)


# ── mcp server instantiation ──────────────────────────────────────────────────


def test_mcp_server_has_tools_registered():
    tools = example.mcp._tool_manager.list_tools()
    tool_names = {t.name for t in tools}
    assert "get_weather" in tool_names
    assert "calculate" in tool_names
    assert "list_files" in tool_names
