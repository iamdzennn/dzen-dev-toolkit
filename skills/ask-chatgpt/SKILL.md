---
name: ask-chatgpt
description: Ask ChatGPT (GPT-5.4) for a second opinion on architecture, pricing, strategy, or technical decisions
---

# Ask ChatGPT Consultation

You need to consult ChatGPT about an implementation question. Use the `ask_chatgpt.py` script from the claude-skills repo.

## Steps

1. **Formulate the question** — include full context so ChatGPT can give a useful answer:
   - What you're trying to achieve
   - Current state / what exists
   - Specific question or trade-offs to evaluate
   - Any constraints

2. **Attach context files if needed** — use `-c` flag for relevant files

3. **Run the script:**
   ```bash
   python3 ~/dev/dzen-dev-toolkit/skills/ask-chatgpt/ask_chatgpt.py "Your question here"

   # With context files
   python3 ~/dev/dzen-dev-toolkit/skills/ask-chatgpt/ask_chatgpt.py "question" -c file1.md file2.py

   # With system instruction
   python3 ~/dev/dzen-dev-toolkit/skills/ask-chatgpt/ask_chatgpt.py "question" -s "You are an expert"

   # Via stdin
   echo "long question" | python3 ~/dev/dzen-dev-toolkit/skills/ask-chatgpt/ask_chatgpt.py

   # Custom reasoning effort
   python3 ~/dev/dzen-dev-toolkit/skills/ask-chatgpt/ask_chatgpt.py "question" -r medium
   ```

4. **Present ChatGPT's response** to the user with your own analysis — agree/disagree/synthesize

## Guidelines

- Default model: `gpt-5.4` (latest with thinking) — do NOT change unless user asks
- Reasoning effort: high by default
- NOTE: gpt-5.4 only supports temperature=1 (fixed), -t flag ignored for this model
- Always include enough context — ChatGPT doesn't see our conversation
- If the question is about prompts or rules, attach the relevant master files as context
- Present both ChatGPT's answer AND your own take — user wants synthesis, not just relay
- ChatGPT is especially useful for Sora-related questions (OpenAI's model)
