Pull YouTube transcripts for: $ARGUMENTS

Invoke the `yt-transcripts` skill via the Skill tool. Pass the full argument string (the URLs) through. Follow the skill's workflow exactly — fetch each transcript, write one minimal markdown file per video to the vault's `raw/youtube-transcripts/` folder, and report each written file path back to the user. If `$ARGUMENTS` is empty, ask the user to paste the URLs.
