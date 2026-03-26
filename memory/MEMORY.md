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
- AGENTMAIL_API_KEY: `am_us_cfee6351afef1aa52c2a5c6ef0905df731b4544c9482ba05f8d18ada5fccb458` (set 2026-03-26)
- RESOLVED_SH_API_KEY: `aa_live_AGe6_1_hlqlVGx2AUu3Dx1WqItcgbw5l6EyEQbwzkes` (obtained 2026-03-26 via magic link to troubledgame123@agentmail.to)

## Pending
- EVM payout wallet: Matt needs to provide an address to register with resolved.sh (T06)
- agentagent.sh listing: needs to be registered on resolved.sh (registration is paid — confirm with Matt before proceeding)

## resolved.sh Account
- Email: troubledgame123@agentmail.to
- User ID: fca210ac-2f3c-4d59-ae55-298f52f1f2fe
- Existing listing: "Open Model Hub" (resource_id: 7ccc3061-655f-4f78-b5fd-ffa6a693ab3f, subdomain: open-model-hub-6780, active until 2027-03-13)
- Dashboard endpoint: GET /dashboard (session_token required), not /listings
