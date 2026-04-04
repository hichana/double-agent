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

## Credentials
- Keys live in `~/Documents/double-agent/.env` (repo root, gitignored)
- Load with: `source ~/Documents/double-agent/.env` or `export $(cat ~/Documents/double-agent/.env | xargs)`
- AGENTMAIL_API_KEY: cycled 2026-03-27 (new key from Downloads/Untitled.rtf)
- RESOLVED_SH_API_KEY: cycled 2026-03-27 via magic link to repulsivemeaning51@agentmail.to (label: double-agent-key)

## Pending
- EVM payout wallet: Matt needs to provide an address to register with resolved.sh (T06)

## resolved.sh Account (Double Agent / agentagent.sh)
- Email: repulsivemeaning51@agentmail.to
- User ID: 29ad4e4d-e3f2-4f9f-b1c1-ad98361236f0
- Listing: "Double Agent" (resource_id: e8592c18-9052-47b5-bfa3-bfe699193d0e, subdomain: agentagent, active until 2027-03-13)
- Current description: "An agent that agents agentically." — needs updating
- Theme: dark + #00d4ff accent (accepted by API schema, not yet persisted server-side — resolved.sh bug)
- Dashboard endpoint: GET /dashboard (session_token required); per-resource ops use API key
- Note: troubledgame123@agentmail.to is a separate/wrong account ("Open Model Hub") — ignore it
