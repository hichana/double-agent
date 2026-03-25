# OpenClaw → Anthropic Playbook
**Replicating the OpenClaw Use Case Using Only Anthropic Tools**

> **Last updated:** March 25, 2026
> **Status:** Active reference — OpenClaw and Anthropic's tooling are both moving fast. Re-verify any specific feature before relying on it.

---

## What This Document Is

OpenClaw is the current gold standard for a personal, autonomous AI agent. This document maps every meaningful OpenClaw capability to its Anthropic equivalent, then walks through how to actually set it up — using Claude Code, Claude Desktop (Cowork + Dispatch), Computer Use, the mobile app, and the Claude API.

The goal: replicate the *experience* of OpenClaw — an always-on, messaging-accessible, integration-rich AI that takes real actions — using only Anthropic's stack.

---

## Part 1: What Makes OpenClaw Special

Understanding what we're replicating is the first step.

### 1.1 The Core Value Proposition

OpenClaw is not a chatbot. The distinction is critical: it **executes tasks**. Users don't get answers; they get outcomes. It was released in November 2025 and grew to 165k GitHub stars and 230k X followers within months — widely described as a "ChatGPT moment" for autonomous agents.

It grew from 9,000 stars on launch day to 250,000+ GitHub stars by early March 2026 — surpassing React as the most-starred GitHub project ever.

Its success rests on four pillars:

> **Note on GitHub stars:** Initial reports cited ~165k stars, but OpenClaw surpassed React's 10-year record in under 60 days. By March 3, 2026 it had 250,000+ stars — the most-starred project in GitHub history.

**1. Messaging-Native Access**
You reach OpenClaw through the apps you already live in: WhatsApp, Telegram, Discord, Slack, iMessage, Signal. The UX is zero-friction — no new app to open, no context switch. You text it like a person.

**2. Real Autonomy**
OpenClaw can browse the web, run shell commands, manage files, send emails, control your calendar, call APIs, and schedule its own future tasks. It's not summarizing; it's acting.

**3. Skills Ecosystem (ClawHub)**
A marketplace of SKILL.md files (currently ~3,286 after a security cleanup from ~5,700). Anyone can write a skill. Users install skills the way you install apps. This is what gives OpenClaw its "50+ integrations" advantage — it's really a skills-as-apps model.

**4. Local-First Privacy**
Runs on your machine. Data doesn't leave. Works with any LLM (Claude, GPT, local Ollama models). This is a major differentiator vs. cloud-only agents.

### 1.2 The Onboarding Experience

