# Tools Stack — Channel Map

> Single source of truth: which tool I use for which scenario.
> Updated: 2026-04-10

## Channel Map

| Channel / Scenario   | Primary Tool         | Fallback           | Cost     | Local / Server | Status |
|----------------------|----------------------|--------------------|----------|----------------|--------|
| Web scrape (JS)      | Playwright MCP       | Firecrawl          | Free / $ | Both           | ✅     |
| Web scrape (static)  | Firecrawl            | Jina Reader        | $        | Both           | ✅     |
| Web search           | Tavily               | Brave              | $        | Both           | ✅     |
| Deep crawl / dataset | Apify                | Bright Data        | $        | Server         | ✅     |
| Proxy / hard targets | Bright Data          | —                  | $$       | Server         | ✅     |
| YouTube transcripts  | yt-dlp (CLI)         | —                  | Free     | Both           | ⬜ not using yet |
| Reddit               | Apify reddit-scraper | Reddit MCP         | $        | Server         | ✅     |
| Telegram             | Telegram MCP         | —                  | Free     | Local          | ⚠️ session path issue |
| Apple Notes          | Apple Notes MCP      | —                  | Free     | Local Mac      | ✅ (no commas in titles, use `<div>`) |
| GitHub               | gh CLI               | —                  | Free     | Both           | ✅     |
| RSS                  | feedparser (Python)  | —                  | Free     | Both           | ⬜ not using yet |
| Twitter / X          | TODO                 | xreach-cli?        | Free     | Local + cookie | ⬜ not using yet |

## Decision rules
- **New agent project:** start by filling this table for the project's needs before writing code.
- **Local-only flows** → prefer MCP servers in Claude Desktop.
- **Server / n8n flows** → prefer CLI tools + Apify/Bright Data for scraping.
- **Always check `mcp-doctor` before debugging** — usually it's a session/env var, not code.

## Known gotchas
- Telegram MCP: `TELEGRAM_SESSION_PATH` env var name matters
- Apple Notes MCP: requires `<div>` tags (not `<p>`), no commas in titles, can't create folders
- Gemini API: returns malformed JSON, regex cleanup needed
- Veo 3.1: use `veo-3.1-generate-preview:predictLongRunning`
