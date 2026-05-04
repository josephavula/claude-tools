#!/usr/bin/env python3
"""Fetch YouTube transcripts and write minimal markdown files."""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

# Override with env var YT_TRANSCRIPTS_DIR. Defaults to ~/youtube-transcripts.
OUTPUT_DIR = Path(
    os.environ.get("YT_TRANSCRIPTS_DIR")
    or Path.home() / "youtube-transcripts"
).expanduser()

ILLEGAL = re.compile(r'[\\/:*?"<>|]')
WHITESPACE = re.compile(r"\s+")


def extract_video_id(url: str) -> str | None:
    url = url.strip().strip(",")
    if not url:
        return None
    try:
        p = urllib.parse.urlparse(url)
    except ValueError:
        return None
    host = (p.netloc or "").lower().lstrip("www.").lstrip("m.")
    if host == "youtu.be":
        vid = p.path.lstrip("/").split("/", 1)[0]
    elif host in ("youtube.com", "music.youtube.com"):
        if p.path == "/watch":
            qs = urllib.parse.parse_qs(p.query)
            vid = (qs.get("v") or [""])[0]
        elif p.path.startswith(("/shorts/", "/embed/", "/v/")):
            vid = p.path.split("/", 2)[2].split("/", 1)[0]
        else:
            vid = ""
    else:
        vid = ""
    vid = vid.split("?", 1)[0].split("&", 1)[0]
    return vid if re.fullmatch(r"[A-Za-z0-9_-]{11}", vid) else None


def fetch_title(video_id: str) -> str | None:
    """Use YouTube's public oEmbed endpoint — no auth, returns title."""
    api = (
        "https://www.youtube.com/oembed?format=json&url="
        + urllib.parse.quote(f"https://www.youtube.com/watch?v={video_id}", safe="")
    )
    try:
        req = urllib.request.Request(api, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode("utf-8"))
        return data.get("title")
    except Exception:
        return None


def fetch_transcript(video_id: str) -> tuple[list[dict] | None, str | None]:
    """Returns (snippets, error_message). snippets is list of {'text': str}."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import (
            TranscriptsDisabled,
            NoTranscriptFound,
            VideoUnavailable,
        )
    except ImportError as e:
        return None, f"youtube-transcript-api not installed: {e}"

    try:
        # Newer instance-based API (>=1.0)
        if hasattr(YouTubeTranscriptApi, "fetch") and not hasattr(
            YouTubeTranscriptApi, "get_transcript"
        ):
            api = YouTubeTranscriptApi()
            fetched = api.fetch(video_id)
            snippets = [{"text": s.text} for s in fetched]
        else:
            # Older static API
            raw = YouTubeTranscriptApi.get_transcript(video_id)
            snippets = [{"text": s["text"]} for s in raw]
        return snippets, None
    except TranscriptsDisabled:
        return None, "transcripts disabled for this video"
    except NoTranscriptFound:
        return None, "no transcript available in any language"
    except VideoUnavailable:
        return None, "video unavailable (private, deleted, or region-locked)"
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def format_transcript(snippets: list[dict]) -> str:
    """Join chunks into paragraphs. Plain text, no timestamps."""
    full = " ".join(s["text"].replace("\n", " ").strip() for s in snippets if s["text"].strip())
    full = WHITESPACE.sub(" ", full).strip()
    # Break into paragraphs at sentence boundaries every ~500 chars for readability.
    paragraphs = []
    buf = []
    count = 0
    for sentence in re.split(r"(?<=[.!?])\s+", full):
        buf.append(sentence)
        count += len(sentence)
        if count >= 500:
            paragraphs.append(" ".join(buf))
            buf, count = [], 0
    if buf:
        paragraphs.append(" ".join(buf))
    return "\n\n".join(paragraphs) if paragraphs else full


def sanitize_filename(name: str, fallback: str) -> str:
    name = ILLEGAL.sub("", name)
    name = WHITESPACE.sub(" ", name).strip()
    if not name:
        return fallback
    return name[:120].rstrip(" .")


def process(url: str) -> str:
    video_id = extract_video_id(url)
    if not video_id:
        return f"FAIL\t{url}\tinvalid YouTube URL"

    snippets, err = fetch_transcript(video_id)
    if err:
        return f"FAIL\t{url}\t{err}"

    title = fetch_title(video_id)
    filename = sanitize_filename(title or "", fallback=video_id) + ".md"
    out_path = OUTPUT_DIR / filename

    body = (
        f"# {title or video_id}\n\n"
        f"https://www.youtube.com/watch?v={video_id}\n\n"
        f"{format_transcript(snippets)}\n"
    )
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(body, encoding="utf-8")
    return f"OK\t{out_path}"


def main():
    args = sys.argv[1:]
    # Allow comma-separated input as a single arg too.
    urls = []
    for a in args:
        urls.extend(part for part in re.split(r"[\s,]+", a) if part)
    if not urls:
        print("usage: fetch.py <url> [<url> ...]", file=sys.stderr)
        sys.exit(2)
    for url in urls:
        print(process(url), flush=True)


if __name__ == "__main__":
    main()