OpenClaw's onboarding is deliberately minimal:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard
```

An interactive TUI walks through: acknowledging the agent can take real actions → choosing a Quick Start path → selecting an LLM provider → connecting a messaging channel → optionally installing skills from ClawHub.

The entire flow takes 10–20 minutes for a technically comfortable user. The macOS menubar app makes ongoing management trivial.

### 1.3 The "Magic Moment"

Users consistently describe the same arc: setup takes effort, but within the first week it becomes "genuinely indispensable." The killer feature is almost always **email automation** — users report saving 3–5 hours/week just on inbox management. From there they expand to daily briefings, developer tasks, content creation, and lead generation.

### 1.4 What Users Are Actually Doing

| Workflow | Description |
|---|---|
| **Morning briefing** | Automated digest: weather, calendar, tasks, news, health stats |
| **Email triage** | Summarize inbox, draft replies, flag urgent items |
| **Developer shortcuts** | Run tests, deploy code, manage GitHub via chat |
| **Content pipeline** | Research → draft → format → schedule |
| **Lead generation** | Find companies, enrich contacts, draft outreach |
| **Receipt processing** | Photo → structured expense data in a spreadsheet |
| **Meeting notes** | Transcribe → summarize → assign tasks |
| **Smart reminders** | Scheduled follow-ups, deadline alerts |

---

## Part 2: The Anthropic Stack (March 2026)

Before mapping, here's the current state of Anthropic's tools:

### 2.1 Claude Code

A CLI-first agentic coding tool, but increasingly general-purpose. Runs on macOS, Linux, and Windows. Available in-terminal, in VS Code/JetBrains, in the Desktop app, and via browser.

**Key automation features:**
- **Cloud scheduled tasks**: Run on Anthropic infrastructure — your computer doesn't need to stay on
- **Desktop scheduled tasks**: Run locally, require computer to be on
- **Channels**: Trigger Claude Code from Telegram and Discord (messaging-native access)
- **Auto Memory**: Learns preferences and patterns across sessions without manual input
- **Skills**: SKILL.md files define repeatable workflows and best practices
- **Hooks**: Pre/post-action shell commands (auto-format after edits, etc.)
- **Sub-agents**: Spawn parallel Claude Code instances for coordinated work
- **MCP integration**: Connects to 10,000+ external services

### 2.2 Claude Desktop + Cowork

The Desktop app brings Claude into everyday non-coding work. Cowork mode (research preview) provides:

- Direct read/write access to local files (no upload required)
- Long-running multi-step task execution
- Document, spreadsheet, and slide deck creation
- **Computer Use** (Mac only, research preview): Click, navigate apps, fill forms, control your screen
- **Projects**: Persistent workspaces with scoped memory and scheduled tasks

### 2.3 Dispatch (Launched March 17, 2026)

Dispatch is Anthropic's direct answer to OpenClaw's messaging-native experience. You pair Claude Desktop with Claude mobile via QR code. Then you text Claude from your phone, and it works on your Mac while you're away.

**What this enables:**
- Send task from iPhone → Claude executes on desktop
- Monitor progress remotely
- Persistent cross-device conversations
- Computer Use runs in the background via Dispatch

**Current limitation:** Requires your Mac to stay on. Not cloud-based (yet). Available on Max tier now; Pro coming imminently.

### 2.4 Claude Mobile App

- Voice mode (5 voice options)
- Vision / image analysis
- Health data analytics (reads HealthKit/Google Fit) — Pro/Max
- "Remote Control" mode: command Claude Code on desktop from phone (March 2026)
- iOS: Reminders integration, Siri Shortcuts
- Android: Home screen widgets

### 2.5 MCP (Model Context Protocol)

Anthropic created MCP and donated it to the Agentic AI Foundation (December 2025). It is now the de facto standard for AI integrations — adopted by OpenAI, Google, Microsoft, Cursor, and VS Code.

**Scope:** 10,000+ public MCP servers. 75+ pre-built connectors in Claude's directory. Enterprise organizations report 40–60% faster agent deployment using MCP.

### 2.6 Current Models

| Model | Best For | Context |
|---|---|---|
| Claude Opus 4.6 | Complex agentic tasks, long reasoning | 1M input / 128k output |
| Claude Sonnet 4.6 | Speed + intelligence balance | 1M input / 64k output |
| Claude Haiku 4.5 | Fast, lightweight tasks | 200k input / 64k output |

---

## Part 3: Feature-by-Feature Mapping

| OpenClaw Feature | Anthropic Equivalent | Fidelity | Notes |
|---|---|---|---|
| Messaging-native access (Telegram, Discord) | Claude Code Channels (Telegram, Discord) | ✅ High | Native; works today |
| Messaging-native access (WhatsApp, iMessage, Signal) | Dispatch (mobile → desktop) | 🟡 Partial | Different UX; phone-to-desktop, not messaging app |
| 24/7 background execution | Claude Code cloud scheduled tasks | ✅ High | Truly cloud-based; no computer required |
| Local execution | Claude Code desktop tasks + Cowork | ✅ High | Requires computer to stay on |
| Email automation | MCP (Gmail/Outlook servers) + Claude Code | ✅ High | Requires MCP setup; very capable once done |
| Calendar management | MCP (Google Calendar server) + Claude Code | ✅ High | Same approach as email |
| File management | Cowork direct file access + Claude Code | ✅ High | Native in both tools |
| Web browsing | Computer Use (Mac) or Puppeteer MCP | 🟡 Partial | Computer Use is research preview; Puppeteer is more stable |
| Shell command execution | Claude Code | ✅ High | Full terminal access; this is its home turf |
| Scheduled / cron tasks | Cloud or desktop scheduled tasks | ✅ High | Both available; cloud preferred for reliability |
| Persistent memory | Auto Memory (Claude Code) + Projects (Cowork) | ✅ High | Auto Memory learns passively; Projects scope it |
| Skills marketplace (ClawHub) | Skills (SKILL.md) + Claude's plugin system | ✅ High | Identical concept; 100+ skills available |
| Form filling / computer control | Computer Use (Mac only, research preview) | 🟡 Partial | Early but functional; Mac only |
| 50+ integrations | MCP (10,000+ servers) | ✅ High | Far broader in scope; less curated |
| GitHub / dev tool access | Claude Code native + GitHub MCP | ✅ High | Strongest area; deep native integration |
| Daily briefing | Scheduled Claude Code task | ✅ High | Trivial to set up with the right MCPs |
| Receipt → spreadsheet | Cowork + vision + Excel skill | ✅ High | Vision reads receipt; Excel skill creates file |
| Local-first privacy | Claude Code / Cowork (local) | ✅ High | Fully local option available |
| Model agnostic | Claude only | ❌ No | Locked to Claude; can't use GPT or Ollama |
| Free / open source | Paid plans required | ❌ No | Pro $20/mo, Max $100/mo; no self-hosted option |
| Cross-platform messaging (15+ channels) | Telegram + Discord (2 channels) | 🔴 Gap | Biggest gap vs. OpenClaw |

---

## Part 4: The Setup Playbook

This section is the actual how-to. Follow it sequentially.

### Step 1: Get the Right Plan

You need at minimum **Claude Pro ($20/mo)** for Cowork and scheduled tasks. For Dispatch and higher usage limits, **Claude Max ($100/mo)** is required — and it's what enables the messaging-from-phone experience.

Decision guide:
- Occasional automation + Cowork → Pro ($20/mo)
- Dispatch + 24/7 automation + higher usage → Max 5x ($100/mo)
- Very heavy usage + Max features → Max 20x ($200/mo)
- Building for production / API access → Claude API subscription separately

### Step 2: Install Claude Desktop + Claude Code

**Claude Desktop** (includes Cowork mode):
- Download from [claude.ai/download](https://claude.ai/download)
- Sign in with your Pro/Max account
- Cowork mode is enabled automatically

**Claude Code** (CLI):
```bash
# macOS / Linux
curl -fsSL https://claude.ai/install-code.sh | bash

