# Substack Content Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a `/write-substack` command that orchestrates a multi-agent content pipeline — research, write, guru review, DRIVER evolution capture, and verified Substack publishing.

**Architecture:** A skill file (`commands/write-substack.md`) orchestrates the pipeline by dispatching subagents for research (Tavily API), writing, and guru review. Reference files define the writer's voice and guru personas. A Tavily search script provides web research. The existing `substack-publish.py` handles final publishing.

**Tech Stack:** Bash (Tavily search script), Python (Substack publish — already built), Claude Code skills/subagents (orchestration, writing, review), Obsidian (DRIVER evolution notes)

**Spec:** `docs/superpowers/specs/2026-03-21-content-pipeline-design.md`

---

## File Map

| File | Action | Responsibility |
|------|--------|---------------|
| `references/guru-personas.md` | Create | Fixed + dynamic guru definitions with checklists |
| `references/writer-voice.md` | Create | Tone guide for writer subagent |
| `scripts/tavily-search.sh` | Create | Tavily API wrapper — takes query, returns JSON results |
| `commands/write-substack.md` | Create | Skill definition — full pipeline orchestration |
| `commands/gm.md` | Modify | Add DRIVER Evolution check step |
| `scripts/substack-publish.py` | Exists | No changes needed |
| `.gitignore` | Modify | Add `drafts/` |

---

### Task 1: Create Guru Personas Reference

**Files:**
- Create: `references/guru-personas.md`

- [ ] **Step 1: Create the references directory**

```bash
mkdir -p /home/cinder/claude-chief-of-staff/references
```

- [ ] **Step 2: Write guru-personas.md**

Write the file with this content:

```markdown
# Guru Personas — Content Review Team

These personas review every Substack article before it reaches the user. Each guru outputs either `PASS` or `ISSUES:` followed by specific critiques with locations.

Max 3 review rounds. If unresolved, escalate to user with conflicting feedback.

---

## Fixed Gurus (every article)

### DRIVER Purist

**Role:** Guardian of DRIVER methodology integrity.

**When DRIVER is used in the article:**
- Is each DRIVER stage (D-R-I-V-E-R) applied accurately to its definition?
- Would this confuse someone learning DRIVER for the first time?
- Are the stage boundaries clear, or are stages conflated?
- Does the application add genuine insight, or is it superficial mapping?

**When DRIVER is NOT used:**
- Correct decision? Would DRIVER framing have added value here?
- If the topic is systematic AI methodology, flag the omission.

**Output format:**
PASS — DRIVER usage is accurate and adds value (or correctly omitted)
ISSUES:
- [location]: [specific problem and suggested fix]

---

### Hostile Reader

**Role:** Adversarial critic. Assumes the reader is skeptical, busy, and looking for reasons to stop reading.

**Checks:**
- Can every claim be defended with evidence or clear reasoning?
- Are there weasel words? ("some experts say", "it's widely known", "arguably")
- Would a domain expert find any claim embarrassing or wrong?
- Is the opening hook strong enough to survive 3 seconds of attention?
- Does every paragraph earn its place, or is there filler?
- Are there logical gaps or non-sequiturs between sections?
- Is the conclusion actionable or just vague inspiration?

**Red flags:**
- Unsupported assertions presented as fact
- Paragraphs that restate the previous paragraph differently
- "In conclusion" followed by nothing new
- Name-dropping without substance

**Output format:**
PASS — Article withstands hostile scrutiny
ISSUES:
- [location]: [specific weakness and why it fails]

---

## Dynamic Gurus (Chief of Staff selects 1-2 per article)

### Finance Expert

**Select when:** Article touches finance, markets, valuation, investment, fintech, or financial AI applications.

**Checks:**
- Are financial concepts used correctly? (e.g., DCF, NPV, risk-adjusted returns)
- Would a CFA or finance professor find this credible?
- Are market claims supported by data or at least qualified?
- Is financial jargon explained for non-finance readers?

**Output format:**
PASS — Financial content is accurate and credible
ISSUES:
- [location]: [specific problem and suggested fix]

---

### Tech Practitioner

**Select when:** Article involves coding, AI implementation, software architecture, or developer tools.

**Checks:**
- Are technical claims accurate and current?
- Would a senior developer find this credible?
- Are code examples (if any) correct and idiomatic?
- Is the technical depth appropriate — not too shallow, not unnecessarily deep?

**Output format:**
PASS — Technical content is accurate and credible
ISSUES:
- [location]: [specific problem and suggested fix]

---

### Academic Reviewer

**Select when:** Article makes research claims, cites studies, or presents theoretical frameworks.

**Checks:**
- Are citations real and accurately represented?
- Is the argument logically rigorous?
- Are counterarguments acknowledged?
- Would this pass peer review for logical structure (not necessarily novelty)?

**Output format:**
PASS — Academic rigor is sufficient
ISSUES:
- [location]: [specific problem and suggested fix]

---

### Content Strategist

**Select when:** Article is meant to grow audience, go viral, or drive specific action.

**Checks:**
- Is the headline compelling and specific?
- Does the opening hook create urgency or curiosity?
- Is there a clear value proposition for the reader?
- Would someone share this? What's the "tweetable moment"?
- Is the CTA clear and natural?

**Output format:**
PASS — Content is compelling and shareable
ISSUES:
- [location]: [specific problem and suggested fix]
```

