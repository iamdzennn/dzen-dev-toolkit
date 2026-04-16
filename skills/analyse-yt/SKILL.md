---
name: analyse-yt
description: Full YouTube pipeline — download, transcribe, summarize with GPT-5.4, save to dzen-os knowledge base
---

# Analyse YouTube Video

Full pipeline: download → transcribe → summarize → save to knowledge base.

## Usage

`/analyse-yt <youtube-url> [language]`

- `language` — optional, language hint for transcription (e.g. `ru`, `en`). Default: `auto`

## Pipeline

### Step 1: Download video

```bash
python3 ~/dev/dzen-dev-toolkit/skills/download-yt/download_yt.py "<URL>"
```

Capture stdout — it prints the downloaded file path.

### Step 2: Transcribe

```bash
python3 ~/dev/dzen-dev-toolkit/skills/transcribe/transcribe.py "<video_path>" -l <language>
```

Capture stdout — it prints the .md transcript path.
Tell the user transcription is in progress — it takes a while for long videos.

### Step 3: Summarize + Rename

```bash
python3 ~/dev/dzen-dev-toolkit/skills/summarize-yt/summarize_yt.py "<transcript_path>" "<video_path>" --url "<original_youtube_url>" --save-to-dzen-os
```

Capture stdout — it prints JSON with final paths:
```json
{"video": "...", "transcript": "...", "summary": "...", "dzen_os": "..."}
```

**IMPORTANT:** Always pass `--url` with the original YouTube URL and `--save-to-dzen-os` to save analysis to the knowledge base at `~/dev/dzen-os/raw/`.

### Step 4: Extract screenshots

```bash
python3 ~/dev/dzen-dev-toolkit/skills/screenshots-yt/screenshots_yt.py "<summary_path>" "<video_path>"
```

Extracts frames at all timestamps the summarizer recommended. Saves to `<video_basename>_screenshots/` next to the video.

### Step 5: Show results to user

1. Read the summary .md file and present key highlights
2. List the recommended screenshot timestamps + path to screenshots folder
3. Show the final file names
4. If saved to dzen-os, mention the path

## Error handling

- If any step fails, stop and tell the user which step failed and why
- If yt-dlp is outdated, suggest: `brew upgrade yt-dlp`
- If whisper model is missing, the script will print the download command

## Example

User: `/analyse-yt https://youtube.com/watch?v=xxx ru`

Expected flow:
1. "Скачиваю видео..." → `~/Downloads/Video Title.mp4`
2. "Транскрибирую (whisper large-v3-turbo)..." → `~/Downloads/Video Title.md`
3. "Отправляю в GPT-5.4 для анализа..." → renames all to `20260415_2030_video-slug.{ext}`
4. "Сохраняю в базу знаний dzen-os..." → `~/dev/dzen-os/raw/2026-04-15-203000-video-slug.md`
5. Показывает саммари с идеями и таймкодами для скриншотов
