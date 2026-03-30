# Double Agent — Project Plan
**Tagline: "Agent watching agents."**
**Domain: [agentagent.sh](https://agentagent.sh)**

---

## Mission

Build an autonomous competitive intelligence platform that tracks agent-based companies operating in the emerging agent economy, starting with a single, high-signal data source and expanding from there.

---

## Phase 0 — Seed Intelligence
*Start immediately. Objective: Build the first dataset before writing a single line of product code.*

### 0.1 — Mine the x402 PR Stream

The Coinbase x402 repo (`github.com/coinbase/x402/pulls`) is a living registry of companies self-identifying as agent-economy participants. Every ecosystem PR is a company raising its hand and saying *"we exist, here's what we do."*

**What to capture from every ecosystem-labeled PR (open + closed):**

| Field | Source |
|---|---|
| Company name | PR title |
| PR status | open / merged / closed / draft |
| Submission date | PR timestamp |
| GitHub author | PR submitter handle |
| Category | facilitator / service / SDK / data / infra |
| Description | PR body |
| Website / domain | PR body or linked files |
| Linked repo | PR source fork |
| Last activity | PR `updated_at` |

**Why all statuses matter:**

- **Merged** — legitimate, accepted x402 partner
- **Closed / rejected** — companies that tried but didn't make the cut; still real signals
- **Open** — aspiring; signals momentum and intent
- **Draft** — very early stage; earliest possible signal

From today's snapshot, the first page alone surfaces: ClearAgent, ClawPurse, Octav, Satring, Compintel, GPU-Bridge, PayCrow, Mercury Trust, SATP, AgenticTotem, KnowMint, x402Scout, NexusWeb3, Silverback, Alby, Mcpkeeper — 15+ companies in a single page, across hundreds of pages of history.

### 0.2 — Enrich Each Company Profile

For each captured company, the agent enriches the profile:

- Resolve domain → scrape description, product category, tech stack signals
- Check for resolved.sh / `agent-card.json` / `llms.txt` presence
- GitHub profile of submitter → other repos, activity, org affiliation
- Check for Twitter/X, LinkedIn presence
- Note: data offering, pricing model (if visible), payment method

### 0.3 — Structure the Dataset

Output: a `.jsonl` file per weekly snapshot, structured as:

```json
{
  "company": "ClearAgent",
  "domain": "clearagent.xyz",
  "category": "agent_services",
  "x402_pr": 1638,
  "pr_status": "open",
  "pr_date": "2026-03-16",
  "description": "...",
  "github_author": "babaeaterbeep",
  "agent_native": true,
  "resolved_sh": false,
  "enrichment_date": "2026-03-25"
}
```

This is the first product Double Agent sells.

---

## Phase 1 — Go Live on resolved.sh
*Week 1–2. Objective: Stand up the storefront and publish the first dataset.*

### 1.1 — Flesh Out the agentagent.sh Listing

Update the resolved.sh listing with:

- **Display name:** Double Agent
- **Description:** "Competitive intelligence on agent-economy companies. We watch the agents so you don't have to."
- **llms.txt:** Machine-readable description of what's for sale, formats, and pricing

### 1.2 — Register Payout Wallet

Set up an EVM wallet address to receive USDC payments via x402 on Base.

### 1.3 — Publish First Datasets

Upload initial `.jsonl` and `.csv` files to the listing:

| Dataset | Price | Refresh |
|---|---|---|
| x402 Ecosystem — Full Company Index | $2.00 | Weekly |
| x402 Ecosystem — New This Week | $0.50 | Weekly |
| x402 Ecosystem — Merged Only (vetted) | $1.00 | Weekly |
| x402 Ecosystem — Raw (all statuses) | $1.50 | Weekly |

---

## Phase 2 — Automate the Pipeline
*Week 2–4. Objective: The agent runs this itself — no human in the loop.*

### 2.1 — GitHub Scraper Agent

A scheduled agent that:

- Hits the GitHub API for all x402 PRs with label `ecosystem`
- Diffs against the previous snapshot to detect new entries
- Enriches new entries (domain lookup, GitHub profile, agent-card check)
- Appends to the master dataset

**Cadence:** Daily diff run, full snapshot weekly.

### 2.2 — Auto-Publish to resolved.sh

The agent automatically:

- Packages the updated dataset as `.jsonl`
- PUTs the new file to the resolved.sh listing with a price
- Updates `llms.txt` with a freshness timestamp and new file listing

### 2.3 — New Entrant Alerts *(Optional Early Win)*

Sell a "new entrants" webhook/feed — notify buyers when new companies appear. High perceived value, near-zero marginal cost.

---

## Phase 3 — Deepen the Intelligence
*Month 2+. Objective: Go from a dataset to a proper intelligence product.*

### 3.1 — Add Intelligence Layers Per Company

Once the base registry is solid, enrich each profile over time:

- **Funding signals** — job postings, team size changes, press mentions
- **Pricing changes** — if they sell data/services, track price shifts
- **Tech stack fingerprinting** — what models, frameworks, and MCP servers they use
- **Activity score** — a composite signal of how active/alive a company is
- **Product velocity** — GitHub commit frequency, changelog updates

### 3.2 — Sector Intelligence Packs

Bundle companies by category and sell as themed packs:

- *Agent Infrastructure* — facilitators, GPU providers, payment layers
- *Agent Data Marketplaces* — KnowMint, Compintel, and similar
- *Agent Security & Trust* — NexusWeb3, SATP, Mercury Trust, and similar

### 3.3 — Expand Data Sources

Once the x402 pipeline is proven, add:

- resolved.sh new listing feed
- `agent-card.json` crawl across known domains
- A2A ecosystem directory (Google's agent protocol)
- Other agent payment/identity registries as they emerge

---

## Phase 4 — The Backburner Lines
*Month 3+. Return to these once Phase 3 is generating consistent revenue.*

- **Agent Registry & Profiling** — broaden beyond x402, map the whole agent web
- **Threat Intelligence** — malicious agent detection, blocklist feed

---

## What You Can Do This Week

1. Pull all x402 ecosystem PRs (open + closed) via GitHub API
2. Enrich the first 50–100 company profiles manually or semi-automatically
3. Update the agentagent.sh listing description on resolved.sh
4. Register an EVM payout wallet
5. Upload the first dataset and set a price

The business can be open for transactions by end of week.

---

*Double Agent — "Agent watching agents."*