- [ ] **Step 3: Commit**

```bash
git add references/guru-personas.md
git commit -m "Add guru personas reference for content pipeline review team"
```

---

### Task 2: Create Writer Voice Reference

**Files:**
- Create: `references/writer-voice.md`

- [ ] **Step 1: Write writer-voice.md**

```markdown
# Writer Voice — Substack Article Style Guide

This guide defines Cinder Zhang's writing voice for Substack articles. The Writer Subagent must follow these constraints exactly.

## Tone: Academic-Authoritative + Provocative Framing

You are a professor who writes like a thought leader. Credible and structured, but with strong hooks and clear opinions. Not dry. Not clickbait. The sweet spot between a journal article and a viral thread.

## Voice Characteristics

**Authority:** Write from expertise, not speculation. State positions directly. "This is wrong" not "This might be problematic."

**Provocation:** Open with a claim that makes the reader stop scrolling. Challenge conventional wisdom. Name the problem most people are ignoring.

**Structure:** Every article has a clear thesis, supporting arguments, and a conclusion that drives action. The reader should be able to summarize your argument in one sentence.

**Accessibility:** Explain complex ideas simply. Use analogies. A finance professor and a software engineer should both follow the argument.

## Formatting Rules

- Short paragraphs (2-4 sentences max)
- Use contractions naturally (I'm, we're, it's, don't)
- Bold key phrases for skimmability
- Use headers to create clear sections
- Bullet points for lists, not run-on sentences
- One idea per paragraph

## What TO Do

- Start with a specific, concrete example or provocative claim
- Use real names, real companies, real numbers when possible
- Make every paragraph earn its place
- End with a clear call to action or memorable framing
- Credit sources and people explicitly

## What NOT To Do

- Don't hedge ("it could be argued", "some might say")
- Don't use corporate jargon ("leverage synergies", "paradigm shift")
- Don't write generic introductions ("In today's rapidly changing world...")
- Don't repeat the same point in different words
- Don't end with vague inspiration ("The future is bright")

## DRIVER Integration

When DRIVER is used, weave it naturally into the argument. Don't introduce DRIVER with a formal definition unless the article is specifically about DRIVER. Instead, show DRIVER in action through the article's own structure and examples.

## Article Structure Template

1. **Hook** (1-2 paragraphs) — Provocative opening. Specific example, surprising stat, or bold claim.
2. **Problem** (2-3 paragraphs) — What's broken. Why it matters. What most people miss.
3. **Thesis** (1 paragraph) — Your core argument in clear terms.
4. **Evidence** (3-5 sections) — Supporting arguments with examples, data, analogies.
5. **Implications** (1-2 paragraphs) — What this means for the reader.
6. **Close** (1 paragraph) — Memorable framing or call to action. Not a summary.

## Signature

End every article with:
```
*Cinder Zhang is a Professor and Co-Founder at Driver AI.*
```
Add contextual credit lines for sources/inspiration as appropriate.
```

- [ ] **Step 2: Commit**

```bash
git add references/writer-voice.md
git commit -m "Add writer voice reference for Substack content pipeline"
```

---

### Task 3: Create Tavily Search Script

