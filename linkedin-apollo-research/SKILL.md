---
name: linkedin-apollo-research
description: >
  Use this skill whenever the user wants to research employees at a company for networking,
  outreach, or sales prospecting. Triggers when the user asks to find contacts, pull leadership
  at a company, research executives, build a contact list, or scout a company's team.
  Automates browser navigation across LinkedIn and Apollo.io to build structured .md profiles
  for each person found. Use this skill even if the user just says "research [Company] for me"
  or "find me contacts at [Company]".
compatibility:
  tools:
    - Claude Chrome extension (Cowork / Claude in Chrome)
  accounts:
    - LinkedIn (burner account strongly recommended — see risk note below)
    - Apollo.io (free tier works)
---

# LinkedIn + Apollo Research Skill

Automates building structured contact profiles for employees at a target company by navigating LinkedIn and Apollo.io in a live Chrome browser session.

---

## Risk Note — LinkedIn

LinkedIn actively detects and bans automated browsing. **Use a burner (secondary) LinkedIn account**, not your main one. If you only have one account, proceed at your own risk or skip LinkedIn and use Apollo alone.

---

## What You'll Get

One `.md` file per person. Each file looks like this:

```
# Jensen Huang — CEO, NVIDIA

## Quick Snapshot
| | |
|---|---|
| Title | CEO & Co-Founder |
| Company | NVIDIA |
| Location | Santa Clara, CA |
| Email | (from Apollo, if available) |
| LinkedIn | linkedin.com/in/jensenhuang |

## About
[Bio pulled from LinkedIn profile]

## Key Strengths
[Inferred from their background and content]

## How to Network With Them
[Practical angle — what they care about, best entry point]

## Notable Context
[Anything useful for outreach or research]
```

See `examples/sample_output.md` for a full example.

---

## Requirements

**Claude Chrome Extension** — This skill requires Claude to have access to your live Chrome browser session. The extension is called *Claude* (by Anthropic) and is available in the Chrome Web Store. Once installed, open Claude.ai in your browser and enable "Computer use" / browser access in the settings. This is what lets Claude navigate LinkedIn and Apollo on your behalf.

**Apollo.io Free Tier** — Free tier exposes: job title, company, LinkedIn URL, and sometimes email. Paid tiers expose direct phone numbers, verified emails, and full career history. This skill works on free — you'll just get less contact data.

---

## User Inputs (Required Before Running)

Ask the user for these before starting if not already provided:

| Variable | Example |
|---|---|
| `TARGET_COMPANY` | Daybreak AI |
| `LINKEDIN_COMPANY_URL` | https://www.linkedin.com/company/daybreak-ai |
| `SENIORITY_FILTER` | C-Suite, VP (default) — adjust to taste |
| `OUTPUT_DIRECTORY` | ~/Desktop/research/ (or specify a path) |

---

## Setup Checklist

Before running the agent prompt, confirm:

1. Chrome is open with a dedicated profile (not your default)
2. Claude Chrome extension is active in that profile
3. LinkedIn is logged in (burner account)
4. Apollo.io is logged in

---

## Agent Prompt

Paste this into Claude Cowork. Fill in the bracketed variables. No file attachment needed — the format template is embedded below.

```
You have access to my Chrome browser. LinkedIn and Apollo.io are already logged in.

Your goal: build a structured .md profile for every [SENIORITY_FILTER] employee at [TARGET_COMPANY].

**Step 1 — LinkedIn**
Go to: [LINKEDIN_COMPANY_URL]/people
Filter by seniority or scan manually. Identify all employees at [SENIORITY_FILTER] level only.
For each person, note:
- Full name
- Title
- LinkedIn URL
- Anything notable from their profile (bio, posts, background)

**Step 2 — Apollo.io**
For each person identified, go to Apollo.io and search their name + company.
Pull whatever is available: email, phone, location, career history.
If Apollo has no data for someone, note that in their file and continue — do not skip them.

**Step 3 — Create files**
For each person, create one .md file named: [TARGET_COMPANY]_FirstName_LastName.md
Save all files to: [OUTPUT_DIRECTORY]

Use the following format template exactly:

---
# [Full Name] — [Title], [Company]

## Quick Snapshot
| | |
|---|---|
| **Title** | [job title] |
| **Company** | [company name] |
| **Location** | [city, state/country] |
| **Email** | [email or "Not available"] |
| **Phone** | [phone or "Not available (locked on Apollo)"] |
| **LinkedIn** | [LinkedIn URL] |

---

## About
[2–4 sentence bio pulled from their LinkedIn profile. Include education, current focus, notable career history, and anything that stands out.]

---

## Key Strengths
- [Strength 1 — inferred from their background or content]
- [Strength 2]
- [Strength 3]

---

## How to Network With Them
[1–3 sentences on the best angle for outreach. What do they care about? What's the warm entry point? What tone works?]

---

## Notable Context
- [Any detail useful for outreach: niche firm context, recent posts, tools they mention, stage on Apollo, etc.]

---

## Sources
- LinkedIn: [URL]
- Apollo: [URL if available]
- Company site: [URL if useful]
---

Only include [SENIORITY_FILTER] level and above. Skip everyone below.
Work through each person one at a time. If a page doesn't load, retry once, then skip and note the failure.
```

---

## Failure Handling

| Scenario | What to do |
|---|---|
| Apollo has no data | Note "No Apollo data found" in file, continue |
| LinkedIn profile is private | Note name + title only, skip detail scrape |
| Page won't load after retry | Skip, create a stub file with the failure noted |
| Seniority unclear from title | Default to including them, flag in file |

---

## Adapting This Skill

- **Sales prospecting**: Add a "Pitch Angle" section to the template
- **Investor research**: Swap Apollo for Crunchbase or PitchBook
- **Academic/nonprofit**: Apollo is less useful — lean on LinkedIn + org website
- **Wider seniority net**: Change `SENIORITY_FILTER` to include Directors or Managers
- **CRM export**: After files are created, run a second pass to extract emails into a `.csv`
