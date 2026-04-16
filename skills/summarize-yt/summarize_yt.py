#!/usr/bin/env python3
"""Skill 3: Summarize transcript via GPT-5.4, rename files, optionally save to dzen-os."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Load API keys
for env_path in [
    Path.home() / ".config" / "dzen-dev-toolkit" / ".env.master",
    Path.cwd() / ".env",
]:
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv(env_path)
        break

SUMMARY_PROMPT = """\
Ты — эксперт по анализу видео-контента. Тебе дан транскрипт видео с YouTube с таймкодами.

Сделай подробное структурированное саммари на русском языке.

## Структура ответа

Ответ ДОЛЖЕН быть валидным JSON со следующими полями:

```json
{
  "slug": "short-name-in-latin-3-5-words",
  "title": "Полное название видео на русском",
  "event": "Название ивента/стрима если есть, иначе null",
  "date": "YYYY-MM-DD дата видео если можно определить, иначе null",
  "participants": ["Имя1", "Имя2"],
  "organizer": "Кто организовал / чей канал",
  "summary": "2-3 предложения — о чём видео, для кого, главный посыл",
  "key_ideas": ["Идея 1", "Идея 2", "..."],
  "workflows": ["Workflow 1: описание", "..."],
  "recommendations": ["Рекомендация 1", "..."],
  "screenshots": [
    {"timestamp": "MM:SS", "description": "что на экране и зачем скриншот"}
  ]
}
```

Правила:
- slug: 3-5 слов, латиницей, через дефис, без спецсимволов
- key_ideas: конкретные мысли, не общие слова. Минимум 5 пунктов.
- workflows: конкретные процессы, методологии, пошаговые инструкции из видео
- screenshots: таймкоды где показано что-то визуально важное (схемы, слайды, демо)
- participants: имена всех участников видео
- Весь текст на русском, кроме slug

Верни ТОЛЬКО JSON, без markdown-обёрток.
"""


def summarize(transcript_path: str) -> dict | None:
    from openai import OpenAI

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set", file=sys.stderr)
        return None

    transcript = Path(transcript_path).read_text(encoding="utf-8")
    client = OpenAI(api_key=api_key)

    print("Sending transcript to GPT-5.4 for summary...", file=sys.stderr)
    response = client.chat.completions.create(
        model="gpt-5.4",
        messages=[
            {"role": "system", "content": SUMMARY_PROMPT},
            {"role": "user", "content": transcript},
        ],
        reasoning_effort="high",
    )

    raw = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print("WARNING: GPT returned non-JSON, saving as-is", file=sys.stderr)
        return {"slug": "video", "summary_raw": raw}


def build_summary_md(data: dict) -> str:
    """Build a readable .md from structured summary data."""
    lines = [f"# {data.get('title', 'Video Summary')}\n"]

    if data.get("event"):
        lines.append(f"**Ивент:** {data['event']}")
    if data.get("date"):
        lines.append(f"**Дата:** {data['date']}")
    if data.get("organizer"):
        lines.append(f"**Организатор:** {data['organizer']}")
    if data.get("participants"):
        lines.append(f"**Участники:** {', '.join(data['participants'])}")
    lines.append("")

    if data.get("summary"):
        lines.append(f"## Суть\n\n{data['summary']}\n")

    if data.get("key_ideas"):
        lines.append("## Ключевые мысли и идеи\n")
        for i, idea in enumerate(data["key_ideas"], 1):
            lines.append(f"{i}. {idea}")
        lines.append("")

    if data.get("workflows"):
        lines.append("## Полезные workflows и практики\n")
        for w in data["workflows"]:
            lines.append(f"- {w}")
        lines.append("")

    if data.get("recommendations"):
        lines.append("## Рекомендации\n")
        for r in data["recommendations"]:
            lines.append(f"- {r}")
        lines.append("")

    if data.get("screenshots"):
        lines.append("## Скриншоты для захвата\n")
        for s in data["screenshots"]:
            lines.append(f"- **[{s['timestamp']}]** — {s['description']}")
        lines.append("")

    if data.get("summary_raw"):
        lines.append(data["summary_raw"])

    return "\n".join(lines)


def build_dzen_os_raw(data: dict, youtube_url: str, summary_md: str) -> str:
    """Build a dzen-os raw/ file with proper frontmatter."""
    title = data.get("title", "YouTube Video")
    date = data.get("date") or datetime.now().strftime("%Y-%m-%d")
    organizer = data.get("organizer", "Unknown")
    participants = data.get("participants", [])
    event = data.get("event", "")

    frontmatter = f"""---
