#!/bin/bash
# Link skills to a Claude Code project so they appear as /ask-gemini and /ask-chatgpt
set -e

if [ -z "$1" ]; then
    echo "Usage: ./link-to-project.sh /path/to/project"
    exit 1
fi

PROJECT="$1"
SKILLS_DIR="$HOME/.config/dzen-dev-toolkit"

if [ ! -d "$PROJECT" ]; then
    echo "ERROR: Project directory not found: $PROJECT"
    exit 1
fi

mkdir -p "$PROJECT/.claude/skills"

for skill_dir in "$SKILLS_DIR"/ask-*/; do
    skill_name=$(basename "$skill_dir")
    target="$PROJECT/.claude/skills/$skill_name"
    mkdir -p "$target"
    # Copy SKILL.md (Claude Code reads this to discover the skill)
    cp "$skill_dir/SKILL.md" "$target/SKILL.md"
    echo "  Installed: $skill_name → $target"
done

# Create TOOLS.md link
TOOLS_FILE="$PROJECT/TOOLS.md"
if [ ! -f "$TOOLS_FILE" ]; then
    echo "See ~/dev/dzen-dev-toolkit for channel maps, MCP configs, doctor script, and playbooks." > "$TOOLS_FILE"
    echo "  Created: TOOLS.md"
fi

echo ""
echo "Done! Skills available in $PROJECT"
echo "  Use /ask-gemini and /ask-chatgpt in Claude Code"
echo "  Run ~/dev/dzen-dev-toolkit/mcp/doctor.sh to check tool health"
