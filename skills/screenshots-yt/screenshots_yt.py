#!/usr/bin/env python3
"""Skill 4: Extract screenshots from video at timestamps recommended in summary."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def parse_timestamps(summary_path: str) -> list[dict]:
    """Parse timestamps from summary .md file.

    Expected format in summary:
      - **[MM:SS]** — description
      - **[H:MM:SS]** — description
    """
    content = Path(summary_path).read_text(encoding="utf-8")
    pattern = r"\*\*\[(\d+(?::\d+)?(?::\d+)?)\]\*\*\s*[—-]\s*(.+?)(?=\n|$)"
    matches = re.findall(pattern, content)

    result = []
    for ts, desc in matches:
        result.append({"timestamp": ts, "description": desc.strip()})
    return result


def ts_to_seconds(ts: str) -> int:
    """Convert MM:SS or H:MM:SS to seconds."""
    parts = ts.split(":")
    if len(parts) == 2:
        m, s = parts
        return int(m) * 60 + int(s)
    elif len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + int(s)
    return int(ts)


def slug_from_desc(desc: str, max_len: int = 40) -> str:
    """Generate a safe filename slug from description."""
    # Take first N chars, replace non-alphanumeric with dash
    text = desc[:max_len]
    slug = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    slug = re.sub(r"[\s_-]+", "-", slug).strip("-").lower()
    return slug or "shot"


def extract_screenshot(video_path: str, seconds: int, output_path: str) -> bool:
    """Extract single frame at given time using ffmpeg."""
    cmd = [
        "ffmpeg",
        "-ss", str(seconds),
        "-i", video_path,
        "-frames:v", "1",
        "-q:v", "2",
        output_path,
        "-y",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Extract screenshots from video at timestamps in summary")
    parser.add_argument("summary", help="Path to summary .md with timestamps")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("-o", "--output-dir", help="Output dir (default: next to video)")
    args = parser.parse_args()

    timestamps = parse_timestamps(args.summary)
    if not timestamps:
        print("ERROR: no timestamps found in summary", file=sys.stderr)
        sys.exit(1)

    video_path = Path(args.video)
    if not video_path.exists():
        print(f"ERROR: video not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    # Output dir: <video_basename>_screenshots/ next to video
    if args.output_dir:
        out_dir = Path(args.output_dir)
    else:
        out_dir = video_path.parent / f"{video_path.stem}_screenshots"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Extracting {len(timestamps)} screenshots to {out_dir}...", file=sys.stderr)

    saved = []
    for ts_data in timestamps:
        ts = ts_data["timestamp"]
        desc = ts_data["description"]
        seconds = ts_to_seconds(ts)
        safe_ts = ts.replace(":", "-")
        slug = slug_from_desc(desc)
        filename = f"{safe_ts}_{slug}.jpg"
        output_path = out_dir / filename

        if extract_screenshot(str(video_path), seconds, str(output_path)):
            print(f"  [{ts}] → {filename}", file=sys.stderr)
            saved.append({"timestamp": ts, "file": str(output_path), "description": desc})
        else:
            print(f"  [{ts}] FAILED", file=sys.stderr)

    print(json.dumps({"dir": str(out_dir), "screenshots": saved}, ensure_ascii=False))


if __name__ == "__main__":
    main()
