# TASKS.md — Double Agent

Entity-based task tracking. Each item is a discrete unit of work with an owner (agent or Matt) and a status.

---

## Status legend
- `[ ]` open
- `[x]` done
- `[-]` blocked

---

## Phase 0 — Seed Intelligence

| ID | Task | Owner | Status | Notes |
|----|------|-------|--------|-------|
| T01 | Pull all x402 ecosystem PRs from GitHub API into JSONL dataset | agent | `[ ]` | `github.com/coinbase/x402/pulls`, label=ecosystem, all statuses |
| T02 | Enrich first 50–100 company profiles (domain, GitHub, agent-card check) | agent | `[ ]` | Depends on T01 |
| T03 | Structure output as `.jsonl` per weekly snapshot | agent | `[ ]` | Schema in PROJECT_PLAN.md §0.3 |

---

## Phase 1 — Go Live on resolved.sh

| ID | Task | Owner | Status | Notes |
|----|------|-------|--------|-------|
| T04 | Get RESOLVED_SH_API_KEY via email magic link | Matt | `[x]` | Done 2026-03-26; key: `aa_live_WVnr0qZH...` (repulsivemeaning51@agentmail.to account) |
| T05 | Fix agentagent.sh listing (description, llms.txt, agent-card.json) | agent | `[x]` | Done 2026-03-26; live at agentagent-9576.resolved.sh with real description, agent-card.json (4 skills), and md_content |
| T06 | Register EVM payout wallet with resolved.sh | Matt | `[ ]` | `POST /account/payout-address`; needs wallet address from Matt |
| T07 | Upload first datasets and set prices (4 SKUs) | agent | `[-]` | Blocked on T04 + T01 |

**4 SKUs to publish:**
1. x402 Ecosystem — Full Company Index — $2.00/download — weekly refresh
2. x402 Ecosystem — New This Week — $0.50/download — weekly refresh
3. x402 Ecosystem — Merged Only (vetted) — $1.00/download — weekly refresh
4. x402 Ecosystem — Raw (all statuses) — $1.50/download — weekly refresh

---

## Phase 2 — Automate the Pipeline

| ID | Task | Owner | Status | Notes |
|----|------|-------|--------|-------|
| T08 | Set up scheduled automation (daily diff, weekly snapshot) | agent | `[ ]` | GitHub API scraper; cron via Claude scheduled tasks |
| T09 | Auto-publish updated dataset to resolved.sh listing | agent | `[ ]` | Depends on T04, T07, T08 |

---

## Infra / Tooling

| ID | Task | Owner | Status | Notes |
|----|------|-------|--------|-------|
| T10 | scripts/agentmail.py — list inboxes, read threads/messages | agent | `[x]` | Done |
| T11 | scripts/resolved_sh.py — list/create/update listings, upload datasets | agent | `[x]` | Done |
| T12 | Check agentmail inbox for resolved.sh magic link / welcome email | agent | `[x]` | Run after T10 |

---

## Phase 3 — Blog

| ID | Task | Owner | Status | Notes |
|----|------|-------|--------|-------|
| B10 | Publish launch post (free) — "The x402 Ecosystem: 311 Companies, 3 Signals, 1 Dataset" | agent | `[x]` | Done 2026-04-01; live at https://agentagent.resolved.sh/posts/x402-ecosystem-launch |
| B11 | Set up `double-agent-weekly-blog` scheduled task (Mon 10am JST) | agent | `[x]` | Done 2026-04-01; publishes free weekly digest of top 3-5 new x402 entries |
| B12 | ~~First paid post ($1.50) — "Top AI Agent Infrastructure Companies"~~ | agent | `[-]` | **Superseded** by weekly deep-research format (see B15) |
| B13 | ~~Second paid post ($1.50) — "x402 Adoption Trends"~~ | agent | `[-]` | **Superseded** by weekly deep-research format (see B15) |
| B14 | ~~Third paid post ($2.00) — "Which Companies Have Full Agent Signals?"~~ | agent | `[-]` | **Superseded** by weekly deep-research format (see B15) |
| B15 | Weekly paid deep-research post ($1.50) — rotating angles (signals, stacks, velocity, contributors, backlog) | agent | `[x]` | Done 2026-04-01; first post "x402-agent-signals-april-2026" live; scheduled task `weekly-deep-research-post` runs Mon 9am JST |

**Blog tiers:**
1. **Free** — Weekly "New This Week" digest (top 3-5 new entries, 300-500 words). Mon 10am JST. Drives traffic.
2. **Free** — Launch/flagship posts. Brand building.
3. **Paid ($1.50)** — Weekly deep-research analysis (rotating angles: agent signals, tech stack, category velocity, contributor power law, backlog health). Mon 9am JST.

---

## Backlog

| ID | Task | Owner | Status | Notes |
|----|------|-------|--------|-------|
| B01 | New entrant webhook/feed product | agent | `[ ]` | Phase 2.3 — after pipeline is running |
| B02 | Sector intelligence packs (infra / data / security) | agent | `[ ]` | Phase 3.2 |
| B03 | Expand data sources beyond x402 (resolved.sh feed, agent-card crawl, A2A) | agent | `[ ]` | Phase 3.3 |
| B04 | Publish x402 ecosystem dataset to HuggingFace | Matt | `[ ]` | Create dataset at huggingface.co/new-dataset, suggested name `hichana/x402-ecosystem`; upload `distribution/huggingface/README.md` as dataset card; optionally add HF_TOKEN to ~/.config/double-agent/.env for future automation |

---

## Blog

- [x] Write launch post (posts/2026-03-30-launch.md)
- [ ] Publish launch post to resolved.sh (POST /resources/{id}/posts, price_usdc: 0)
- [x] Publish first weekly deep-research post ($1.50) — "Agent Signals: What the x402 Backlog Tells Us" — live at slug `x402-agent-signals-april-2026`
- [x] Set up weekly deep-research scheduled task (`weekly-deep-research-post`, runs Mon 9am JST, rotates angle each week)
- [x] Set up weekly digest scheduled task (double-agent-weekly-blog, runs Mondays 10am)
- [ ] Set up HuggingFace dataset (see distribution/huggingface/README.md)
