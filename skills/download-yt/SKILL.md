---
name: download-yt
description: Download YouTube video or audio using yt-dlp
---

# Download YouTube Video

Download a YouTube video (or playlist) using `yt-dlp`.

## Steps

1. **Run the script:**
   ```bash
   python3 ~/dev/dzen-dev-toolkit/skills/download-yt/download_yt.py "URL"

   # Save to specific directory
   python3 ~/dev/dzen-dev-toolkit/skills/download-yt/download_yt.py "URL" -o ~/Videos

   # Audio only (mp3)
   python3 ~/dev/dzen-dev-toolkit/skills/download-yt/download_yt.py "URL" -a
   ```

2. **Report the result** — the script prints the downloaded file path to stdout

## Arguments

- First argument: YouTube URL (required)
- `-o <dir>` — output directory (default: `~/Downloads`)
- `-a` — audio only (extracts mp3)
- `-f <format>` — custom yt-dlp format string

## Prerequisites

- `yt-dlp` — `brew install yt-dlp`