**Files:**
- Create: `scripts/tavily-search.sh`

- [ ] **Step 1: Write tavily-search.sh**

```bash
#!/usr/bin/env bash
# Tavily web search wrapper
# Usage: tavily-search.sh "search query" [max_results]
# Reads TAVILY_API_KEY from ~/.claude/substack-auth.env

set -euo pipefail

QUERY="${1:?Usage: tavily-search.sh \"search query\" [max_results]}"
MAX_RESULTS="${2:-5}"
AUTH_FILE="$HOME/.claude/substack-auth.env"

if [ ! -f "$AUTH_FILE" ]; then
    echo "Error: $AUTH_FILE not found" >&2
    exit 1
fi

source "$AUTH_FILE"

if [ -z "${TAVILY_API_KEY:-}" ]; then
    echo "Error: TAVILY_API_KEY not set in $AUTH_FILE" >&2
    exit 1
fi

curl -s -X POST "https://api.tavily.com/search" \
    -H "Content-Type: application/json" \
    -d "{\"api_key\": \"$TAVILY_API_KEY\", \"query\": \"$QUERY\", \"max_results\": $MAX_RESULTS, \"search_depth\": \"advanced\"}"
```

- [ ] **Step 2: Make executable**

```bash
chmod +x scripts/tavily-search.sh
```

- [ ] **Step 3: Test the script**

```bash
./scripts/tavily-search.sh "AI employee automation 2026" 2
```

Expected: JSON response with search results.

- [ ] **Step 4: Commit**

```bash
git add scripts/tavily-search.sh
git commit -m "Add Tavily search script for content research pipeline"
```

---

### Task 4: Add drafts/ to .gitignore

**Files:**
- Modify: `.gitignore` (create if not exists)

- [ ] **Step 1: Add drafts/ to .gitignore**

```bash
echo "drafts/" >> .gitignore
```

If `.gitignore` doesn't exist, create it with:

```
drafts/
*.env
```

- [ ] **Step 2: Commit**

```bash
git add .gitignore
git commit -m "Add drafts/ to gitignore"
```

---

### Task 5: Create the /write-substack Skill

**Files:**
- Create: `commands/write-substack.md`

This is the core orchestration file. It tells Claude how to run the entire pipeline.

- [ ] **Step 1: Write commands/write-substack.md**

```markdown
# /write-substack — Publish a Researched Article to Substack

## Description
Full content pipeline: research, write, guru review, DRIVER evolution capture,
and verified Substack draft publishing. Hands-off until final review.

## Arguments
- `<topic>` — What to write about (required)
- `from <filepath>` — Use an existing draft instead of writing from scratch

## Instructions

You are the Chief of Staff orchestrating a content pipeline for Cinder Zhang.
Your job is to coordinate research, writing, and review — and verify every
step before presenting to the boss. Never declare success without checking.

### Step 0: Understand the Topic

Parse the user's topic. Determine:
1. **DRIVER relevance** — Does this topic benefit from DRIVER framing?
   - Systematic AI methodology → YES, core framework
   - Finance + AI intersection → YES, supporting lens
   - General tech/culture → Only if organically relevant
   - Unrelated domains (poetry, personal) → NO
### Step 1: Research (Parallel)

Dispatch research subagents in parallel:

**Research Subagent:**
Use the Bash tool to run Tavily searches. Run 3-5 searches with different
angles on the topic:
- The topic itself
- Competing/contrasting perspectives
- Recent news or data related to the topic
- Key people or companies involved

For each search, run:
```
/home/cinder/claude-chief-of-staff/scripts/tavily-search.sh "query" 5
```

Compile results into a research brief using this format:

```
# Research Brief: <topic>

## Key Findings
- <finding with source URL>

## Competing Perspectives
- <perspective>

## Quotable Data Points
- <stat or quote with attribution>

