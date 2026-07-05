"""05 — LangChain: a minimal, runnable reference.

WHY this layer: swap providers behind one interface; batteries-included retrieval and
tool integrations; huge ecosystem. Reach for it when raw SDK calls get tangled across
providers or when you need a retriever. Don't add it "just in case" — for single-model
calls the raw SDK is leaner. Switching cost from LangChain to raw SDK = 2.
See ../compatibility_matrix.md.

Three demos:
  1. basic_chain     — ChatAnthropic | StrOutputParser LCEL chain
  2. provider_swap   — identical chain wired to ChatOpenAI (proves the interface is the same)
  3. retrieval       — InMemoryVectorStore + hash embeddings → retrieve → answer

Run:
  uv run python example.py              # all three
  uv run python example.py basic_chain  # or: provider_swap | retrieval
"""

from __future__ import annotations

import hashlib
import os
import sys

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore

load_dotenv()


class _HashEmbeddings:
    """Deterministic fake embeddings using SHA-256. No numpy required.

    Produces consistent vectors so retrieval tests are stable without any model server.
    """

    def __init__(self, size: int = 128) -> None:
        self.size = size

    def embed_query(self, text: str) -> list[float]:
        raw = hashlib.sha256(text.encode()).digest()
        return [(raw[i % 32] / 127.5) - 1.0 for i in range(self.size)]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(t) for t in texts]


SMOKE_MODEL = "claude-haiku-4-5-20251001"
QUALITY_MODEL = "claude-opus-4-8"
MODEL = SMOKE_MODEL

MAX_TOKENS = 512


def _anthropic_model(model: str | None = None) -> ChatAnthropic:
    return ChatAnthropic(model=model or MODEL, max_tokens=MAX_TOKENS)


def demo_basic_chain() -> str:
    """LCEL chain: prompt | ChatAnthropic | StrOutputParser — the LangChain canonical pattern."""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{question}"),
        ]
    )
    chain = prompt | _anthropic_model() | StrOutputParser()
    answer = chain.invoke({"question": "In one sentence, what is LangChain?"})
    print(answer)
    return answer


def demo_provider_swap() -> str:
    """Same LCEL chain, swapped to ChatOpenAI — proves the interface is identical.

    Skips gracefully when OPENAI_API_KEY is not set, so this never blocks a demo run.
    Switching cost between providers in LangChain = 1 (swap the model class).
    """
    if not os.getenv("OPENAI_API_KEY"):
        msg = (
            "[provider_swap] OPENAI_API_KEY not set — skipping (set it in .env to run)"
        )
        print(msg)
        return msg

    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_messages([("human", "{question}")])
    chain = (
        prompt
        | ChatOpenAI(model="gpt-4o-mini", max_tokens=MAX_TOKENS)
        | StrOutputParser()
    )
    answer = chain.invoke({"question": "In one sentence, what is LangChain?"})
    print(f"[openai] {answer}")
    return answer


def demo_retrieval() -> str:
    """Retrieve → stuff → answer: the core RAG pattern in LangChain.

    Uses InMemoryVectorStore + FakeEmbeddings (no Ollama required) to keep this
    demo runnable without any external services. Swap FakeEmbeddings for
    OllamaEmbeddings (see 08_chromadb_rag) when you need real semantic search.
    """
    docs = [
        "LangChain is a framework for building LLM applications.",
        "LCEL stands for LangChain Expression Language and uses the | pipe operator.",
        "LangGraph extends LangChain with stateful, cyclic workflows.",
        "ChromaDB is a local vector database useful for RAG.",
        "Claude Haiku is Anthropic's fastest, cheapest model.",
    ]

    embeddings = _HashEmbeddings(size=128)
    store = InMemoryVectorStore(embedding=embeddings)
    store.add_texts(docs)
    retriever = store.as_retriever(search_kwargs={"k": 3})

    query = "What is LCEL?"
    retrieved = retriever.invoke(query)
    context = "\n".join(d.page_content for d in retrieved)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Answer using only the context below.\n\nContext:\n{context}"),
            ("human", "{question}"),
        ]
    )
    chain = prompt | _anthropic_model() | StrOutputParser()
    answer = chain.invoke({"context": context, "question": query})
    print(answer)
    return answer


DEMOS = {
    "basic_chain": demo_basic_chain,
    "provider_swap": demo_provider_swap,
    "retrieval": demo_retrieval,
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
