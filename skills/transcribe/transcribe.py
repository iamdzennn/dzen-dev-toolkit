#!/usr/bin/env python3
"""Skill 2: Transcribe video/audio to .md using whisper.cpp with timestamps."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


WHISPER_MODEL = "~/.local/share/whisper-models/ggml-large-v3-turbo.bin"


def format_timestamp(ms: int) -> str:
    s = ms // 1000
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def transcribe(filepath: str, language: str = "auto") -> str | None:
    model_path = os.path.expanduser(WHISPER_MODEL)
    if not os.path.exists(model_path):
        print(f"ERROR: Whisper model not found at {model_path}", file=sys.stderr)
        print(f"Download: curl -L https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin -o {WHISPER_MODEL}", file=sys.stderr)
        return None

    # Convert to WAV (whisper.cpp requires 16kHz mono WAV)
    wav_path = filepath + ".wav"
    print("Converting to WAV...", file=sys.stderr)
    conv = subprocess.run(
        ["ffmpeg", "-i", filepath, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", wav_path, "-y"],
        capture_output=True, text=True,
    )
    if conv.returncode != 0:
        print(f"ERROR: ffmpeg failed: {conv.stderr}", file=sys.stderr)
        return None

    # Run whisper-cli with JSON output (includes timestamps)
    output_base = os.path.splitext(filepath)[0]
    print("Transcribing with whisper.cpp (large-v3-turbo)...", file=sys.stderr)

    cmd = [
        "whisper-cli",
        "-m", model_path,
        "-f", wav_path,
        "-l", language,
        "-oj",  # JSON output
        "-of", output_base,
    ]
    result = subprocess.run(cmd)
    os.remove(wav_path)

    if result.returncode != 0:
        print("ERROR: whisper transcription failed", file=sys.stderr)
        return None

    # Parse JSON and build timestamped .md
    json_path = output_base + ".json"
    md_path = output_base + ".md"

    if not os.path.exists(json_path):
        print("ERROR: whisper JSON output not found", file=sys.stderr)
        return None

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    title = Path(filepath).stem
    lines = [f"# {title}\n"]

    for seg in data.get("transcription", []):
        ts_start = seg["offsets"]["from"]
        ts_end = seg["offsets"]["to"]
        text = seg["text"].strip()
        if text:
            lines.append(f"**[{format_timestamp(ts_start)}]** {text}\n")

    Path(md_path).write_text("\n".join(lines), encoding="utf-8")
    os.remove(json_path)

    print(f"Transcript saved: {md_path}", file=sys.stderr)
    return md_path


def main():
    parser = argparse.ArgumentParser(description="Transcribe video/audio to .md")
    parser.add_argument("filepath", help="Path to video or audio file")
    parser.add_argument("-l", "--language", default="auto", help="Language (default: auto)")
    args = parser.parse_args()

    md_path = transcribe(args.filepath, args.language)
    if not md_path:
        sys.exit(1)
    print(md_path)


if __name__ == "__main__":
    main()
