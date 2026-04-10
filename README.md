# dzen-dev-toolkit

Cross-project toolkit for AI/agent development. One repo, two laptops, all the knowledge.

## Two laptops, one toolkit

Personal MacBook + work MacBook. Both have this repo at `~/dev/dzen-dev-toolkit`. Syncing a new laptop = `git pull` + `./setup.sh` + copy `.env.master` from the other machine.

API keys live in `~/.config/dzen-dev-toolkit/.env.master` (not in the repo). Scripts load keys from there automatically.

## Structure

```
skills/                    # Claude Code custom skills
  ask-chatgpt/             #   GPT-5.4 consultation (SKILL.md + Python script)
  ask-gemini/              #   Gemini 3.1 Pro consultation
channels/
  tools-stack.md           #   Which tool for which scenario (scraping, search, etc.)
mcp/
  configs/                 #   Reusable MCP server configs (TODO)
  doctor.sh                #   Health check for all tools & APIs
playbooks/
  credentials-map.md       #   All keys, servers, SSH, repos — single source of truth
  n8n-config.md            #   n8n server setup on Hetzner
  new-agent-project.md     #   Checklist for starting a new agent project
snippets/                  # Reusable code snippets (TODO)
```

## Quick start

```bash
# Clone
git clone git@github.com:iamdzennn/dzen-dev-toolkit.git ~/dev/dzen-dev-toolkit

# Install deps + create config dir
cd ~/dev/dzen-dev-toolkit
./setup.sh

# Copy .env.master from the other laptop
# scp other-laptop:~/.config/dzen-dev-toolkit/.env.master ~/.config/dzen-dev-toolkit/.env.master

# Link skills to a project
./link-to-project.sh ~/dev/my-project

# Health check
./mcp/doctor.sh
```

## What each piece does

### Skills (`skills/`)

Claude Code skills that work in any project. After `link-to-project.sh`, use `/ask-chatgpt` and `/ask-gemini` in Claude Code.

Scripts are self-contained in the toolkit — SKILL.md files reference `~/dev/dzen-dev-toolkit/skills/...` directly, so they work on any machine where the repo is cloned to `~/dev/`.

### Doctor (`mcp/doctor.sh`)

Quick diagnostic: checks CLI tools (gh, claude, yt-dlp, jq), API keys in env, and network services (n8n). Run it before debugging anything.

```bash
~/dev/dzen-dev-toolkit/mcp/doctor.sh
# or add alias to ~/.zshrc:
alias doctor='~/dev/dzen-dev-toolkit/mcp/doctor.sh'
```

### Credentials map (`playbooks/credentials-map.md`)

Single source of truth: all API keys, servers, SSH keys, GitHub/GitLab repos, which laptop has what. Not the keys themselves (those are in `.env.master`), just the map of what exists and where to get new ones.

### Tools stack (`channels/tools-stack.md`)

Decision table: web scraping → Playwright/Firecrawl, search → Tavily/Brave, deep crawl → Apify/Bright Data, etc. Includes known gotchas per tool.

## Linking to projects

`link-to-project.sh` copies SKILL.md files into a project's `.claude/skills/` directory and creates a `TOOLS.md` pointer file. Project-specific skills (like `check-post` for zenevich-blogs) stay in their projects.

```bash
./link-to-project.sh ~/dev/zenevich-blogs
./link-to-project.sh ~/dev/some-other-project
```

## Syncing between laptops

```bash
git pull   # That's it — scripts, playbooks, skills all update
```

API keys (`~/.config/dzen-dev-toolkit/.env.master`) are NOT in the repo. Copy manually when setting up a new machine.
