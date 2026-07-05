"""07 — CrewAI: a minimal, runnable reference.

WHY this layer: CrewAI models problems as role-based teams — each agent has a role,
goal, and tools; a "crew" coordinates them on tasks. Natural fit when a problem
decomposes into roles (researcher → writer → reviewer). If you need precise, debuggable
control flow instead of roles, use LangGraph (06). Switching cost = 4.
See ../compatibility_matrix.md.

LOCAL OLLAMA SWAP (zero API cost):
  Replace the LLM below with:
    LLM(model="ollama/qwen2.5-coder:14b", base_url="http://localhost:11434")
  Works because CrewAI uses litellm under the hood, which is OpenAI-compatible.

One demo:
  demo_research_write_crew — Researcher + Writer, two sequential tasks

Run:
  uv run python example.py
"""

from __future__ import annotations

import os
import sys

from crewai import Agent, Crew, LLM, Process, Task
from dotenv import load_dotenv

load_dotenv()

SMOKE_MODEL = "anthropic/claude-haiku-4-5-20251001"
QUALITY_MODEL = "anthropic/claude-opus-4-8"
MODEL = SMOKE_MODEL


def _llm() -> LLM:
    return LLM(model=MODEL, api_key=os.environ.get("ANTHROPIC_API_KEY", ""))


def demo_research_write_crew(topic: str = "benefits of open-source LLMs") -> str:
    """Researcher → Writer crew on a given topic. Returns the writer's final output."""
    llm = _llm()

    researcher = Agent(
        role="Research Analyst",
        goal=f"Find 3 key facts about: {topic}",
        backstory="You are a diligent researcher who finds accurate, concise information.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    writer = Agent(
        role="Content Writer",
        goal="Write a clear, one-paragraph summary using the researcher's findings.",
        backstory="You are a concise technical writer who turns research into readable prose.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    research_task = Task(
        description=f"Research and list 3 key facts about: {topic}",
        expected_output="A bullet list of exactly 3 facts.",
        agent=researcher,
    )

    write_task = Task(
        description="Using the researcher's bullet list, write one clear paragraph.",
        expected_output="One paragraph (3–5 sentences) summarising the research.",
        agent=writer,
        context=[research_task],
    )

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()
    output = result.raw if hasattr(result, "raw") else str(result)
    print(output)
    return output


def main(argv: list[str] | None = None) -> int:
    if not os.getenv("ANTHROPIC_API_KEY"):
        print(
            "ANTHROPIC_API_KEY is not set.\n"
            "  1. cp ../.env.example .env\n"
            "  2. add your key: ANTHROPIC_API_KEY=sk-ant-...\n"
            "  OR swap to local: LLM(model='ollama/qwen2.5-coder:14b', base_url='http://localhost:11434')\n"
            "  3. re-run:        uv run python example.py",
            file=sys.stderr,
        )
        return 1

    demo_research_write_crew()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
