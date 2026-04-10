#!/bin/bash
# Setup dzen-dev-toolkit: install deps + create config dir + symlink skills
set -e

SKILLS_DIR="$HOME/.config/dzen-dev-toolkit"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Claude Skills Setup ==="

# 1. Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r "$REPO_DIR/requirements.txt" --quiet

# 2. Create config directory
mkdir -p "$SKILLS_DIR"

# 3. Symlink skill directories
for skill_dir in "$REPO_DIR"/skills/ask-*/; do
    skill_name=$(basename "$skill_dir")
    target="$SKILLS_DIR/$skill_name"
    if [ -L "$target" ]; then
        rm "$target"
    fi
    ln -s "$skill_dir" "$target"
    echo "  Linked: $skill_name → $target"
done

# 4. Create .env if not exists
if [ ! -f "$SKILLS_DIR/.env" ]; then
    cp "$REPO_DIR/.env.example" "$SKILLS_DIR/.env"
    echo ""
    echo "  Created $SKILLS_DIR/.env — fill in your API keys!"
    echo "  Edit: nano $SKILLS_DIR/.env"
else
    echo "  .env already exists at $SKILLS_DIR/.env"
fi

echo ""
echo "Done! Skills installed to $SKILLS_DIR"
echo ""
echo "Next steps:"
echo "  1. Add API keys to $SKILLS_DIR/.env"
echo "  2. In each Claude Code project, copy skill SKILL.md files to .claude/skills/"
echo "     Or run: ./link-to-project.sh /path/to/project"
