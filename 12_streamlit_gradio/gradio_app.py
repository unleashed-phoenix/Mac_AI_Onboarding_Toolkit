"""Gradio chat interface — run with: uv run python gradio_app.py"""

import gradio as gr

from example import chat_once


def respond(message: str, history: list[list[str]]) -> str:
    """Convert Gradio history format to our dict format and call chat_once."""
    prior: list[dict] = []
    for human, assistant in history:
        prior.append({"role": "user", "content": human})
        if assistant:
            prior.append({"role": "assistant", "content": assistant})
    return chat_once(message, history=prior)


demo = gr.ChatInterface(
    fn=respond,
    title="Claude Chat",
    description="Powered by claude-haiku-4-5-20251001 · folder 12",
    examples=["What is Python?", "Write a haiku about AI."],
)

if __name__ == "__main__":
    demo.launch()
