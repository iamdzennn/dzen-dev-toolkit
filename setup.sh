#!/bin/bash
# Setup dzen-dev-toolkit: install deps + create config dir for secrets
set -e

CONFIG_DIR="$HOME/.config/dzen-dev-toolkit"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== dzen-dev-toolkit setup ==="

# 1. Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r "$REPO_DIR/requirements.txt" --quiet

# 2. Create config directory for secrets (not in repo)
mkdir -p "$CONFIG_DIR"

# 3. Create .env.master if not exists
if [ ! -f "$CONFIG_DIR/.env.master" ]; then
    if [ -f "$REPO_DIR/.env.example" ]; then
        cp "$REPO_DIR/.env.example" "$CONFIG_DIR/.env.master"
    else
        touch "$CONFIG_DIR/.env.master"
    fi
    echo "  Created $CONFIG_DIR/.env.master — fill in your API keys!"
    echo "  Edit: nano $CONFIG_DIR/.env.master"
else
    echo "  .env.master already exists at $CONFIG_DIR/.env.master"
fi

echo ""
echo "Done!"
echo ""
echo "Next steps:"
echo "  1. Add API keys to $CONFIG_DIR/.env.master"
echo "  2. Link skills to projects: ./link-to-project.sh ~/dev/<project>"
