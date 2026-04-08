# AI Chief of Staff

An AI-powered productivity system built on [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that operates as a chief of staff — triaging inboxes, managing relationships, producing content, and keeping priorities honest.

Forked from [Mike Murchison's original](https://github.com/mimurchison/claude-chief-of-staff) and extended with a full content pipeline, DRIVER framework integration, and multi-agent workflows.

---

## What It Does

### Communicate
Triage email, Slack, and messaging. Draft responses in your voice, prioritized by relationship tier. Morning briefings surface what matters before you open your inbox.

### Produce Content
Full Substack pipeline: research, write, guru review (4 expert lenses), source verification, humanize, distribute. One command takes a topic from idea to publication-ready draft with distribution assets (LinkedIn, X thread, newsletter teaser, video hook).

### Deepen Relationships
Personal CRM that builds itself. Contact files track relationship context, history, and notes. Staleness alerts when important relationships go quiet. LinkedIn outreach via MCP.

### Achieve Goals
Quarterly objectives in `goals.yaml` filter every decision. Claude pushes back when time allocation drifts from stated priorities.

---

## Content Pipeline

The standout addition to the original CoS framework. A multi-agent pipeline for thought leadership:

```
Topic idea
  -> /write-substack
     -> Researcher agent (multi-source, competitive landscape)
     -> Writer agent (voice-matched, DRIVER-integrated)
     -> Guru reviewer (4 expert lenses, iterates until all pass)
     -> Humanizer (strips AI writing patterns)
     -> Source verification (fact-check all claims and URLs)
     -> Growth strategist (distribution plan, social assets)
     -> Publisher (push to Substack as draft)
```

Each stage produces artifacts in `drafts/` — research briefs, guru logs, verification reports, distribution assets. Everything is auditable.

### Published Articles
| # | Title | Focus |
|---|-------|-------|
| 1 | DRIVER Revisited | The one stage every AI framework gets wrong |
| 2 | The Human Gap | Why AI superpowers need human design |
| 3 | The Harness and the Horse | Education's AI debate is stuck on the wrong metaphor |
| 4 | The Company That Already Killed the Org Chart | Haier's 20-year proof vs. Dorsey's AI thesis |

---

## Commands

| Command | What It Does |
|---------|--------------|
| `/gm` | Morning briefing — calendar, tasks, urgent messages, signals |
| `/triage` | Inbox triage across all connected channels |
| `/my-tasks` | Task management with execution, not just tracking |
| `/enrich` | Auto-enrich contact profiles from all channels |
| `/write-substack` | Full content pipeline from topic to Substack draft |

---

## Project Structure

```
ChiefStaff/
├── CLAUDE.md              # AI operating system — personality, voice, rules
├── goals.yaml             # Quarterly objectives (source of truth)
├── my-tasks.yaml          # Active task list
├── schedules.yaml         # Automation schedules
├── commands/              # Slash commands (/gm, /triage, /enrich, etc.)
├── contacts/              # Relationship CRM files
├── config/                # Auth credentials (.env)
├── drafts/                # Article drafts, research, distribution assets
├── experts/               # DRIVER expert configurations
├── references/            # Writer voice guide, guru personas, hook templates
├── scripts/               # Publish scripts (Substack, LinkedIn MCP, Tavily)
├── videos/                # Video production assets
└── docs/                  # Setup guide, MCP servers, customization
```

---

## Setup

### Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed and authenticated
- Gmail MCP server
- Google Calendar MCP server

### Install

```bash
git clone <repo-url>
cd ChiefStaff
chmod +x install.sh
./install.sh
```

### MCP Servers

| Server | Required? | What It Enables |
|--------|-----------|-----------------|
| Gmail | Yes | Email triage, drafting |
| Google Calendar | Yes | Scheduling, availability |
| Slack | Recommended | Slack triage |
| LinkedIn | Optional | Profile lookup, outreach |
| Tavily | Optional | Research for content pipeline |

See [docs/mcp-servers.md](docs/mcp-servers.md) for installation instructions.

### Content Pipeline Setup

The Substack publisher requires a session cookie:

1. Log in to [substack.com](https://substack.com)
2. Open DevTools (F12) > Console
3. Run: `document.cookie.match(/substack\.sid=([^;]+)/)?.[1]`
4. Save to `config/.env` as `SUBSTACK_COOKIE=<value>`

---

## Customization

`CLAUDE.md` is the core. It defines who you are, how you write, what you care about, and how Claude should operate. The longer you use it, the better it gets.

Key files to personalize:
- **CLAUDE.md** — Voice, constraints, operating modes
- **goals.yaml** — Your actual priorities
- **contacts/** — Your relationship network
- **references/writer-voice.md** — Your writing style for content

See [docs/customization.md](docs/customization.md) for the full guide.

---

## Credits

Original framework by [Mike Murchison](https://linkedin.com/in/mikemurchison) ([@mimurchison](https://twitter.com/mimurchison)), CEO of [Ada](https://ada.cx). Extended by [Cinder Zhang](https://cinderzhang.substack.com), Professor at Purdue University and Co-Founder of Driver AI.

MIT License. See [LICENSE](LICENSE) for details.