title: "{title}"
source: youtube
author: "{organizer}"
date: {date}
url: "{youtube_url}"
type: video-analysis
event: "{event}"
participants: {json.dumps(participants, ensure_ascii=False)}
tags: []
---"""

    overview = f"""## Overview

- **Видео:** {title}
- **Источник:** YouTube
- **Ивент:** {event or 'N/A'}
- **Дата:** {date}
- **Организатор:** {organizer}
- **Участники:** {', '.join(participants) if participants else 'N/A'}
- **URL:** {youtube_url}
"""

    return f"{frontmatter}\n\n{overview}\n{summary_md}"


def rename_files(video_path: str, transcript_path: str, summary_path: str, slug: str) -> dict:
    """Rename all 3 files to: {YYYYMMDD_HHMM}_{slug}.{ext}"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    base_name = f"{timestamp}_{slug}"

    result = {}
    for label, old_path in [("video", video_path), ("transcript", transcript_path), ("summary", summary_path)]:
        p = Path(old_path)
        new_path = p.parent / f"{base_name}{p.suffix}"
        if new_path.exists() and new_path != p:
            new_path = p.parent / f"{base_name}_{label}{p.suffix}"
        p.rename(new_path)
        result[label] = str(new_path)
        print(f"Renamed {label}: {p.name} → {new_path.name}", file=sys.stderr)

    return result


def save_to_dzen_os(data: dict, youtube_url: str, summary_md: str, slug: str) -> str | None:
    """Save analysis to dzen-os/raw/ with proper frontmatter."""
    dzen_os_path = Path.home() / "dev" / "dzen-os" / "raw"
    if not dzen_os_path.exists():
        print("WARNING: dzen-os/raw/ not found at ~/dev/dzen-os/raw/", file=sys.stderr)
        return None

    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    filename = f"{timestamp}-{slug}.md"
    filepath = dzen_os_path / filename

    content = build_dzen_os_raw(data, youtube_url, summary_md)
    filepath.write_text(content, encoding="utf-8")
    print(f"Saved to dzen-os: {filepath}", file=sys.stderr)
    return str(filepath)


def main():
    parser = argparse.ArgumentParser(description="Summarize transcript via GPT-5.4 and rename files")
    parser.add_argument("transcript", help="Path to transcript .md file")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("--url", help="Original YouTube URL (for dzen-os metadata)")
    parser.add_argument("--save-to-dzen-os", action="store_true", help="Save analysis to ~/dev/dzen-os/raw/")
    args = parser.parse_args()

    data = summarize(args.transcript)
    if not data:
        sys.exit(1)

    slug = data.get("slug", "video")
    summary_md = build_summary_md(data)

    # Save summary file
    summary_path = os.path.splitext(args.transcript)[0] + "_summary.md"
    Path(summary_path).write_text(summary_md, encoding="utf-8")
    print(f"Summary saved: {summary_path}", file=sys.stderr)

    # Rename all files
    paths = rename_files(args.video, args.transcript, summary_path, slug)

    # Optionally save to dzen-os
    if args.save_to_dzen_os:
        url = args.url or ""
        dzen_path = save_to_dzen_os(data, url, summary_md, slug)
        if dzen_path:
            paths["dzen_os"] = dzen_path

    # Output final paths as JSON
    print(json.dumps(paths, ensure_ascii=False))


if __name__ == "__main__":
    main()