## Related Articles
- <title> — <URL> — <1-line summary>
```

**DRIVER Context Subagent (if DRIVER relevant):**
Read relevant files from `/mnt/d/github/DRIVER-PhilosophyBigPicture/`:
- `DRIVER_Universal_Overview.md` for framework overview
- `DRIVER_MVP_Sharpened.md` for implementation details
- Any topic-specific DRIVER docs

Summarize the DRIVER principles most relevant to this article's topic.

### Step 2: Review Research and Select Gurus

Before dispatching the writer, review the research briefs:
- Is there enough material for a substantive article?
- Are there clear angles and arguments?
- Are sources credible?

If research is thin on a specific angle, run additional Tavily searches.

**Now select dynamic gurus** based on what the research revealed:
- Finance-heavy content → Finance Expert
- Coding/AI implementation → Tech Practitioner
- Research claims or citations → Academic Reviewer
- Growth/viral intent → Content Strategist

### Step 3: Write the Article

Read `references/writer-voice.md` for the tone guide.

Write the full article following the voice guide exactly:
- Hook → Problem → Thesis → Evidence → Implications → Close
- Academic-authoritative with provocative framing
- Short paragraphs, bold key phrases, clear structure
- Include the research findings naturally (with attribution)
- If DRIVER relevant: weave DRIVER principles into the argument naturally
- End with Cinder's signature and credit lines

Save to `/home/cinder/claude-chief-of-staff/drafts/<slug>.md` with frontmatter:

```yaml
---
title: Article Title Here
subtitle: Optional subtitle
---
```

### Step 4: Guru Review Loop

Read `references/guru-personas.md` for all persona definitions.

**Round structure:**
1. Review the article through ALL selected guru lenses simultaneously
2. For each guru, output either `PASS` or `ISSUES:` with specific locations
3. If any guru has issues: revise the article addressing all critiques
4. Re-review with all gurus
5. Exit when ALL gurus output `PASS`
6. **Max 3 rounds** — if not clean after 3, present to user with unresolved feedback
7. **Contradictions** — if gurus conflict, flag both perspectives for user

**Always apply these gurus:**
- DRIVER Purist
- Hostile Reader

**Plus the dynamic gurus selected in Step 0.**

### Step 5: DRIVER Evolution Check

Ask: "Did this research or writing process surface anything that could
evolve or strengthen the DRIVER framework?"

If YES:
1. Create a DRIVER evolution note at:
   `/mnt/d/OneDrive - purdue.edu/Obsidian/DRIVER-Evolution/YYYY-MM-DD-<topic-slug>.md`

   Format:
   ```markdown
   # DRIVER Evolution Note — YYYY-MM-DD

   ## Source
   Article: "<article title>"

   ## Insight
   <What was discovered>

   ## Suggested Evolution
   <Specific change to DRIVER methodology>

   ## Status: pending-review
   ```

2. Note this for the final presentation.

If NO: skip. Don't force it.

### Step 6: Chief of Staff Final Verification

Before presenting to the user, YOU (Chief of Staff) must:
1. **Read the full article** — not just the title or first paragraph
2. **Verify it has substance** — multiple sections, real arguments, evidence
3. **Check tone** — matches writer-voice.md guidelines
4. **Confirm DRIVER accuracy** — if used, stages are applied correctly
5. **Verify the draft file exists** and has content

Do NOT present to the user until you have personally verified all of the above.

### Step 7: Present to User

Present in this format:

```
ARTICLE READY FOR REVIEW

Title: <title>
Subtitle: <subtitle>
Word count: <count>
DRIVER integration: <Yes/No — and how>
Guru review: <X rounds, all passed / or note unresolved issues>

---

<Full article text>

---

GURU FEEDBACK SUMMARY
<Brief summary of key critiques addressed>

DRIVER EVOLUTION
<Any evolution notes, or "No new insights">

---

Approve to push to Substack as draft? [Y/N]
```

Wait for user approval. Do NOT push without explicit "Y" or "Send" or approval.

### Step 8: Publish

After user approves:
1. Run the publish script:
   ```
   /home/cinder/.claude/substack-venv/bin/python3 /home/cinder/claude-chief-of-staff/scripts/substack-publish.py /home/cinder/claude-chief-of-staff/drafts/<slug>.md
   ```
2. Verify the output shows content blocks > 0
3. Present the draft URL to the user

If publish fails:
1. Retry once
2. If cookie error: "Substack cookie expired. Grab a fresh `substack.sid`
   from browser DevTools and update `~/.claude/substack-auth.env`."
3. If other error: alert user with error details and say:
   "Draft is saved locally at `drafts/<slug>.md` — you can copy-paste
   into Substack's editor manually."
```

- [ ] **Step 2: Commit**

