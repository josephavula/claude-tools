# yt-transcripts

A Claude Code skill + slash command that pulls transcripts from one or more YouTube videos and writes one minimal markdown file per video.

Paste any number of YouTube links after `/yt-transcripts`. Each video becomes its own `.md` file, named after the video title.

## Output format

Each file is minimal — title, URL, plain transcript text. No frontmatter, no timestamps.

```markdown
# Inside the Mind of a Master Procrastinator | Tim Urban | TED

https://www.youtube.com/watch?v=arj7oStGLkU

So in college, I was a government major, which means I had to write a lot of papers...
```

## Requirements

- Python 3.9+
- `youtube-transcript-api` (the skill installs it on first run if missing)
- Claude Code

## Install

1. **Copy the skill files** to your Claude Code skills folder:
   ```bash
   mkdir -p ~/.claude/skills/yt-transcripts
   cp SKILL.md fetch.py ~/.claude/skills/yt-transcripts/
   ```

2. **Copy the slash command file** to your commands folder:
   ```bash
   cp yt-transcripts.md ~/.claude/commands/
   ```

3. **(Optional) Set your output directory.** Defaults to `~/youtube-transcripts/`. To send transcripts somewhere else (e.g., an Obsidian vault), set the env var in your shell profile:
   ```bash
   export YT_TRANSCRIPTS_DIR="$HOME/Documents/Obsidian Vault/Transcripts"
   ```

4. **(Optional) Pre-install the Python dep** to skip the first-run install prompt:
   ```bash
   pip3 install --user youtube-transcript-api
   ```

## Use

In Claude Code:

```
/yt-transcripts https://youtu.be/abc123 https://www.youtube.com/watch?v=def456
```

Accepts:
- Space-, comma-, or newline-separated URLs
- `youtube.com/watch?v=`, `youtu.be/`, `youtube.com/shorts/`, `m.youtube.com/`
- URLs with extra query params (`&t=120s` etc.)

The skill reports the file path written for each video, or the failure reason (transcripts disabled, video unavailable, etc.).

## How it works

1. Slash command (`~/.claude/commands/yt-transcripts.md`) hands the URLs to the skill
2. Skill (`SKILL.md`) verifies/installs the Python dep, then runs `fetch.py`
3. `fetch.py` extracts video IDs, fetches transcripts via `youtube-transcript-api`, fetches titles via YouTube's public oEmbed endpoint (no API key), and writes one minimal markdown file per video

## Limitations

- Videos with disabled captions can't be transcribed (you'll get a clear failure message)
- Age-restricted and region-locked videos may fail
- Transcripts are plain text only — if you need timestamps, edit `fetch.py` to keep the `start` field from each snippet
