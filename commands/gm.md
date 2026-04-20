# /gm — Morning Briefing

## Description
Start your day with a structured briefing: today's calendar, priority tasks,
urgent messages, and upcoming deadlines. Know exactly what matters before
you open your inbox.

## Instructions

You are running the morning briefing for {{YOUR_NAME}}. Follow these steps
in order, collecting information before presenting the final briefing.

### Step 0: Get Current Time

Call the Google Calendar `get-current-time` tool to get the authoritative
date and time. Extract the day of week, date, and timezone. Never guess
the day of week — always verify.

### Step 1: Calendar Review

Fetch today's calendar events using `list-events` with today's date range.

For each event, note:
- Time and duration
- Title and attendees
- Whether it requires preparation
- Any conflicts or back-to-back meetings

Flag:
- Meetings that conflict with hard constraints (e.g., dinner time)
- Back-to-back meetings with no buffer
- Meetings with no clear agenda or purpose

### Step 2: Task Review

Read `~/.claude/my-tasks.yaml` and identify:
- Tasks due TODAY (urgent)
- Tasks OVERDUE (critical — should have been done)
- Tasks due in the next 3 days (approaching)
- Tasks that can be completed today given the calendar

### Step 2.5: Job Opportunities Scan

Active job hunt context: see `C:\Users\cinde\.claude\projects\D--ChiefStaff\memory\project_job_hunt_2026.md`.
Profile fit: AI-finance intersection, tenure-track or senior faculty, leverages DRIVER
framework + World Scientific 3-book contract + top-journal pub record. Hard filters:
pay ≥ current Purdue comp; research-resource-positive (not admin-heavy at resource-poor
schools); brand ≥ Purdue Mitch Daniels School of Business.

1. Use LinkedIn MCP `search_jobs` with rotating queries: "applied AI finance professor",
   "financial AI research", "quantitative AI faculty", "AI finance tenure track"
2. Cross-check with any open applications in the job hunt memory to avoid duplicates
3. Score each new hit 1–5 on fit (5 = Booth-tier, 1 = MSU-tier)

Present only fit ≥ 3 under a JOB OPPORTUNITIES section:
- [role] @ [institution] — fit [N/5]: [one-line reasoning]
- If none qualify, skip the section entirely. Do not pad.

### Step 3: Goals Check

Read `~/.claude/goals.yaml` and briefly assess:
- Which goals have stalled (no progress update in 7+ days)?
- Does today's calendar align with the highest-priority goals?
- Any goal-aligned work that should be scheduled today?

### Step 4: Inbox Quick Scan (if email MCP is connected)

Do a quick scan of email for anything urgent:
- Search for emails from the last 12 hours
- Flag Tier 1 items (from key contacts, marked urgent, or time-sensitive)
- Don't do a full triage — just surface what's critical

### Step 4.5: DRIVER Evolution Check

Check the Obsidian vault for pending DRIVER evolution notes:

```bash
ls "/mnt/d/OneDrive - purdue.edu/Obsidian/DRIVER-Evolution/" 2>/dev/null
```

For each file found, read it and check if it contains `Status: pending-review`.
If any pending notes exist, include in the briefing under a DRIVER EVOLUTION section:

```
DRIVER EVOLUTION
- [date]: [insight summary] — Review at DRIVER-Evolution/[filename]
- Action: Review and decide whether to incorporate into DRIVER
```

If no pending notes or directory doesn't exist, skip this section entirely.

### Step 4.7: Entropy Research Development

Cinder's active research pivot (as of April 2026): information-theoretic foundations
for AI-augmented finance. Source material is in `D:/github/MSF_AI_Finance/Cases/` — six
entropy-based regime-shift case studies (textual, sample-space, regulatory, structural,
transfer, systemic/belief entropy). See memory: `reference_msf_cases.md`.

Each morning, nudge one concrete step forward. Rotate focus across:
- Case operationalization (one case → formal test specification)
- Paper draft sections (one section → 500 words of drafting)
- Methodology notes (one Shannon concept → one paragraph of theoretical framing)
- Literature (one paper → one-paragraph note on how it connects)

Gradually develop topics with Cinder. Do not dump a menu. Pick ONE next step based on
what's been touched least recently (check file mtimes in the Cases directory).

Present under ENTROPY RESEARCH section:
- Today's nudge: [ONE specific, 30–60 min action]
- Why this one: [one line — which case/paper, why it's due]

If Cinder already has a live entropy-research thread from prior days, continue that
thread rather than starting fresh.

### Step 4.8: Investment Position Watch

Read `C:\Users\cinde\.claude\investment-positions.yaml`. If the file doesn't exist,
skip this section and flag it: "Investment positions file not set up — ask Cinder to
seed positions."

For each active thesis:
1. Scan Gmail for overnight news matching the thesis keywords (e.g., "Hormuz", "Iran",
   "oil", "VIX", "defense stocks")
2. Check for material signals: price moves, policy actions, geopolitical escalation
3. Flag if thesis is invalidated, confirmed, or in need of trim/add

Present under INVESTMENT WATCH section:
- [thesis name]: [signal summary] — [action: monitor / trim / add / exit]
- If all theses are quiet: "Investment watch: all quiet."

Do NOT give trade advice unprompted. Surface signals; Cinder decides.

### Step 5: Present the Briefing

Format the briefing as follows:

```
Good morning. It's [Day], [Date]. Here's your day:

CALENDAR ([count] meetings)
- [time]  [title] ([duration]) [any flags]
- ...

[If applicable: "Heads up: [conflict or concern]"]

TASKS
- DUE TODAY: [list or "Nothing due today"]
- OVERDUE: [list or "All clear"]
- APPROACHING: [list of next 3 days]

GOALS
- [Brief status on top 1-2 goals, especially if stalled]

URGENT
- [Any Tier 1 items from inbox, or "No urgent items"]

JOB OPPORTUNITIES
- [Fit ≥3 hits, or skip section entirely]

DRIVER EVOLUTION
- [Any pending evolution notes, or skip if none]

ENTROPY RESEARCH
- Today's nudge: [ONE action]
- Why this one: [one line]

INVESTMENT WATCH
- [Thesis signals, or "all quiet"]

FOCUS RECOMMENDATION
Based on your calendar and priorities, here's what I'd focus on today:
1. [Top priority]
2. [Second priority]
3. [Third priority, if time allows]
```

### Guidelines

- Be concise. The whole briefing should fit on one screen.
- Lead with the most important information.
- If there are no urgent items, say so — that's good news.
- The focus recommendation should reflect goal alignment.
- If today's calendar is misaligned with goals, say so explicitly.
- End with an offer: "Want me to run a full triage or prep for any of these meetings?"
