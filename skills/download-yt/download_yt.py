#!/usr/bin/env python3
"""Skill 1: Download YouTube video via yt-dlp."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys


DEFAULT_OUTPUT_DIR = "~/Downloads"
DEFAULT_FORMAT = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
MAX_AGE_DAYS = 90


def check_ytdlp_version():
    try:
        result = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("ERROR: yt-dlp not found. Install with: brew install yt-dlp", file=sys.stderr)
            sys.exit(1)
        from datetime import datetime
        version_date = datetime.strptime(result.stdout.strip(), "%Y.%m.%d")
        age = (datetime.now() - version_date).days
        if age > MAX_AGE_DAYS:
            print(f"WARNING: yt-dlp is {age} days old ({result.stdout.strip()}). "
                  f"YouTube may block downloads. Update with: brew upgrade yt-dlp", file=sys.stderr)
    except (ValueError, FileNotFoundError):
        pass


def download(url: str, output_dir: str = DEFAULT_OUTPUT_DIR, audio_only: bool = False, format_str: str | None = None) -> str | None:
    output_dir = os.path.expanduser(output_dir)
    cmd = ["yt-dlp", "-o", f"{output_dir}/%(title)s.%(ext)s", "--print", "after_move:filepath"]

    if audio_only:
        cmd += ["-x", "--audio-format", "mp3"]
    elif format_str:
        cmd += ["-f", format_str]
    else:
        cmd += ["-f", DEFAULT_FORMAT]

    cmd.append(url)

    print(f"Downloading to {output_dir} ...", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        return None

    filepath = result.stdout.strip().split("\n")[-1]
    print(f"Downloaded: {filepath}", file=sys.stderr)
    return filepath


def main():
    parser = argparse.ArgumentParser(description="Download YouTube video")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("-a", "--audio", action="store_true", help="Audio only (mp3)")
    parser.add_argument("-f", "--format", help="Custom yt-dlp format string")
    args = parser.parse_args()

    check_ytdlp_version()
    filepath = download(args.url, args.output, args.audio, args.format)
    if not filepath:
        sys.exit(1)
    print(filepath)


if __name__ == "__main__":
    main()
