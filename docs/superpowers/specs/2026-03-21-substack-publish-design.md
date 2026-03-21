# Substack Publishing Skill — Design Spec

**Date:** 2026-03-21
**Author:** Cinder Zhang + Claude
**Status:** Approved

## Problem

No existing tool publishes full articles to Substack from Claude Code. The two Substack MCPs (Article MCP, Notes MCP) are read-only or notes-only. Writing articles locally and manually copy-pasting into Substack's web editor is slow and error-prone.

## Solution

A `/publish-substack` skill that pushes markdown articles to Substack as drafts, using the `python-substack` package (ma2za). User previews and publishes manually from Substack's UI.

## Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Package | `python-substack` (ma2za) | Actively maintained, email/password auth, full draft workflow |
| Auth | Email + password (not cookies) | No manual cookie refresh every few weeks |
| Publish mode | Draft only | Safe — user previews in Substack UI before going live |
| Email notification | Default off | User controls notification from Substack UI |
| Audience | Free (everyone) | All posts are free for now |

## Architecture

```
User writes markdown OR asks Claude to draft
        |
/publish-substack skill (commands/publish-substack.md)
        |
Claude prepares markdown with frontmatter (title, subtitle)
        |
scripts/substack-publish.py (python-substack)
        |
Draft created on Substack -> constructs URL from publication + draft ID
        |
User previews in Substack UI -> publishes manually
```

## Files

| File | Purpose |
|------|---------|
| `commands/publish-substack.md` | Skill definition — orchestrates the flow |
| `scripts/substack-publish.py` | Python script (~20 lines) — creates draft via python-substack |
| `drafts/` | Local drafts folder (gitignored) |
| `~/.claude/substack-auth.env` | Email + password storage (private, never committed) |

## Skill Flow

### `/publish-substack` (no arguments)

1. Claude asks: "What do you want to write about?"
2. Claude drafts the article in markdown
3. Claude saves to `drafts/<slug>.md` with frontmatter
4. Script pushes draft to Substack
5. Script constructs and returns draft URL for preview

### `/publish-substack <filepath>`

1. Reads the specified markdown file
2. Parses frontmatter (title, subtitle) and body
3. Script pushes draft to Substack
4. Script constructs and returns draft URL for preview

## Draft Markdown Format

```markdown
---
title: Your Article Title
subtitle: Optional subtitle
---

Article body in markdown here...
```

## Script: `substack-publish.py`

Responsibilities:
- Read auth credentials from `~/.claude/substack-auth.env`
- Parse markdown file (frontmatter + body)
- Convert markdown body to HTML
- Retrieve `user_id` via `api.get_user().get("id")` after auth
- Call `python-substack` API: create draft with title, subtitle, body, user_id
- Set audience to "everyone" (free)
- Construct draft URL: `https://cinderzhang.substack.com/publish/post/<draft_id>`

Error handling:
- Missing auth file: print setup instructions and exit 1
- Auth failure: print "credentials invalid, check ~/.claude/substack-auth.env" and exit 1
- Network error: print error message and exit 1

## Auth Setup

First-time setup (prompted by skill):

Prerequisites:
- Substack account must have a password set. Passwordless (magic-link) accounts must set one at substack.com before using this skill.

1. Create `~/.claude/substack-auth.env`:
   ```
   SUBSTACK_EMAIL=your_email
   SUBSTACK_PASSWORD=your_password
   ```
2. Lock down permissions: `chmod 600 ~/.claude/substack-auth.env`
3. File lives outside repo — never committed

## Dependencies

- Python 3.9+
- `python-substack` (`pip install python-substack`) — pulls in `requests`, `python-dotenv`, `PyYAML`
- `python-frontmatter` (`pip install python-frontmatter`) — for parsing markdown frontmatter

## Out of Scope

- Publishing (live) from CLI — always draft-only
- Paid/subscriber-only posts
- Image uploads (future enhancement)
- Scheduling posts
- Email notification control from CLI

## Success Criteria

- `/publish-substack drafts/test.md` creates a draft on cinderzhang.substack.com
- Draft URL is returned and accessible in browser
- No manual cookie management required
- Works with both pre-written files and Claude-drafted content
