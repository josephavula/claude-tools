# linkedin-apollo-research

A Claude Code skill that automates building structured contact profiles for employees at a target company — using LinkedIn and Apollo.io via the Claude Chrome extension.

Built by a supply chain student who needed a faster way to research people before outreach. Now free and open source.

---

## What This Is

You give it a company name and a LinkedIn URL. It opens Chrome, navigates LinkedIn to find employees at a target seniority level, cross-references each person on Apollo.io, and writes one structured `.md` file per person to a folder of your choice.

No scraping APIs. No code. Just Claude navigating your browser the same way you would — but faster.

---

## What You'll Get

One `.md` file per person with:
- Name, title, company, location
- Email and phone (when Apollo exposes it)
- LinkedIn bio and background
- Key strengths inferred from their profile
- A practical "how to network with them" section
- Notable context for outreach

**See a full example:** [`examples/sample_output.md`](examples/sample_output.md)

---

## Requirements

| Requirement | Notes |
|---|---|
| [Claude Chrome Extension](https://chromewebstore.google.com/detail/claude/pmaeehhfomkghjfbblmeonlendoibenb) | Gives Claude access to your live Chrome session. Install it, then enable browser access in Claude.ai settings. |
| LinkedIn account | **Use a burner/secondary account.** LinkedIn detects and bans automated browsing. Don't risk your main account. |
| Apollo.io account | Free tier works. Exposes: job title, company, LinkedIn URL, and sometimes email. Paid tiers add direct phone and verified email. |

---

## Setup

1. Install the [Claude Chrome Extension](https://chromewebstore.google.com/detail/claude/pmaeehhfomkghjfbblmeonlendoibenb) and enable browser access in Claude.ai
2. Open Chrome with a dedicated profile (not your default)
3. Log into LinkedIn (burner account) in that profile
4. Log into Apollo.io in that profile
5. Open Claude Cowork (claude.ai) in the same profile

---

## How to Use

1. Copy the contents of `SKILL.md` into your Claude Cowork session
2. When prompted, fill in:
   - `TARGET_COMPANY` — company name (e.g., `Daybreak AI`)
   - `LINKEDIN_COMPANY_URL` — the company's LinkedIn URL (e.g., `https://www.linkedin.com/company/daybreak-ai`)
   - `SENIORITY_FILTER` — which levels to include (e.g., `C-Suite, VP` or `Director and above`)
   - `OUTPUT_DIRECTORY` — where to save the files (e.g., `~/Desktop/research/`)
3. Run the agent prompt and let Claude work through each person one at a time

Each person gets their own `.md` file. If Apollo has no data for someone, Claude notes it and continues. If a LinkedIn profile is private, Claude captures what's visible and moves on.

---

## Adapting It

The skill includes an "Adapting This Skill" section with suggestions for:
- Sales prospecting (add a "Pitch Angle" section)
- Investor research (swap Apollo for Crunchbase)
- Academic or nonprofit targets
- Wider seniority filters
- CSV export for CRM import

---

## Risk Note

LinkedIn will ban accounts that show automated browsing behavior. This is a soft risk on the first run, but it compounds with repeated use. **Use a burner account.** This warning is in the skill itself, but it's worth repeating here.

---

## License

MIT. Use it, modify it, build on it.
