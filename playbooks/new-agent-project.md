# New Agent Project Checklist

Before writing code, run through this checklist:

1. [ ] **Channel map** — Open `channels/tools-stack.md`, fill in rows relevant to this project
2. [ ] **Run doctor** — `~/dev/dzen-dev-toolkit/mcp/doctor.sh` — confirm all needed channels are ✅
3. [ ] **MCP config** — Copy relevant MCP config from `mcp/configs/` if needed
4. [ ] **Link toolkit** — `echo "See ~/dev/dzen-dev-toolkit" > TOOLS.md` in project root
5. [ ] **Check gotchas** — Review "Known gotchas" section in `channels/tools-stack.md`
6. [ ] **Only then** — start coding

## Quick start

```bash
# From your new project directory:
~/dev/dzen-dev-toolkit/link-to-project.sh "$(pwd)"
~/dev/dzen-dev-toolkit/mcp/doctor.sh
```