# Or via npm
npm install -g @anthropic-ai/claude-code
```

Verify installation:
```bash
claude --version
claude auth login
```

### Step 3: Install Claude Mobile + Set Up Dispatch

1. Install the Claude app on your iPhone/Android
2. Sign in with the same account
3. In Claude Desktop: Settings → Dispatch → Pair Mobile Device → scan QR code
4. Send a test message from your phone: "Run a quick test task on my desktop"
5. Watch it execute on your Mac

This is the equivalent of OpenClaw's messaging-channel setup. It won't give you a WhatsApp or iMessage interface, but it gives you a persistent, mobile-to-desktop execution loop.

### Step 4: Connect Claude Code Channels (Telegram/Discord)

If you want to trigger tasks from Telegram or Discord (closer to the OpenClaw messaging-native experience):

**Telegram:**
```bash
claude channel add telegram
# Follow the prompts to create a bot via BotFather and connect it
```

**Discord:**
```bash
claude channel add discord
# Follow the prompts to authorize a Discord bot to your server
```

Once connected, you can message your bot directly and Claude Code will execute tasks, report back, and maintain context.

### Step 5: Install Core MCP Servers

This is the equivalent of installing OpenClaw's integrations. Start with the highest-leverage ones:

```bash
# In Claude Code, add MCP servers
# Full syntax: claude mcp add [options] <name> -- <command> [args...]
# Example for an npm-based server:
claude mcp add gmail -- npx @anthropic/mcp-gmail
claude mcp add google-calendar -- npx @anthropic/mcp-google-calendar
claude mcp add github -- npx @anthropic/mcp-github
claude mcp add slack -- npx @anthropic/mcp-slack
claude mcp add puppeteer -- npx @anthropic/mcp-puppeteer   # web browsing
claude mcp add filesystem -- npx @anthropic/mcp-filesystem  # structured file ops
```

Verify:
```bash
claude mcp list
```

Each MCP server will prompt for authentication (OAuth or API key) on first use. Gmail and Calendar use Google OAuth — the same flow you'd use for any Google app.

### Step 6: Set Up Persistent Memory

**Auto Memory (Claude Code):**
No setup required. Claude Code automatically learns patterns across sessions. After a week of use, it will know your file structure, your preferred writing style, your common commands.

**Cowork Projects:**
1. Open Claude Desktop
2. Cowork → New Project
3. Name it (e.g., "Daily Automation", "Work Tasks", "Personal Ops")
4. Add custom instructions: your name, timezone, preferred formats, recurring priorities
5. Claude will maintain context across all sessions within that project

**CLAUDE.md files (for persistent instructions):**
Create a `~/.claude/CLAUDE.md` file with your global preferences:
```markdown
# My Preferences
- Name: Matt
- Timezone: [your timezone]
- Preferred output format: concise, action-oriented
- Email style: direct, no fluff
- Default calendar: work@yourdomain.com
```

### Step 7: Create Your First Scheduled Task

**The daily briefing** is the canonical first automation — same as OpenClaw users' killer use case.

In Claude Code:
```bash
claude schedule create "morning-briefing" \
  --cron "0 7 * * 1-5" \
  --prompt "Generate my morning briefing: check my calendar for today's events, check my email for anything urgent (flag senders I've starred before), give me a 3-item priority list for the day. Format it cleanly. Send it to my Telegram."
