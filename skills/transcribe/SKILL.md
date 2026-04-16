---
name: transcribe
description: Transcribe video/audio to timestamped .md using whisper.cpp (large-v3-turbo)
---

# Transcribe

Transcribe a video or audio file to a timestamped markdown file using whisper.cpp.

## Steps

1. **Run the script:**
   ```bash
   python3 ~/dev/dzen-dev-toolkit/skills/transcribe/transcribe.py "/path/to/video.mp4"

   # With language hint (faster than auto-detect)
   python3 ~/dev/dzen-dev-toolkit/skills/transcribe/transcribe.py "/path/to/video.mp4" -l ru
   ```

2. **Report the result** — tell the user the .md file path

## Output format

The .md file contains timestamped transcript:
```
# Video Title

**[0:00]** First segment of text...

**[0:15]** Next segment...
```

## Prerequisites

- `ffmpeg` — `brew install ffmpeg`
- `whisper-cpp` — `brew install whisper-cpp`
- Whisper model at `~/.local/share/whisper-models/ggml-large-v3-turbo.bin`
