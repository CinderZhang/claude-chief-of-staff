# Multi-Agent Substack Content Pipeline — Design Spec

**Date:** 2026-03-21
**Author:** Cinder Zhang + Claude
**Status:** Approved

## Problem

Single-pass AI writing produces mediocre content. The first attempt at publishing to Substack pushed an article without proper research, review, or verification. Content creation needs a multi-agent team that mirrors how Cinder works with real guru reviewers: research deeply, write professionally, critique rigorously, and verify before presenting.

## Solution

A `/write-substack` skill that orchestrates a full content pipeline: parallel research, professional writing, iterative guru review, DRIVER evolution capture, and verified Substack publishing. Chief of Staff orchestrates and verifies every step before presenting to the user.

## Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Research tool | Tavily direct API (not MCP) | Simpler, no OAuth expiry, less token overhead |
| Team structure | 2 fixed gurus + 1-2 dynamic per topic | Mirrors edu-video pattern; consistent quality + topic expertise |
| Review rounds | Iterate until clean pass | Matches edu-video; quality over speed |
| DRIVER inclusion | Strategic — Chief of Staff decides per topic | Don't force DRIVER into unrelated content |
| Writing tone | Academic-authoritative + provocative framing | Cinder's voice: credible professor with strong opinions |
| User involvement | Hands-off until final review | Maximum leverage; user approves once at the end |
| Publish mode | Draft only, user publishes from Substack UI | Safe — preview before going live |
| Auth | Cookie-based (`SUBSTACK_COOKIE`), not email/password | Substack blocks programmatic login with CAPTCHA |
| Drafts path | `/home/cinder/claude-chief-of-staff/drafts/` | Pinned to repo, gitignored |

## Architecture

```
/write-substack "topic"
        |
   Chief of Staff
        |
        |-- 1. DRIVER Check: "Does this topic benefit from DRIVER?"
        |
        |-- 2. Dispatch parallel research
        |       |-- Research Subagent (Tavily API, 3-5 searches)
        |       |-- DRIVER Context Subagent (if applicable, reads DRIVER docs)
        |
        |-- 3. Chief of Staff reviews research briefs
        |
        |-- 4. Select dynamic gurus based on topic
        |
        |-- 5. Dispatch Writer Subagent
        |       Input: research brief + DRIVER context + tone guide
        |       Output: full article markdown with frontmatter
        |
        |-- 6. Guru Review Loop (iterate until clean)
        |       |-- Fixed: DRIVER Purist + Hostile Reader
        |       |-- Dynamic: 1-2 topic-specific experts
        |       |-- Writer revises -> gurus re-check -> repeat until clean
        |
        |-- 7. DRIVER Evolution Check
        |       "Did this research surface anything that evolves DRIVER?"
        |       YES -> save to Obsidian DRIVER-Evolution/, tag for /gm
        |
        |-- 8. Chief of Staff final verification
        |       - Read the full article (not just metadata)
        |       - Verify tone, accuracy, DRIVER alignment (if applicable)
        |
        |-- 9. Present to user
        |       - Full article text
        |       - Guru feedback summary
        |       - DRIVER evolution notes (if any)
        |       - "Approve to push to Substack?"
        |
        |-- 10. User approves -> push draft + verify content blocks -> return URL
```

## Team Composition

### Fixed Gurus (every article)

| Guru | Role | Key Checks |
|------|------|------------|
| **DRIVER Purist** | Ensures DRIVER methodology is applied correctly when used | Is the framework applied accurately? Would this confuse a DRIVER learner? Is DRIVER forced in where it doesn't belong? |
| **Hostile Reader** | Finds weak arguments, vague claims, logical gaps | Can every claim be defended? Are there weasel words? Would a skeptic be convinced? Any unsupported assertions? |

### Dynamic Experts (Chief of Staff selects 1-2 per article)

| Expert | When Selected | Key Checks |
|--------|--------------|------------|
| **Finance Expert** | Finance/AI intersection topics | Are financial concepts accurate? Would a finance professional respect this? |
| **Tech Practitioner** | Hands-on AI/coding topics | Are technical claims accurate? Would a developer find this credible? |
| **Academic Reviewer** | Research-heavy pieces | Are citations appropriate? Is the argument rigorous? |
| **Content Strategist** | Growth-focused pieces | Is the hook strong? Would this get shared? Is the CTA clear? |

### Research Subagent

- Uses Tavily API (direct curl, not MCP)
- Env var: `TAVILY_API_KEY` in `~/.claude/substack-auth.env`
- Endpoint: `POST https://api.tavily.com/search`
- Example: `curl -s -X POST "https://api.tavily.com/search" -H "Content-Type: application/json" -d '{"api_key": "$TAVILY_API_KEY", "query": "...", "max_results": 5}'`
- Runs 3-5 searches related to the topic
- Gathers: competing perspectives, recent data, quotable sources, related articles
- Outputs structured research brief:

