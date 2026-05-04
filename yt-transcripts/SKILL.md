---
name: yt-transcripts
description: Use when the user wants to extract or pull transcripts from one or more YouTube videos — including phrasings like "get the transcript", "pull transcripts", "transcribe these videos", or the /yt-transcripts slash command. Fetches captions via youtube-transcript-api and writes one minimal markdown file per video to the Obsidian vault.
---

# YouTube Transcript Extractor

## Overview

Given one or more YouTube URLs, fetch each video's transcript (auto-generated or manual captions) and write one minimal `.md` file per video to the configured output directory.

Output directory is set via the `YT_TRANSCRIPTS_DIR` env var, defaulting to `~/youtube-transcripts/`. See `README.md` for setup.

Each file contains: title (H1), URL, and plain transcript text. Nothing else.

## When to Use

- User invokes `/yt-transcripts <url> [<url> ...]`
- User pastes YouTube URLs and asks for transcripts, captions, or to "transcribe these"
- User says "pull the transcript from this video"

## When NOT to Use

- User wants a *summary* of a video → fetch transcript with this skill first, then summarize separately
- User wants audio/video download → use yt-dlp directly, not this skill
- User wants live captions or non-YouTube sources → out of scope

## Inputs

A whitespace- or comma-separated string of YouTube URLs. Accepts any of:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/shorts/VIDEO_ID`
- `https://m.youtube.com/watch?v=VIDEO_ID`

URLs may include extra query params (e.g., `&t=120s`); the script strips them.

If the user invokes the command with no URLs, ask them to paste the links.

## Workflow

1. **Verify dependency.** Check whether `youtube-transcript-api` is importable:
   ```bash
   python3 -c "import youtube_transcript_api" 2>&1
   ```
   If it fails with `ModuleNotFoundError`, install it once:
   ```bash
   pip3 install --user --quiet youtube-transcript-api
   ```
   Then re-verify. If install fails, report the error to the user and stop.

2. **Run the fetcher.** Pass all URLs as args to `fetch.py` in this skill folder:
   ```bash
   python3 ~/.claude/skills/yt-transcripts/fetch.py <url1> <url2> ...
   ```
   The script handles everything: parsing video IDs, fetching titles, fetching transcripts, sanitizing filenames, writing files. It prints one line per URL (success path or failure reason) and exits 0 even on per-video failures.

3. **Report results.** Relay the script's output to the user. For each success, show the absolute file path. For each failure, show the URL and the reason (e.g., "transcripts disabled", "video unavailable").

## Output Format

Each `.md` file is minimal:

```markdown
# <Video Title>

https://www.youtube.com/watch?v=<video_id>

<plain transcript text, paragraphs separated by blank lines>
```

No frontmatter. No timestamps. No channel/date metadata.

## File Naming

`<sanitized_title>.md`, where sanitization:
- Strips characters illegal on macOS/Obsidian: `/ \ : * ? " < > |`
- Collapses whitespace
- Trims to 120 chars
- Falls back to `<video_id>.md` if title fetch fails

If a file with the same name already exists, **overwrite it** (re-running refreshes the transcript).

## Error Handling

- Per-video failures must not stop the batch. The script continues to the next URL.
- Common failure modes the script handles: transcripts disabled, no transcript in any language, video unavailable, age-restricted, invalid URL.
- If ALL videos fail, report the failures clearly so the user can debug.
