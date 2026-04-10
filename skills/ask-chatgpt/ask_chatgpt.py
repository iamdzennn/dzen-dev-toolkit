#!/usr/bin/env python3
"""Ask ChatGPT a question from CLI. Used by Claude Code for consultations."""

import argparse
import os
import sys
from pathlib import Path

# Load API keys: ~/.config/dzen-dev-toolkit/.env.master → project .env → env vars
for env_path in [
    Path.home() / ".config" / "dzen-dev-toolkit" / ".env.master",
    Path.cwd() / ".env",
]:
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv(env_path)
        break

DEFAULT_MODEL = "gpt-5.4"
DEFAULT_TEMPERATURE = 1  # gpt-5.4 only supports temperature=1
DEFAULT_REASONING = "high"


def ask_chatgpt(
    prompt: str,
    context_files: list[str] | None = None,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    system_instruction: str | None = None,
    reasoning_effort: str = DEFAULT_REASONING,
) -> str:
    from openai import OpenAI

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set. Put it in ~/.config/dzen-dev-toolkit/.env.master", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)

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

    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.append({"role": "user", "content": full_content})

    kwargs = dict(model=model, messages=messages)
    # gpt-5.4 only supports temperature=1, so don't send it unless non-default model
    if model != "gpt-5.4":
        kwargs["temperature"] = temperature
    if reasoning_effort:
        kwargs["reasoning_effort"] = reasoning_effort

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content


def main():
    parser = argparse.ArgumentParser(description="Ask ChatGPT a question")
    parser.add_argument("question", nargs="?", help="Question text (or pipe via stdin)")
    parser.add_argument("-c", "--context", nargs="+", help="Context files to include")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help=f"Model (default: {DEFAULT_MODEL})")
    parser.add_argument("-t", "--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("-s", "--system", help="System instruction")
    parser.add_argument("-r", "--reasoning", default=DEFAULT_REASONING,
                        choices=["low", "medium", "high", "none"],
                        help=f"Reasoning effort (default: {DEFAULT_REASONING})")
    args = parser.parse_args()

    question = args.question
    if not question:
        if sys.stdin.isatty():
            parser.error("Provide a question as argument or pipe via stdin")
        question = sys.stdin.read().strip()

    if not question:
        parser.error("Empty question")

    result = ask_chatgpt(
        prompt=question,
        context_files=args.context,
        model=args.model,
        temperature=args.temperature,
        system_instruction=args.system,
        reasoning_effort=args.reasoning if args.reasoning != "none" else None,
    )
    print(result)


if __name__ == "__main__":
    main()