```

Or via the Cowork UI:
1. Open Claude Desktop → Cowork
2. New Scheduled Task
3. Set time: 7:00 AM weekdays
4. Write your prompt (include instructions about what to check and where to send it)

**Cloud vs. Desktop tasks:**
- **Cloud tasks** (Claude Code): Run on Anthropic's servers. Your computer doesn't need to be on. Use these for true 24/7 automation.
- **Desktop tasks** (Cowork): Run locally. More powerful (can use Computer Use, access local files), but require your Mac to stay on.

### Step 8: Build Your Skills Library

Skills are the Anthropic equivalent of ClawHub. They're SKILL.md files that define best practices and workflows Claude follows.

**Where to find skills:**
- Claude's built-in plugin system (available in Cowork)
- Community-built skills (search GitHub for `claude-skill`)
- Write your own

**Writing a skill (example: expense processing):**
```markdown
# SKILL.md — Expense Processing

When the user sends a photo of a receipt:
1. Extract: vendor name, date, amount, category
2. Append to expenses-tracking.xlsx in the "Expenses" tab
3. Rename the receipt file: YYYY-MM-DD_VendorName_$Amount.jpg
4. Move to /Receipts/[Year]/[Month]/
5. Confirm: "Added $[amount] at [vendor] on [date] to your tracker."
```

Save to `~/.claude/skills/expense-processing/SKILL.md` and Claude will use it automatically.

**High-value skills to build or find:**
- Email triage and response drafting
- Meeting notes → action items
- GitHub PR review
- Lead research and outreach
- Content drafting pipeline
- Expense processing (above)

### Step 9: Enable Computer Use

Computer Use lets Claude click, navigate, and control your Mac — the equivalent of OpenClaw's browser automation and form-filling.

1. Claude Desktop → Settings → Enable Computer Use
2. Claude will request Accessibility permissions (grant them)
3. Test: "Open Safari, search for [something], and tell me the first three results"

**Current limitations (March 2026):**
- Mac only (Windows/Linux in development)
- Research preview — occasional errors, especially on complex UI
- Permission-first: Claude asks before touching new applications
- Not suitable for fully unattended critical tasks yet (but improving fast)

**Use Computer Use for:**
- Filling forms on websites that don't have APIs
- Interacting with apps that don't have MCP servers
- Automating tasks in desktop apps (Notion, Excel, etc.)
- Web scraping when Puppeteer MCP isn't enough

### Step 10: Wire It All Together — Sample Daily Automation Stack

Here's a full stack that replicates what a power OpenClaw user would have running:

```
7:00 AM (Cloud task) → Morning briefing via Gmail MCP + Calendar MCP → sends to Telegram
7:15 AM (Cloud task) → Scan for urgent GitHub notifications → posts summary to Discord
As needed (Dispatch) → Send task from phone → executes on Mac → responds in Claude chat
On receipt photo (Cowork) → Expense processing skill → updates spreadsheet
Daily at 5 PM (Cloud task) → End-of-day summary: completed tasks, tomorrow's calendar → sends to Telegram
As needed (Computer Use) → Any UI-based task Matt delegates
```

---

## Part 5: Gaps and How to Work Around Them

### Gap 1: WhatsApp / iMessage / Signal Access

**The gap:** OpenClaw integrates natively with 15+ messaging platforms. Claude's Channels only cover Telegram and Discord. Dispatch adds mobile-to-desktop but through the Claude app, not native messaging apps.

**Workarounds:**
- Use Telegram as your primary command channel (it's excellent and has a great bot API)
- Use Dispatch for iOS/Android native feel
- Consider a Zapier or Make.com bridge: WhatsApp message → webhook → Claude Code API trigger (involves third-party tools, but keeps Claude as the brain)
- If WhatsApp Business API access is available: route through a custom MCP server

### Gap 2: No Open-Source / Self-Hosted Option

**The gap:** OpenClaw is MIT-licensed and runs entirely locally. Claude requires a paid subscription and makes API calls to Anthropic's servers.

**Workaround:** There isn't a true workaround — this is a fundamental architectural difference. For privacy-critical workflows, keep sensitive data out of prompts (process locally, only send metadata to Claude) or use Claude Code's local file access carefully.

### Gap 3: Cloud Scheduled Tasks Can't Use Computer Use

**The gap:** Cloud tasks run on Anthropic's servers, not your Mac. So they can't use Computer Use or access local files.

**Workaround:** Use cloud tasks for API-based work (email, calendar, GitHub, Slack) and desktop tasks for anything requiring local access or computer control. Design your automations accordingly — prefer MCPs over Computer Use where possible.

### Gap 4: No Model Agnosticism

**The gap:** OpenClaw works with Claude, GPT, Gemini, and local models via Ollama. The Anthropic stack is Claude-only.

**Workaround:** Not applicable if you're committed to Anthropic's stack. If model flexibility matters, OpenClaw remains the better choice.

---

## Part 6: Capability Tiers

Use this to decide what's worth setting up first:

### Tier 1: Quick Wins (Setup in < 1 hour)
- Install Claude Desktop + Claude Code + Claude mobile
- Set up Dispatch (mobile → desktop pairing)
- Connect Telegram channel to Claude Code
- Create morning briefing scheduled task (cloud)
- Enable Auto Memory

### Tier 2: High-Value Integrations (Setup in 1–4 hours)
- Gmail MCP (email triage + drafting)
- Google Calendar MCP (event management)
- GitHub MCP (PR reviews, issue management)
- File system skill (receipt processing, document organization)
- Write 2–3 core SKILL.md files for your most common tasks

### Tier 3: Advanced Automation (Ongoing, 1–2 weeks)
- Computer Use for UI-based tasks
- End-to-end email automation pipeline
- Lead research + outreach automation
- Full daily briefing with weather, calendar, email, health data
- Custom MCP server for anything without a pre-built integration

---

## Part 7: Companion Documents

### [openclaw-anthropic-artifact-comparison.md](./openclaw-anthropic-artifact-comparison.md)
A deep dive into every config file, memory file, skill file, and manifest that each system uses — with full schemas, side-by-side comparisons, full directory trees, and a practical migration guide. Key findings:

- OpenClaw splits agent identity across four files (`IDENTITY.md`, `SOUL.md`, `USER.md`, `AGENTS.md`); all four collapse into `~/.claude/CLAUDE.md` in Anthropic's world
- Both systems use `SKILL.md` with nearly identical formats and even the same `.skill` ZIP bundle convention — the closest point of alignment in the entire ecosystem
- Memory is structurally similar (`MEMORY.md` in both), but OpenClaw is date-organized (daily log files), while Anthropic is topic-organized
- OpenClaw uses one big `openclaw.json` (JSON5) for everything; Claude Code splits config across `settings.json`, `.mcp.json`, and `hooks.json`
- Several OpenClaw files have no Anthropic equivalent: `BOOTSTRAP.md`, `BOOT.md`, `HEARTBEAT.md`, `agents.yaml`, `openclaw.plugin.json`'s auth metadata
- Several Anthropic files have no OpenClaw equivalent: `.claude/rules/*.md` (path-scoped rules), `.lsp.json`, `file-history/`, `plans/`, `transcript.jsonl`

---

## Part 8: Key References

### Anthropic Tools
- [Claude Code docs](https://code.claude.com/docs)
- [Cowork getting started](https://support.claude.com/en/articles/13345190-get-started-with-cowork)
- [MCP server directory](https://github.com/modelcontextprotocol/servers)
- [Claude API models](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Claude Desktop download](https://claude.ai/download)

### OpenClaw (for reference / comparison)
- [OpenClaw website](https://openclaw.ai/)
- [OpenClaw docs](https://docs.openclaw.ai/)
- [ClawHub skill marketplace](https://clawhub.ai/)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)

### Related Reading
- [CNBC: OpenClaw's ChatGPT moment (March 2026)](https://www.cnbc.com/2026/03/21/openclaw-chatgpt-moment-sparks-concern-ai-models-becoming-commodities.html)
- [Axios: OpenClaw inspires industry (March 2026)](https://www.axios.com/2026/03/23/openclaw-agents-nvidia-anthropic-perplexity)
- [DigitalOcean: What is OpenClaw?](https://www.digitalocean.com/resources/articles/what-is-openclaw)

---

## Appendix: Things That Will Change

Both OpenClaw and Anthropic's tooling are moving extremely fast. Expect these to shift:

| Item | Direction |
|---|---|
| Computer Use (Mac only) | Windows + Linux support coming |
| Dispatch (Max only) | Pro access coming within weeks |
| Cloud scheduled tasks | More triggers, more channels |
| MCP ecosystem | Growing rapidly; more curated connectors incoming |
| OpenClaw v2026.3.22 | 12 breaking changes; stay on latest |
| ClawHub security | Still improving; verify skills before installing |

**Re-verify this document against current docs before implementing anything time-sensitive.** The research for this document was conducted on March 25, 2026.

---

*Document maintained in the Double Agent repo. If something is stale or wrong, update it here.*
