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

**Plus the dynamic gurus selected in Step 2.**

### Step 4.5: Humanize

Run the `humanizer` skill on the article to remove signs of AI-generated writing.
This catches patterns the guru team might miss: inflated symbolism, promotional
language, em dash overuse, rule of three, AI vocabulary words, negative
parallelisms, and excessive conjunctive phrases.

After humanizing, re-read the article to confirm it still sounds like Cinder's
voice and hasn't lost any substance.

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