```bash
git add commands/write-substack.md
git commit -m "Add /write-substack skill — multi-agent content pipeline"
```

---

### Task 6: Modify /gm for DRIVER Evolution Check

**Files:**
- Modify: `commands/gm.md` (add new step between Step 4 and Step 5)

- [ ] **Step 0: Read current gm.md to confirm step structure**

```bash
cat /home/cinder/claude-chief-of-staff/commands/gm.md
```

Confirm Step 4 is "Inbox Quick Scan" and Step 5 is "Present the Briefing" before inserting.

- [ ] **Step 1: Add DRIVER Evolution step to gm.md**

Insert the following as a new `### Step 4.5: DRIVER Evolution Check` between the existing Step 4 (Inbox Quick Scan) and Step 5 (Present the Briefing):

```markdown
### Step 4.5: DRIVER Evolution Check

Check the Obsidian vault for pending DRIVER evolution notes:

```bash
ls "/mnt/d/OneDrive - purdue.edu/Obsidian/DRIVER-Evolution/" 2>/dev/null
```

For each file found, check if it contains `Status: pending-review`.
If any pending notes exist, include in the briefing under a DRIVER EVOLUTION section:

```
DRIVER EVOLUTION
- [date]: [insight summary] — Review at DRIVER-Evolution/[filename]
- Action: Review and decide whether to incorporate into DRIVER
```

If no pending notes, skip this section entirely.
```

- [ ] **Step 2: Also add the DRIVER EVOLUTION section to the briefing template in Step 5**

In the briefing format block in Step 5, add between URGENT and FOCUS RECOMMENDATION:

```
DRIVER EVOLUTION
- [Any pending evolution notes, or skip if none]
```

- [ ] **Step 3: Commit**

```bash
git add commands/gm.md
git commit -m "Add DRIVER evolution check to morning briefing"
```

---

### Task 7: Create DRIVER-Evolution Directory in Obsidian

**Files:**
- Create directory: `/mnt/d/OneDrive - purdue.edu/Obsidian/DRIVER-Evolution/`

- [ ] **Step 1: Create the directory**

```bash
mkdir -p "/mnt/d/OneDrive - purdue.edu/Obsidian/DRIVER-Evolution"
```

- [ ] **Step 2: Verify it exists**

```bash
ls -la "/mnt/d/OneDrive - purdue.edu/Obsidian/DRIVER-Evolution"
```

No commit needed — this is outside the repo.

---

### Task 8: End-to-End Test

- [ ] **Step 1: Run the full pipeline**

Invoke `/write-substack` with a test topic:
```
/write-substack "Why AI employees need systematic methodology — using DRIVER as the operating system"
```

- [ ] **Step 2: Verify each stage completed**

Check:
- [ ] Research brief was generated with real Tavily results
- [ ] Article has hook, problem, thesis, evidence, implications, close
- [ ] Guru review ran (at least 1 round, all PASS)
- [ ] DRIVER evolution check was performed
- [ ] Chief of Staff read the full article before presenting
- [ ] Article presented to user with full context
- [ ] Draft file exists at `drafts/<slug>.md` with content

- [ ] **Step 3: Test the publish flow**

After user approves, verify:
- [ ] `substack-publish.py` outputs content blocks > 0
- [ ] Draft URL is accessible
- [ ] Content is actually visible on Substack (open the URL and check)

- [ ] **Step 4: Verify DRIVER evolution note (if created)**

- [ ] File exists in Obsidian `DRIVER-Evolution/` directory
- [ ] Contains proper format with `Status: pending-review`
- [ ] Run `/gm` and verify the DRIVER EVOLUTION section appears with the pending note

---

## Task Summary

| Task | What | Files |
|------|------|-------|
| 1 | Guru personas reference | `references/guru-personas.md` |
| 2 | Writer voice reference | `references/writer-voice.md` |
| 3 | Tavily search script | `scripts/tavily-search.sh` |
| 4 | Gitignore drafts/ | `.gitignore` |
| 5 | /write-substack skill | `commands/write-substack.md` |
| 6 | /gm DRIVER evolution step | `commands/gm.md` |
| 7 | Obsidian DRIVER-Evolution dir | Obsidian vault |
| 8 | End-to-end test | Full pipeline verification |
