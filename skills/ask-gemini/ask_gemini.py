#!/usr/bin/env python3
"""Ask Gemini a question from CLI. Used by Claude Code for consultations."""

import argparse
import os
import sys
from pathlib import Path

# Load API keys: ~/.config/claude-skills/.env → project .env → env vars
for env_path in [
    Path.home() / ".config" / "claude-skills" / ".env",
    Path.cwd() / ".env",
]:
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv(env_path)
        break

DEFAULT_MODEL = "gemini-3.1-pro-preview"
DEFAULT_TEMPERATURE = 0
DEFAULT_THINKING_BUDGET = 8192


def ask_gemini(
    prompt: str,
    context_files: list[str] | None = None,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    system_instruction: str | None = None,
    thinking_budget: int = DEFAULT_THINKING_BUDGET,
) -> str:
    from google import genai
    from google.genai import types as genai_types

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set. Put it in ~/.config/claude-skills/.env", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key, http_options={"api_version": "v1beta"})

    parts = []
    if context_files:
        for fpath in context_files:
            p = Path(fpath)
            if not p.exists():
                print(f"WARNING: context file not found: {fpath}", file=sys.stderr)
                continue
            text = p.read_text(encoding="utf-8")
            parts.append(f"--- FILE: {p.name} ---\n{text}\n--- END FILE ---\n")

    parts.append(prompt)
    full_content = "\n".join(parts)

    config = genai_types.GenerateContentConfig(
        temperature=temperature,
        thinking_config=genai_types.ThinkingConfig(thinking_budget=thinking_budget),
    )
    if system_instruction:
        config.system_instruction = system_instruction

    response = client.models.generate_content(
        model=model,
        contents=full_content,
        config=config,
    )
    client.close()
    return response.text


def main():
    parser = argparse.ArgumentParser(description="Ask Gemini a question")
    parser.add_argument("question", nargs="?", help="Question text (or pipe via stdin)")
    parser.add_argument("-c", "--context", nargs="+", help="Context files to include")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help=f"Model (default: {DEFAULT_MODEL})")
    parser.add_argument("-t", "--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("-s", "--system", help="System instruction")
    parser.add_argument("--thinking-budget", type=int, default=DEFAULT_THINKING_BUDGET,
                        help=f"Thinking token budget (default: {DEFAULT_THINKING_BUDGET}, 0 to disable)")
    args = parser.parse_args()

    question = args.question
    if not question:
        if sys.stdin.isatty():
            parser.error("Provide a question as argument or pipe via stdin")
        question = sys.stdin.read().strip()

    if not question:
        parser.error("Empty question")

    result = ask_gemini(
        prompt=question,
        context_files=args.context,
        model=args.model,
        temperature=args.temperature,
        system_instruction=args.system,
        thinking_budget=args.thinking_budget,
    )
    print(result)


if __name__ == "__main__":
    main()