```markdown
# Research Brief: <topic>

## Key Findings
- <finding 1 with source URL>
- <finding 2 with source URL>

## Competing Perspectives
- <perspective 1>
- <perspective 2>

## Quotable Data Points
- <stat or quote with attribution>

## Related Articles
- <title> — <URL> — <1-line summary>
```

### Writer Subagent

- Tone: Academic-authoritative with provocative framing
- Short paragraphs, strong opinions, structured arguments
- Takes: research brief + DRIVER context (if applicable) + tone guide
- Produces: full article with frontmatter (title, subtitle)

## DRIVER Integration Strategy

### Inclusion Rules

| Topic Type | DRIVER Role |
|------------|-------------|
| Systematic AI methodology | Core framework — apply and evolve |
| Finance + AI intersection | Supporting lens — use where it adds clarity |
| General tech/culture | Only if organically relevant |
| Unrelated domains | Don't mention |

Chief of Staff decides before research begins: "Does this topic benefit from DRIVER framing?"

### DRIVER Evolution Pipeline

Every article is a testing ground for DRIVER. After the guru review:

1. Chief of Staff asks: "Did this research surface anything that could evolve DRIVER?"
2. If YES: save evolution note to Obsidian `DRIVER-Evolution/YYYY-MM-DD-<topic>.md`
3. Morning brief (`/gm`) surfaces pending evolution notes for Cinder's review

### Evolution Note Format

```markdown
# DRIVER Evolution Note — YYYY-MM-DD

## Source
Article: "<article title>"

## Insight
<What was discovered that could strengthen or extend DRIVER>

## Suggested Evolution
<Specific change to DRIVER methodology>

## Status: pending-review
```

## Files

| File | Purpose |
|------|---------|
| `commands/write-substack.md` | Skill definition — full pipeline orchestration |
| `scripts/substack-publish.py` | Publish script (POST + PUT + verify, already built) |
| `scripts/tavily-search.sh` | Research script — Tavily API wrapper |
| `references/writer-voice.md` | Tone guide and writing style for writer subagent **(to be created)** |
| `references/guru-personas.md` | Fixed + dynamic guru definitions with checklists **(to be created)** |
| `drafts/` | Local drafts (gitignored) |
| Obsidian: `DRIVER-Evolution/` | Evolution notes tagged for morning brief |

## Morning Brief Integration

**Required modification:** Add a new step to `commands/gm.md` that checks Obsidian `DRIVER-Evolution/` for files with `Status: pending-review` and surfaces them:

```
DRIVER EVOLUTION
Yesterday's research on "AI Employees" surfaced:
- Validate stage may need "cascading validation" for multi-agent systems
- Action: Review note at DRIVER-Evolution/2026-03-21-ai-employees.md
```

## Guru Review Process

Modeled on edu-video's iterative review:

1. All gurus (fixed + dynamic) review the article simultaneously
2. Each guru outputs either `PASS` or `ISSUES:` followed by specific critiques with locations
3. If any guru outputs `ISSUES`: writer subagent revises based on all critiques
4. Gurus re-review the revised version
5. Loop exits when ALL gurus output `PASS`
6. **Max 3 rounds** — if not resolved after 3 iterations, Chief of Staff presents the article to user with unresolved guru feedback for human judgment
7. **Contradicting gurus** — if two gurus give conflicting feedback, Chief of Staff flags the conflict and presents both perspectives to the user
8. Chief of Staff reads the final article before presenting to user

## Error Handling

- Substack push fails: retry once, then save draft locally and alert user
- Cookie expired: print refresh instructions, don't silently fail
- Writer produces thin content: guru team catches it, forces revision
- After push: verify content blocks > 0 before reporting success

## Dependencies

- Python 3.9+
- `python-substack` (already installed in `~/.claude/substack-venv/`)
- `python-frontmatter` (already installed)
- Tavily API key (saved in `~/.claude/substack-auth.env`)
- Obsidian vault at `/mnt/d/OneDrive - purdue.edu/Obsidian/`
- DRIVER docs at `/mnt/d/github/DRIVER-PhilosophyBigPicture/`

## Success Criteria

- `/write-substack "topic"` produces a thoroughly researched, guru-reviewed article
- User sees the full article + guru feedback + DRIVER notes before approving
- Draft pushes to Substack with verified content
- DRIVER evolution notes surface in next morning's `/gm`
- No article goes to Substack without Chief of Staff verification
