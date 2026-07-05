"""06 — LangGraph: a minimal, runnable reference.

WHY this layer: StateGraph lets you express loops, branches, and human-in-the-loop
workflows that plain LangChain chains can't. "Chain" = linear pipeline; "graph" = cycles.
Add LangGraph only when the control flow gets too tangled for LCEL. Switching cost to
CrewAI = 4 (roles vs explicit state machine — different mental model).
See ../compatibility_matrix.md.

Two demos:
  1. simple_graph  — linear START → llm_node → END; shows the graph API without tools
  2. react_loop    — ReAct pattern: llm_node ↔ tools_node, loops until end_turn

Both use MessagesState (built-in) so no TypedDict boilerplate needed.

Run:
  uv run python example.py               # all demos
  uv run python example.py simple_graph  # or: react_loop
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

SMOKE_MODEL = "claude-haiku-4-5-20251001"
QUALITY_MODEL = "claude-opus-4-8"
MODEL = SMOKE_MODEL

MAX_TOKENS = 1024


def _llm(tools: list | None = None) -> ChatAnthropic:
    base = ChatAnthropic(model=MODEL, max_tokens=MAX_TOKENS)
    return base.bind_tools(tools) if tools else base


def demo_simple_graph() -> str:
    """Linear graph: START → llm → END. Proves the StateGraph API with no extra deps."""

    def llm_node(state: MessagesState) -> dict:
        return {"messages": [_llm().invoke(state["messages"])]}

    graph = StateGraph(MessagesState)
    graph.add_node("llm", llm_node)
    graph.add_edge(START, "llm")
    graph.add_edge("llm", END)
    app = graph.compile()

    result = app.invoke(
        {"messages": [HumanMessage(content="In one sentence, what is LangGraph?")]}
    )
    text = result["messages"][-1].content
    print(text)
    return text


@tool
def get_weather(location: str) -> str:
    """Return the current weather for a location.

    Args:
        location: City name.
    """
    return f"It is 22C and sunny in {location}."


def demo_react_loop() -> str:
    """ReAct loop: llm ↔ tools, cycles until the model stops calling tools.

    Graph shape: START → llm → [tools_condition] → tools → llm (loop) or END.
    tools_condition is a built-in langgraph helper that routes on whether the last
    message contains tool_calls.
    """
    tools = [get_weather]
    model_with_tools = _llm(tools)

    def llm_node(state: MessagesState) -> dict:
        return {"messages": [model_with_tools.invoke(state["messages"])]}

    graph = StateGraph(MessagesState)
    graph.add_node("llm", llm_node)
    graph.add_node("tools", ToolNode(tools))
    graph.add_edge(START, "llm")
    graph.add_conditional_edges("llm", tools_condition)
    graph.add_edge("tools", "llm")
    app = graph.compile()

    result = app.invoke(
        {"messages": [HumanMessage(content="What's the weather in Paris?")]}
    )
    text = result["messages"][-1].content
    print(text)
    return text


DEMOS = {
    "simple_graph": demo_simple_graph,
    "react_loop": demo_react_loop,
}


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    if not os.getenv("ANTHROPIC_API_KEY"):
        print(
            "ANTHROPIC_API_KEY is not set.\n"
            "  1. cp ../.env.example .env\n"
            "  2. add your key: ANTHROPIC_API_KEY=sk-ant-...\n"
            "  3. re-run:       uv run python example.py",
            file=sys.stderr,
        )
        return 1

    if argv:
        name = argv[0]
        if name not in DEMOS:
            print(
                f"Unknown demo '{name}'. Choose from: {', '.join(DEMOS)}",
                file=sys.stderr,
            )
            return 2
        DEMOS[name]()
        return 0

    for name, fn in DEMOS.items():
        print(f"\n=== {name} ===")
        fn()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
