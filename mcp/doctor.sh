#!/usr/bin/env bash
# mcp-doctor — check status of all MCP servers and CLI tools
set -u

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

pass=0
fail=0
warn=0

check() {
  local name=$1; local cmd=$2; local hint=$3
  if eval "$cmd" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ $name${NC}"
    ((pass++))
  else
    echo -e "${RED}❌ $name${NC} — $hint"
    ((fail++))
  fi
}

check_warn() {
  local name=$1; local cmd=$2; local hint=$3
  if eval "$cmd" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ $name${NC}"
    ((pass++))
  else
    echo -e "${YELLOW}⚠️  $name${NC} — $hint"
    ((warn++))
  fi
}

echo "🩺 MCP & CLI Doctor"
echo "===================="
echo ""

echo "--- Core CLI Tools ---"
check "gh CLI"        "gh auth status"           "run: gh auth login"
check "Claude Code"   "command -v claude"        "npm i -g @anthropic-ai/claude-code"
check_warn "yt-dlp"   "command -v yt-dlp"        "pip install -U yt-dlp"
check_warn "jq"       "command -v jq"            "brew install jq"
check_warn "feedparser" "python3 -c 'import feedparser'" "pip install feedparser"
echo ""

echo "--- API Keys ---"
check_warn "GEMINI_API_KEY"  "test -n \"\${GEMINI_API_KEY:-}\""  "set GEMINI_API_KEY in env"
check_warn "OPENAI_API_KEY"  "test -n \"\${OPENAI_API_KEY:-}\""  "set OPENAI_API_KEY in env"
check_warn "TAVILY_API_KEY"  "test -n \"\${TAVILY_API_KEY:-}\""  "set TAVILY_API_KEY in env"
check_warn "BRAVE_API_KEY"   "test -n \"\${BRAVE_API_KEY:-}\""   "set BRAVE_API_KEY in env"
check_warn "FIRECRAWL_API_KEY" "test -n \"\${FIRECRAWL_API_KEY:-}\"" "set FIRECRAWL_API_KEY in env"
check_warn "APIFY_TOKEN"     "test -n \"\${APIFY_TOKEN:-}\""     "set APIFY_TOKEN in env"
echo ""

echo "--- Network Services ---"
check_warn "n8n reachable" "curl -sf --max-time 5 https://n8n.voora.live/healthz" "check Hetzner server"
echo ""

# TODO: add MCP server pings (Brave, Tavily, Firecrawl, Playwright, Apify, Bright Data, Telegram, Apple Notes, Reddit)

echo "===================="
echo -e "Results: ${GREEN}${pass} passed${NC}, ${RED}${fail} failed${NC}, ${YELLOW}${warn} warnings${NC}"
echo ""
echo "Run this anytime something feels broken before debugging code."
