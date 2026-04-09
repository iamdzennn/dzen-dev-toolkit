---
name: ask-gemini
description: Send a consultation question to Gemini 3.1 Pro and get a response directly. Use when you need Gemini's opinion on implementation, architecture, prompt design, or model behavior.
---

# Ask Gemini Consultation

You need to consult Gemini 3.1 Pro about an implementation question. Use the `ask_gemini.py` script from the claude-skills repo.

## Steps

1. **Formulate the question** — include full context so Gemini can give a useful answer:
   - What you're trying to achieve
   - Current state / what exists
   - Specific question or trade-offs to evaluate
   - Any constraints

2. **Attach context files if needed** — use `-c` flag for relevant files

3. **Run the script:**
   ```bash
   python3 ~/.config/claude-skills/ask-gemini/ask_gemini.py "Your question here"

   # With context files
   python3 ~/.config/claude-skills/ask-gemini/ask_gemini.py "question" -c file1.md file2.py

   # With system instruction
   python3 ~/.config/claude-skills/ask-gemini/ask_gemini.py "question" -s "You are an expert"

   # Via stdin
   echo "long question" | python3 ~/.config/claude-skills/ask-gemini/ask_gemini.py

   # Custom temperature (default 0)
   python3 ~/.config/claude-skills/ask-gemini/ask_gemini.py "question" -t 0.7
   ```

4. **Present Gemini's response** to the user with your own analysis — agree/disagree/synthesize

## Guidelines

- Default model: `gemini-3.1-pro-preview` (latest, with thinking) — do NOT change unless user asks
- Temperature 0 by default (deterministic, precise answers)
- Thinking enabled by default (budget 8192 tokens) — let it reason deeply
- To disable thinking: `--thinking-budget 0`
- Always include enough context — Gemini doesn't see our conversation
- If the question is about prompts or rules, attach the relevant master files as context
- Present both Gemini's answer AND your own take — user wants synthesis, not just relay
