---
name: summarize-yt
description: Summarize a transcript via GPT-5.4 — key ideas, workflows, screenshot timestamps — and rename all files
---

# Summarize YouTube Transcript

Send a timestamped transcript to GPT-5.4 for structured summary, then rename all files consistently.

## Steps

1. **Run the script:**
   ```bash
   python3 ~/dev/dzen-dev-toolkit/skills/summarize-yt/summarize_yt.py "/path/to/transcript.md" "/path/to/video.mp4"
   ```

2. **Report the result** — show the user:
   - Summary highlights
   - Recommended screenshot timestamps
   - New file names

## What it does

1. Sends transcript to GPT-5.4 with a structured prompt
2. Gets back: key ideas, workflows, recommendations, screenshot timestamps
3. GPT generates a short slug for the video
4. Renames all 3 files to `{YYYYMMDD_HHMM}_{slug}.{ext}`:
   - `20260415_2030_product-launch-stream.mp4` (video)
   - `20260415_2030_product-launch-stream.md` (transcript)
   - `20260415_2030_product-launch-stream_summary.md` (summary)

## Additional flags

- `--url <youtube-url>` — original YouTube URL (for dzen-os metadata)
- `--save-to-dzen-os` — save analysis to `~/dev/dzen-os/raw/` with proper frontmatter

## Prerequisites

- `OPENAI_API_KEY` in `~/.config/dzen-dev-toolkit/.env.master`
- `~/dev/dzen-os` cloned (for --save-to-dzen-os)
