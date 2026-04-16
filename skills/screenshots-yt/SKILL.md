---
name: screenshots-yt
description: Extract screenshots from video at timestamps recommended in summary .md
---

# Extract Screenshots from Video

Parse timestamps from a summary .md file and extract frames from the video using ffmpeg.

## Usage

```bash
python3 ~/dev/dzen-dev-toolkit/skills/screenshots-yt/screenshots_yt.py "<summary.md>" "<video>"

# Custom output dir
python3 ~/dev/dzen-dev-toolkit/skills/screenshots-yt/screenshots_yt.py "<summary.md>" "<video>" -o ~/screens
```

## Output

- Default: `<video_basename>_screenshots/` next to the video file
- Filename format: `{MM-SS}_{short-description}.jpg`

## Prerequisites

- `ffmpeg` — `brew install ffmpeg`
- Summary .md must have timestamps in format `**[MM:SS]** — description` or `**[H:MM:SS]** — description`
