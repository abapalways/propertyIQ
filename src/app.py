"""PropertyIQ — Gradio ChatInterface stub.

This is an intentionally minimal but *runnable* scaffold. It:
  1. Loads environment variables from a local .env file (if present).
  2. Checks whether OPENAI_API_KEY is configured.
  3. Serves a Gradio ChatInterface that echoes the user's message with a clear
     "agent logic not wired up yet" placeholder.

The real agent (RAG retrieval, mortgage/comps tools, memory, and fair-housing
guardrails) is not implemented here yet — see requirements.md and docs/team.md.

Run it with:  python src/app.py
"""

import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
KEY_CONFIGURED = bool(OPENAI_API_KEY and OPENAI_API_KEY.strip() and "your-openai-api-key" not in OPENAI_API_KEY)

PLACEHOLDER_NOTE = (
    "_(PropertyIQ agent logic is not wired up yet — RAG, mortgage/comps tools, "
    "memory, and fair-housing guardrails are still to come. This is a scaffold echo.)_"
)


def respond(message: str, history: list) -> str:
    """Echo the user's message back with a scaffold placeholder.

    `history` is accepted to match the Gradio ChatInterface signature but is
    unused in this stub.
    """
    del history  # not used in the stub

    if not KEY_CONFIGURED:
        return (
            "⚠️ **OPENAI_API_KEY is not configured.**\n\n"
            "Copy `.env.example` to `.env` and set your key to enable real model "
            "calls once the agent is implemented.\n\n"
            f"You said: “{message}”\n\n"
            f"{PLACEHOLDER_NOTE}"
        )

    return (
        f"✅ OPENAI_API_KEY detected.\n\n"
        f"You said: “{message}”\n\n"
        f"{PLACEHOLDER_NOTE}"
    )


def build_demo():
    import gradio as gr

    return gr.ChatInterface(
        fn=respond,
        title="PropertyIQ",
        description=(
            "Property-search & deal-analysis assistant (scaffold). "
            "Ask about listings, mortgages, or comparables — real agent logic is coming."
        ),
    )


def main():
    status = "configured ✅" if KEY_CONFIGURED else "NOT configured ⚠️ (running in echo-only mode)"
    print(f"[PropertyIQ] OPENAI_API_KEY is {status}")
    demo = build_demo()
    demo.launch()


if __name__ == "__main__":
    main()
