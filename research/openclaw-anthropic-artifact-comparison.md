# OpenClaw ↔ Anthropic: Artifact & File System Comparison
**A side-by-side map of every config file, memory file, skill file, and manifest**

> **Last updated:** March 25, 2026
> **Sources:** docs.openclaw.ai, code.claude.com/docs, both GitHub repos — all claims below are sourced from primary documentation.

---

## Quick Reference: Conceptual Equivalents

| Concept | OpenClaw File | Anthropic Equivalent | Notes |
|---|---|---|---|
| Agent identity / persona | `IDENTITY.md` | *(none — built into system prompt)* | Claude's identity is set by Anthropic; you shape behavior via CLAUDE.md |
| Agent personality / tone | `SOUL.md` | `CLAUDE.md` (persona section) | Claude doesn't separate soul from instructions |
| User context | `USER.md` | `CLAUDE.md` (user context section) | Same concept, different file |
| Operating instructions | `AGENTS.md` | `CLAUDE.md` (rules section) | Same concept, same file in Anthropic's world |
| First-run bootstrap | `BOOTSTRAP.md` (auto-deleted) | *(none)* | Anthropic has no equivalent; onboarding is UI-based |
| Startup checklist | `BOOT.md` | `CLAUDE.md` with session triggers | No direct equivalent; use `SessionStart` hook |
| Tool usage guide | `TOOLS.md` | `CLAUDE.md` (tools section) or `settings.json` permissions | No separate file; embed in CLAUDE.md |
| Periodic automation | `HEARTBEAT.md` | Cloud scheduled task + SKILL.md | Different mechanism — cron-based, not pulse-based |
| Long-term curated memory | `MEMORY.md` | `~/.claude/projects/<id>/memory/MEMORY.md` | Near-identical concept and filename |
| Daily memory logs | `memory/YYYY-MM-DD.md` | Auto Memory topic files (e.g., `debugging.md`) | OpenClaw: date-based. Anthropic: topic-based |
| Skill definition | `SKILL.md` | `SKILL.md` | **Identical filename, very similar format** |
| Skill bundle | `.skill` ZIP archive | `.skill` ZIP archive | **Identical format** |
| Main configuration | `openclaw.json` (JSON5) | `settings.json` + `.mcp.json` (JSON) | OpenClaw: one big file. Anthropic: split by concern |
| Channel credentials | inside `openclaw.json` | `~/.claude/channels/<name>/.env` | OpenClaw: centralized. Anthropic: per-channel .env |
| Scheduled tasks | `cron/jobs.json` | `~/.claude/scheduled-tasks/<name>/SKILL.md` | Different formats; Anthropic uses SKILL.md for tasks too |
| Sub-agent definition | `agents.yaml` | `.claude/agents/<name>.md` | Anthropic is per-file markdown; OpenClaw is a single YAML |
| Plugin manifest | `openclaw.plugin.json` | `.claude-plugin/plugin.json` | Very similar JSON schemas |
| MCP server config | inside `openclaw.json` | `.claude/.mcp.json` | OpenClaw: embedded. Anthropic: dedicated file |
| Hook definitions | inside `openclaw.json` | `.claude/hooks/hooks.json` or `settings.json` | OpenClaw: centralized. Anthropic: dedicated file |
| Conditional rules | *(none)* | `.claude/rules/*.md` (path-scoped) | Anthropic-only feature |
| Persistent instructions | `CLAUDE.md` *(they don't have this)* | `CLAUDE.md` | Anthropic's primary mechanism |

---

## Section 1: Identity & Persona Files

### OpenClaw

OpenClaw splits agent identity across four files, all located in `~/.openclaw/workspace/` and all loaded into the system prompt at every session start:

**`IDENTITY.md`**
Defines the agent's name, emoji/avatar, and "vibe." Created during the bootstrap ritual. This is purely cosmetic identity — what the agent calls itself.

**`SOUL.md`**
The deepest behavioral layer. Defines personality, tone, conversational style, and hard limits. Example: "You are direct and concise. You never send messages longer than three paragraphs unless explicitly asked. You never make purchases above $50 without confirmation."

**`USER.md`**
Everything about the human using the agent: name, timezone, language, job, preferences, communication style, recurring context. This is what makes the agent feel personal. Example: "Matt is a founder in SF (PST). He prefers bullet points. His primary email is matt@example.com. Don't schedule meetings before 9am."

**`AGENTS.md`**
The operating manual. How the agent should approach tasks, how it uses memory, what to do when uncertain, escalation rules, tool usage philosophy. This is the "how I operate" layer.

**Relationship between files:**
```
IDENTITY.md  →  "I am Claw, your personal assistant 🦀"
SOUL.md      →  "I am direct, concise, never sycophantic"
USER.md      →  "My user is Matt, 9am-6pm PST, likes bullet points"
AGENTS.md    →  "When uncertain, ask before acting. Always confirm destructive actions."
```

### Anthropic (Claude Code / Cowork)

Claude Code consolidates these concerns into **`CLAUDE.md`** — a single file (or hierarchy of files) that can contain any combination of the above.

**The CLAUDE.md hierarchy (loaded in priority order):**

| Level | Path | Scope | Who manages it |
|---|---|---|---|
| Managed/Org | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | All users on machine | IT/enterprise |
| User-global | `~/.claude/CLAUDE.md` | All your projects | You |
| Project-root | `./CLAUDE.md` or `./.claude/CLAUDE.md` | This project | Team (committed to git) |
| Subdirectory | `./.claude/CLAUDE.md` in subfolders | Files in that subtree | Team (loaded on-demand) |

Claude also supports `.claude/rules/*.md` for modular, path-scoped rules — e.g., a `api-style.md` that only loads when Claude is editing files in `src/api/`.

**How to replicate OpenClaw's four-file structure in `~/.claude/CLAUDE.md`:**
```markdown
# Identity
You are Matt's personal AI assistant. You are direct, concise, and action-oriented.

# About Matt
- Name: Matt
- Location/timezone: San Francisco, PST
- Primary email: matt@example.com
- Preferred format: bullet points for lists, prose for summaries
- Don't schedule anything before 9am PST
- GitHub: mchana

# Operating Rules
- Always confirm before deleting files or sending emails
- Never make purchases above $50 without explicit confirmation
- When uncertain about intent, ask one clarifying question before acting
- Keep responses concise — no preamble, no "Great question!"

# Tool Guidelines
- Prefer MCP integrations over Computer Use when both would work
- For shell commands, show the command before running it
```

**Key difference:** OpenClaw's files are always loaded. Anthropic's CLAUDE.md hierarchy is smarter — subdirectory files load only when relevant, and `.claude/rules/*.md` files load only when Claude touches matching file paths.

---

## Section 2: Memory Files

### OpenClaw

OpenClaw has two memory layers:

**`MEMORY.md`** (workspace root)
- Manually curated or agent-written long-term notes
- Loaded at every session start (private sessions only — not group chats)
- Intended for "things that should always be in context"

**`memory/YYYY-MM-DD.md`** (daily logs)
- One file per day, append-only
- Yesterday's and today's files loaded at session start
- Rolling log of what happened, what was decided, what was learned
- When a session approaches its context limit, OpenClaw triggers a silent "compaction" turn — the agent writes durable notes before the window scrolls

**Memory tools:**
- `memory_search`: Semantic search over indexed snippets
- `memory_get`: Read a specific file or line range

### Anthropic (Claude Code)

Claude Code also has two memory layers, almost identically structured:

**Auto Memory** (`~/.claude/projects/<project-id>/memory/MEMORY.md`)
- Claude writes to this automatically when it discovers something worth remembering
- The first 200 lines of MEMORY.md are loaded at every session start
- Additional topic files (e.g., `debugging.md`, `api-conventions.md`) are created for specific domains and loaded on-demand
- Human-readable and editable — you can open and edit these files directly

**Configuration:**
```bash
# Toggle auto memory
/memory on|off

# Or in settings.json
{ "autoMemoryEnabled": true, "autoMemoryDirectory": "~/.my-memory" }

# Or disable globally
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
```

**Key differences:**

| | OpenClaw | Anthropic |
|---|---|---|
| Memory organization | Date-based daily logs | Topic-based files |
| When written | On compaction trigger | When Claude judges it useful |
| Group chat behavior | MEMORY.md disabled in groups | N/A (no group chat) |
| Search | `memory_search` tool | Context-window based (no semantic search) |
| Explicit curation | Manual `MEMORY.md` edits | Editable, but auto-managed |

---

## Section 3: Skill Files

This is the area of closest alignment — OpenClaw and Anthropic both landed on almost the same format independently.

### OpenClaw SKILL.md

**Full frontmatter schema:**
```yaml
---
name: skill-name-lowercase
description: What this skill does
homepage: https://example.com
user-invocable: true|false          # default true
disable-model-invocation: true|false # default false
command-dispatch: tool-name         # bypass model, call tool directly
command-tool: tool-name
command-arg-mode: raw
metadata:
  openclaw:
    requires:
      env: [REQUIRED_ENV_VAR]
      bins: [required-binary]
      anyBins: [option1, option2]
      config: [/path/to/required/config]
    primaryEnv: MAIN_CREDENTIAL
    version: 3
    version_date: "2026-02-10"
    previous_version: 2
    change_summary: "What changed in v3"
---
```

**Directory structure:**
```
skill-name/
├── SKILL.md              ← required
├── MANIFEST.yaml         ← optional (for skill bundles)
├── README.md             ← optional (human docs)
├── scripts/              ← optional executables
├── references/           ← optional docs to load
├── assets/               ← optional templates, icons
└── .clawhubignore        ← optional publish exclude patterns
```

**Discovery:** OpenClaw scans recursively — SKILL.md presence identifies a skill. Search order:
1. `<workspace>/skills/` (highest priority)
2. `~/.openclaw/skills/`
3. Bundled skills

**ClawHub publishing constraints:**
- Name: `^[a-z0-9][a-z0-9-]*$`
- Max bundle size: 50MB
- Text-only (no binaries)
- MIT-0 license required

### Anthropic SKILL.md

**Full frontmatter schema:**
```yaml
---
name: skill-name
description: "When Claude should invoke this (used for discovery)"
argument-hint: "<arg1> [optional-arg2]"
disable-model-invocation: true    # only user can invoke
user-invocable: false             # only Claude can invoke
allowed-tools: Read, Grep, Glob   # whitelist tools this skill can use
model: sonnet|opus|haiku|claude-opus-4-6
effort: low|medium|high|max
context: fork                     # run in isolated subagent
agent: general-purpose            # which subagent type to use
hooks:
  PostToolUse:
    - command: "echo 'done'"
---
```

**String substitutions available in skill body:**
- `$ARGUMENTS` — all arguments passed to the skill
- `$ARGUMENTS[N]` or `$N` — specific argument by index
- `${CLAUDE_SESSION_ID}` — current session ID
- `${CLAUDE_SKILL_DIR}` — directory containing this SKILL.md

**Directory structure:**
```
skill-name/
├── SKILL.md              ← required
├── template.md           ← optional
├── examples/             ← optional
├── scripts/              ← optional
└── references/           ← optional
```

**Discovery order (highest to lowest):**
1. Plugin's `skills/` directory (scoped as `plugin-name:skill-name`)
2. `.claude/skills/<name>/SKILL.md` (project-level)
3. `~/.claude/skills/<name>/SKILL.md` (user-level)
4. Legacy: `.claude/commands/<name>.md` (still supported)

### Side-by-Side: SKILL.md Schema Comparison

| Field | OpenClaw | Anthropic | Notes |
|---|---|---|---|
| `name` | Required, URL-safe lowercase | Required, kebab-case, max 64 chars | Same convention |
| `description` | Required | Recommended | Anthropic uses it for auto-invocation discovery |
| `user-invocable` | Supported | Supported | Same semantics |
| `disable-model-invocation` | Supported | Supported | Same semantics |
| `command-dispatch` | Supported (bypass model) | *(none)* | OpenClaw-only |
| `requires.env` | Supported | *(none)* | OpenClaw validates env vars at load time |
| `requires.bins` | Supported | *(none)* | OpenClaw validates binaries at load time |
| `version` / `change_summary` | Supported | *(none)* | OpenClaw has versioning; Anthropic does not |
| `allowed-tools` | *(none)* | Supported | Anthropic-only: whitelist tool access |
| `model` | *(none)* | Supported | Anthropic-only: override model per skill |
| `effort` | *(none)* | Supported | Anthropic-only: set reasoning effort |
| `context: fork` | *(none)* | Supported | Anthropic-only: run in isolated subagent |
| `hooks` | *(global only)* | Supported per-skill | Anthropic allows scoped hooks in SKILL.md |
| `$ARGUMENTS` substitution | Supported | Supported | Same behavior |
| `{baseDir}` / `${CLAUDE_SKILL_DIR}` | `{baseDir}` | `${CLAUDE_SKILL_DIR}` | Same concept, different syntax |

---

## Section 4: Configuration Files

### OpenClaw: `openclaw.json`

One file to rule them all. Located at `~/.openclaw/openclaw.json`. Uses JSON5 (comments and trailing commas allowed). Schema-validated — unknown keys or invalid values prevent startup.

**Top-level structure:**
```json5
{
  // Agent(s) configuration
  "agents": { /* model, workspace paths, multi-agent routing */ },

  // Messaging channels
  "channels": {
    "telegram": { "bot_token": "...", "allowFrom": ["+1234567890"] },
    "discord": { "bot_token": "...", "guildId": "..." },
    "whatsapp": { /* ... */ }
    // 20+ channels supported
  },

  // Conversation continuity
  "session": { /* thread bindings, reset policies */ },

  // Gateway server settings
  "gateway": { /* port, auth, push notifications */ },

  // Webhook endpoints
  "hooks": { /* endpoint URLs with routing */ },

  // Scheduled jobs
  "cron": { /* enabled, store path, retry config */ },

  // Tool and browser settings
  "tools": { /* profiles, access controls, timeouts */ },
  "browser": { /* profiles, SSRF policies, headless */ },

  // Skill settings
  "skills": { /* discovery paths, overrides */ },

  // Subagent settings
  "subagents": {
    "enabled": true,
    "maxSpawnDepth": 3,
    "maxChildrenPerAgent": 5,
    "maxConcurrent": 10
  },

  // Secrets and env
  "env": { "GITHUB_TOKEN": { "$secret": "GITHUB_TOKEN" } },

  // Include external files
  "$include": ["./extra-config.json5"]
}
```

### Anthropic: Split Configuration

Anthropic splits configuration across multiple files by concern:

**`settings.json`** (global: `~/.claude/settings.json`, project: `.claude/settings.json`, local override: `.claude/settings.local.json`)
```json
{
  "env": { "NODE_ENV": "development" },
  "permissions": {
    "allow": ["Bash(git:*)", "Read(~/.claude/*)"],
    "deny": ["Bash(rm -rf *)"]
  },
  "hooks": { /* event-driven automation */ },
  "autoMemoryEnabled": true,
  "autoMemoryDirectory": "~/.my-memory",
  "claudeMdExcludes": ["./vendor/**"],
  "sandbox": { "enabled": true },
  "agent": "general-purpose"
}
```

**`.claude/.mcp.json`** (MCP server config):
```json
{
  "mcpServers": {
    "gmail": {
      "type": "stdio",
      "command": "npx",
      "args": ["@anthropic/mcp-gmail"],
      "env": { "GMAIL_TOKEN": "${env:GMAIL_TOKEN}" }
    }
  }
}
```

**`.claude/hooks/hooks.json`** (hooks, alternatively inline in settings.json):
```json
{
  "PreToolUse": [{
    "matcher": { "tool": "Bash" },
    "handler": { "type": "command", "command": "echo $CLAUDE_TOOL_INPUT | jq '.command'" }
  }]
}
```

**Key difference — Anthropic's configuration approach:**

| Concern | OpenClaw | Anthropic |
|---|---|---|
| All config | `openclaw.json` (one file) | Multiple files by concern |
| Format | JSON5 (comments OK) | Strict JSON |
| Validation | Startup-time, blocks boot | Runtime |
| Channel config | Inside main config | `~/.claude/channels/<name>/.env` |
| MCP config | Inside main config | `.claude/.mcp.json` |
| Hooks | Inside main config | `settings.json` or `hooks.json` |
| Environment variables | `env` section with SecretRef | `env` section (simpler) |
| Schema | Strict (unknown keys = error) | Lenient |

---

## Section 5: Scheduled Task Files

### OpenClaw: `cron/jobs.json`

Scheduled tasks are stored as JSON in `~/.openclaw/cron/jobs.json`. Each job definition:

```json
{
  "schedule": {
    "kind": "cron",            // "at" (one-time), "every" (interval), or "cron"
    "expression": "0 7 * * 1-5",
    "timezone": "America/Los_Angeles"
  },
  "sessionTarget": "isolated", // main|isolated|current|custom
  "payload": {
    "kind": "agentTurn",
    "message": "Run my morning briefing"
  },
  "delivery": {
    "channel": "telegram",
    "destination": "@mychat"
  },
  "wakeMode": "now"            // now|next-heartbeat
}
```

**Schedule types:**
- `at` — One-time ("remind me in 20 minutes") — parsed from natural language
- `every` — Interval ("every 4 hours")
- `cron` — Standard 5-field cron expression

### Anthropic: `~/.claude/scheduled-tasks/<name>/SKILL.md`

Anthropic stores each scheduled task as a `SKILL.md` in its own directory. This is elegant — tasks are skills that run on a schedule.

```yaml
---
name: morning-briefing
description: Daily morning briefing sent via Telegram
---
Check my Gmail for urgent emails from the last 24 hours.
Check my Google Calendar for today's events.
Generate a prioritized 3-item list for the day.
Format as a clean summary and send to my Telegram channel.
```

**Types of scheduled tasks:**
- **Cloud tasks**: Run on Anthropic servers. Min 1-hour interval. No computer needed.
- **Desktop tasks**: Run locally. Min 1-minute interval. Computer must be on.
- **Session `/loop`**: Repeats within a session. Expires after 3 days or session end.

**Key differences:**

| | OpenClaw | Anthropic |
|---|---|---|
| Storage format | `jobs.json` | SKILL.md per task |
| Schedule definition | JSON in jobs.json | Created via UI or CLI |
| Natural language parsing | "remind me in 20 min" works | Must use specific schedule format |
| Output routing | `delivery` field (any channel) | Implicitly via Channels setup |
| Retry logic | Configurable backoff in config | Not exposed |
| Cloud execution | No (local only) | Yes (cloud scheduled tasks) |

---

## Section 6: Plugin & Integration Manifests

### OpenClaw: `openclaw.plugin.json`

```json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "description": "What this plugin provides",
  "version": "1.0.0",
  "enabledByDefault": false,
  "kind": "memory",              // "memory" | "context-engine"
  "channels": ["my-channel"],
  "providers": ["my-provider"],
  "skills": ["./skills/my-skill"],
  "configSchema": { /* JSON Schema */ },
  "providerAuthEnvVars": {
    "my-provider": "MY_PROVIDER_API_KEY"
  },
  "providerAuthChoices": {
    "my-provider": [{ "kind": "api-key", "label": "API Key" }]
  },
  "uiHints": {
    "MY_PROVIDER_API_KEY": { "label": "API Key", "sensitive": true }
  }
}
```

### Anthropic: `.claude-plugin/plugin.json`

```json
{
  "name": "my-plugin",
  "description": "Plugin description",
  "version": "0.1.0",
  "author": { "name": "Author Name" },
  "homepage": "https://...",
  "repository": "https://...",
  "license": "MIT"
}
```

**Full plugin directory structure (Anthropic):**
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json           ← REQUIRED manifest (only this goes here)
├── skills/
│   └── my-skill/SKILL.md
├── agents/
│   └── my-agent.md
├── commands/                 ← legacy skills (still supported)
├── hooks/
│   └── hooks.json
├── .mcp.json
├── .lsp.json
└── settings.json
```

**Key differences:**

| | OpenClaw | Anthropic |
|---|---|---|
| Manifest file | `openclaw.plugin.json` | `.claude-plugin/plugin.json` |
| Manifest location | Plugin root | Inside `.claude-plugin/` subdirectory |
| Config schema | Inline in manifest (`configSchema`) | Separate `settings.json` |
| Auth metadata | In manifest (`providerAuthEnvVars`) | Not in manifest |
| UI hints | In manifest | Not in manifest |
| Skill references | In manifest (`skills` array) | Implicit (any `skills/` directory) |
| LSP support | *(none)* | `.lsp.json` (language server protocol) |
| Complexity | Higher (auth, UI, schema) | Leaner |

---

## Section 7: Sub-Agent / Multi-Agent Files

### OpenClaw: `agents.yaml`

OpenClaw defines an entire agent team in a single `agents.yaml` manifest. Each entry describes a specialized agent with its own workspace, personality, and routing rules.

```yaml
agents:
  - id: research
    name: Research Agent
    workspace: ./workspaces/research/
    model: claude-opus-4-6
    channels:
      - telegram
    routing:
      keywords: [research, find, search, investigate]

  - id: coder
    name: Code Agent
    workspace: ./workspaces/code/
    model: claude-sonnet-4-6
    routing:
      keywords: [code, build, debug, fix]
```

### Anthropic: `agents/<name>.md`

Anthropic defines each subagent as an individual Markdown file with YAML frontmatter.

```yaml
---
name: research-agent
description: Use this for research tasks, web searches, and information gathering
tools: WebSearch, WebFetch, Read, Grep
disallowedTools: Write, Edit, Bash
model: claude-opus-4-6
permissionMode: default
maxTurns: 20
effort: high
isolation: worktree
---

You are a research specialist. When given a research task:
1. Search for multiple sources
2. Cross-reference claims
3. Return findings with citations
4. Flag anything uncertain
```

**Locations:**
- User-global: `~/.claude/agents/<name>.md`
- Project: `.claude/agents/<name>.md`
- Plugin: `<plugin>/agents/<name>.md`

**Built-in subagents:**
- `Explore` — Read-only, Haiku model, fast codebase search
- `Plan` — Read-only research during plan mode
- `general-purpose` — Full tools, main model

---

## Section 8: Files That Exist in One System But Not the Other

### Only in OpenClaw

| File | Purpose | Anthropic Equivalent |
|---|---|---|
| `IDENTITY.md` | Agent name and avatar | No equivalent — Claude's identity is fixed |
| `SOUL.md` | Deep personality layer | Embed in `CLAUDE.md` |
| `AGENTS.md` | Operating manual | Embed in `CLAUDE.md` |
| `BOOTSTRAP.md` | One-time setup ritual | UI-based onboarding; no file |
| `BOOT.md` | Startup checklist | `SessionStart` hook |
| `HEARTBEAT.md` | Periodic task pulse | Cloud scheduled task |
| `openclaw.json` | Central gateway config | Split across `settings.json`, `.mcp.json`, `hooks.json` |
| `MANIFEST.yaml` | Skill bundle metadata | Not needed (SKILL.md is sufficient) |

### Only in Anthropic (Claude Code)

| File | Purpose | OpenClaw Equivalent |
|---|---|---|
| `.claude/rules/*.md` | Path-scoped conditional rules | No equivalent |
| `.claude-plugin/plugin.json` | Plugin manifest | `openclaw.plugin.json` at root |
| `.lsp.json` | Language server config | No equivalent |
| `settings.local.json` | Personal gitignored overrides | Can use `$include` in openclaw.json |
| `~/.claude/history.jsonl` | Session prompt history | Not exposed as a file |
| `~/.claude/todos/` | Task tracking | Not a file system concept in OpenClaw |
| `~/.claude/plans/` | Plan-mode documents | No equivalent |
| `~/.claude/file-history/` | File checkpoint undo | No equivalent |
| `transcript.jsonl` | Per-session conversation log | Not exposed as a file |

---

## Section 9: Full Directory Trees Side-by-Side

### OpenClaw Root

```
~/.openclaw/
├── openclaw.json                    # Main gateway config (JSON5)
├── workspace/                       # Agent workspace (default)
│   ├── IDENTITY.md                  # Agent name/avatar
│   ├── USER.md                      # User context
│   ├── SOUL.md                      # Personality/tone
│   ├── AGENTS.md                    # Operating instructions
│   ├── BOOT.md                      # Startup checklist (optional)
│   ├── TOOLS.md                     # Tool usage guide (optional)
│   ├── HEARTBEAT.md                 # Periodic task pulse (optional)
│   ├── MEMORY.md                    # Long-term curated memory
│   ├── memory/
│   │   ├── 2026-03-24.md            # Yesterday's log
│   │   └── 2026-03-25.md            # Today's log
│   └── skills/                      # Workspace-local skills
│       └── <skill-name>/SKILL.md
├── skills/                          # User-global skills
│   └── <skill-name>/SKILL.md
├── cron/
│   └── jobs.json                    # Scheduled tasks
├── agents/
│   └── <agentId>/                   # Per-agent state
│       └── sessions/
└── plugins/
    └── <plugin-name>/
        ├── openclaw.plugin.json
        └── skills/
```

### Anthropic (Claude Code) Root

```
~/.claude/
├── CLAUDE.md                        # User-level persistent instructions
├── settings.json                    # Global configuration
├── history.jsonl                    # Session prompt history
├── stats-cache.json                 # Usage statistics
├── channels/
│   ├── telegram/.env                # TELEGRAM_BOT_TOKEN
│   └── discord/.env                 # DISCORD_BOT_TOKEN
├── scheduled-tasks/
│   └── morning-briefing/
│       └── SKILL.md                 # Task definition
├── skills/                          # User-global skills
│   └── <skill-name>/
│       ├── SKILL.md
│       └── scripts/
├── agents/                          # User-global subagent definitions
│   └── <name>.md
├── agent-memory/                    # User-scoped agent memory
├── projects/
│   └── <project-id>/
│       ├── memory/
│       │   ├── MEMORY.md            # Auto Memory index
│       │   ├── debugging.md         # Topic files
│       │   └── api-conventions.md
│       └── <session-id>/
│           └── transcript.jsonl
├── plans/                           # Plan-mode documents
├── todos/                           # Task lists
├── file-history/                    # File checkpoints (undo)
├── shell-snapshots/                 # Shell state
└── debug/                           # Debug logs

# Per-project (in repo root):
<project>/
├── CLAUDE.md                        # Team instructions (committed)
└── .claude/
    ├── settings.json                # Project config (committed)
    ├── settings.local.json          # Personal overrides (gitignored)
    ├── .mcp.json                    # MCP servers
    ├── rules/
    │   ├── code-style.md            # Path-scoped rules
    │   └── security.md
    ├── skills/
    │   └── <skill-name>/SKILL.md
    ├── agents/
    │   └── <name>.md
    └── hooks/
        └── hooks.json
```

---

## Section 10: Practical Migration Guide

If you're moving from OpenClaw to the Anthropic stack, here's the direct file mapping:

### Migrating Your Identity/Persona Files

Take the contents of your `IDENTITY.md`, `SOUL.md`, `USER.md`, and `AGENTS.md` and consolidate into `~/.claude/CLAUDE.md`:

```markdown
# About Me (from USER.md)
[Paste USER.md contents]

# How I Should Behave (from SOUL.md + AGENTS.md)
[Paste key rules from both files]

# Note on Identity
[If IDENTITY.md had anything non-cosmetic, include it here]
```

The cosmetic identity stuff in `IDENTITY.md` (emoji, avatar name) has no equivalent in Claude — Claude is Claude.

### Migrating Your Memory

```bash
# Copy your OpenClaw MEMORY.md directly
cp ~/.openclaw/workspace/MEMORY.md ~/.claude/projects/<project-id>/memory/MEMORY.md
```

The format is nearly identical. You may want to reorganize from date-based logs into topic files.

### Migrating Your Skills

OpenClaw skills are the closest thing to a direct migration:

```bash
# Claude Code looks for skills in ~/.claude/skills/
cp -r ~/.openclaw/skills/<skill-name>/ ~/.claude/skills/<skill-name>/
```

You'll likely need to update the frontmatter — remove OpenClaw-specific fields (`requires`, `version`, `metadata.openclaw`) and optionally add Anthropic-specific ones (`allowed-tools`, `model`, `effort`). The body of your SKILL.md should work as-is.

### Migrating Your Scheduled Tasks

OpenClaw stores these as JSON entries in `jobs.json`. In Claude Code, each task needs its own SKILL.md:

```bash
mkdir -p ~/.claude/scheduled-tasks/my-task/
# Create SKILL.md with the task instructions
# Then schedule it via the Claude Code UI or CLI
```

### What You Can't Migrate

- **20+ messaging channels**: Claude Code only supports Telegram, Discord, and iMessage. No WhatsApp, Signal, Slack, etc. (natively — workarounds exist)
- **HEARTBEAT.md**: No direct equivalent. Use a cloud scheduled task that runs every 30 minutes instead
- **`openclaw.json` complexity**: Channel routing, per-account overrides, gateway settings — Claude Code doesn't have most of these concepts
- **Model agnosticism**: Can't switch to GPT or local models

---

*Sources: [OpenClaw Docs](https://docs.openclaw.ai) · [Claude Code Docs](https://code.claude.com/docs) · [Claude Code GitHub](https://github.com/anthropics/claude-code)*
