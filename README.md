# claude-skills

Cross-project toolkit for AI/agent development. One repo, two laptops, all the knowledge.

## Structure

```
skills/          # Claude Code custom skills (ask-gemini, ask-chatgpt)
channels/        # Channel maps — what tool for what scenario
mcp/             # MCP configs and doctor script
  configs/       # Reusable MCP server configs
  doctor.sh      # Health check for all tools & APIs
playbooks/       # Step-by-step checklists (new project, debugging, etc.)
snippets/        # Reusable code snippets
```

## Quick start

```bash
# Install skills + dependencies
./setup.sh

# Link skills to a project
./link-to-project.sh ~/dev/my-project

# Run health check
./mcp/doctor.sh
```

## Doctor alias

Add to your `~/.zshrc`:

```bash
alias doctor='~/dev/claude-skills/mcp/doctor.sh'
```

## Linking to projects

In any agent project, create a `TOOLS.md`:

```bash
echo "See ~/dev/claude-skills" > TOOLS.md
```

Or run the full linker which also installs skills:

```bash
./link-to-project.sh /path/to/project
```

## Second laptop sync

```bash
git pull  # That's it
```
