# Memory

_Initialized during onboarding — 2026-03-25_

---

## Project
- Double Agent: competitive intelligence + replication playbook for the agent-economy
- Current focus: mapping OpenClaw's UX/architecture to Anthropic's stack
- Repo is the source of truth; Claude commits, Matt pushes

## Decisions
- Skills are project-scoped (`.claude/skills/`), not global
- agentmail and resolved-sh are the two active skills
- Confirm only before irreversible actions; everything else: proceed and report

## Pending
- AGENTMAIL_API_KEY not yet set (needed for agentmail skill)
- RESOLVED_SH_API_KEY not yet set (needed for resolved-sh skill — get via email magic link or GitHub OAuth at resolved.sh)
