# Double Agent — Deep Research Report
**Date:** 2026-03-25
**Purpose:** Inform and stress-test the initial project plan before execution begins.

---

## 1. resolved.sh — Platform Mechanics (The Storefront)

### What it is
resolved.sh is an agent-native registration and data marketplace platform. For $12/year, you get a subdomain (`slug.resolved.sh`), a machine-readable identity layer (agent-card.json, llms.txt, robots.txt), and optional custom domain support. It is explicitly designed for autonomous agents to register and operate without human intermediaries.

### How the data marketplace works
- Operators upload datasets (JSON, CSV, JSONL; max 10MB each, up to **5 files per resource**)
- Each file gets an individual price set by the operator
- Buyers pay via **x402 (USDC on Base)** or **Stripe**
- Access tokens are valid for **1 hour** after purchase
- Economics: **operator earns 90%, platform takes 10%**
- Payouts sweep daily to a registered EVM wallet when balance hits **$5.00 USDC**

### Key API routes
- `PUT /listing/{id}/data/{filename}` — upload/update a marketplace file
- `GET /{subdomain}/llms.txt` — machine-readable product listing (agents discover what's for sale here)
- `GET /.well-known/agent-card.json` — A2A conformant agent card

### Critical constraints to know
- **5 file cap per resource** — This limits how many distinct dataset SKUs we can sell from a single listing. If we want to sell more than 5 distinct datasets, we'd need multiple listings or a different delivery mechanism.
- **10MB per file** — Fine for JSONL snapshots of a few hundred companies, but we'll need to think about compression or chunking as the dataset scales.
- **1-hour access tokens** — Buyers get a download link valid for 1 hour. This is fine for snapshot data; less elegant for a streaming feed use case.

### Authentication for the agent
- API Key (`aa_live_...`) works fine for the automation pipeline
- ES256 JWT signing is available for fully autonomous key rotation (more complex, worth implementing in Phase 2 for zero-human operations)

---

## 2. The agentagent.sh Listing — Current State

The current listing is a near-empty placeholder:
- Display name: "agentagent"
- Description: "An agent that agents agentically."
- No products listed, no datasets, no pricing
- No llms.txt content beyond the default resolved.sh boilerplate
- No agent-card.json configured

**The storefront is live but completely empty.** This is actually fine — it means there's no cleanup needed, we're starting fresh. But it also means there's zero discoverability right now. Fleshing this out is genuinely the highest-leverage immediate action.

---

## 3. x402 Protocol — Current Status & Ecosystem Size

### x402 is the clear winner in its category
- Launched May 2025 by Coinbase; V2 shipped December 2025 with sessions, multi-chain support, and auto service discovery
- **x402 Foundation** co-founded by Coinbase and Cloudflare; Google and Visa have since joined
- Stripe integrated x402 for USDC payments on Base in **February 2026**
- **200-300 companies** are in the ecosystem (x402.org/ecosystem)
- The GitHub repo has **302 ecosystem-labeled PRs** (88 open, 214 closed) as of our research date

### Competing protocols (important context)
The agent payment space has splintered into four overlapping standards:
- **x402** (Coinbase + Cloudflare + Google + Visa) — settlement layer, crypto-native, most production traction
- **AP2** (Google, 60+ partners) — authorization/trust layer, supports x402 as an extension
- **ACP** (OpenAI/Stripe) — e-commerce checkout flow; OpenAI pivoted away from it in March 2026
- **MPP** (Stripe + Tempo, launched March 18, 2026) — streaming micropayments, fiat + crypto, sessions model

**These are largely complementary, not competitive.** x402 is the settlement layer; the others handle authorization, checkout, and session management. Double Agent should track *all of them* as data sources, not just x402.

### x402 as a data source: scale assessment
302 ecosystem PRs is a solid starting dataset, but it's not enormous. The real insight is that **this list is growing fast and is highly self-selected** — every company in it is explicitly agent-economy native and actively self-identifying. That makes it qualitatively richer than any scraped or inferred list.

The PR stream also captures **intent and trajectory**: a draft PR signals an earlier stage than a merged PR. Companies that submitted and got rejected are still real signals. This temporal dimension is genuinely valuable.

---

## 4. Competitive Landscape — Who Else Is Doing This?

### Direct competitors: effectively none (yet)
No company is currently running a dedicated competitive intelligence / registry tracking service specifically for the agent economy in the way Double Agent proposes. The closest things that exist:

- **x402Scan** and **x402station** — on-chain analytics for x402 transactions, not company intelligence
- **The Agentic List 2026** (agentconference.com) — annual curated list of 120 top agentic AI companies, manually compiled, enterprise-focused, not agent-purchasable
- **CB Insights, Messari, etc.** — broad market maps, not agent-economy specific, not agent-purchasable, expensive subscription models
- **StartUs Insights** — tracks 9M+ startups broadly, no specific agent-economy focus, human-oriented

**The gap Double Agent fills is real:** there is no continuously-updated, machine-purchasable, agent-native intelligence feed specifically tracking who is building in the agent economy. The closest analogs are broad startup trackers aimed at human analysts, not agents.

### Adjacent data providers in the x402 ecosystem
Several companies are already selling data via x402 — these are potential customers *and* things we should be tracking:
- **Messari** — crypto intelligence, gated via x402
- **Nansen** — on-chain analytics, gated via x402
- **Gloria AI** — real-time news data for agents
- **Moltalyzer** — community digests, GitHub trending repos
- **SLAMai** — smart money intelligence
- **KnowMint** — human knowledge marketplace for agents

None of these track the agent economy itself. There's no one watching the watchers.

---

## 5. Broader Agent Economy Context

- Market size: ~$9.9B in 2026, projected $57B by 2031 (CAGR ~42%)
- 35% of organizations already have broad AI agent deployment; another 27% are experimenting
- The "Tier 3 agent-native startup" category (companies building with agents as the primary interface) is explicitly being identified as the emerging wave
- **The x402 Foundation now includes Google and Visa** — x402 is not a niche crypto experiment, it's becoming infrastructure

This context matters for Double Agent's positioning: the *buyers* of this data are overwhelmingly going to be other agents — AI research agents, due diligence agents, investment screening agents. The product should be optimized for machine consumption first, human consumption second. The plan already reflects this instinct (JSONL format, resolved.sh distribution, llms.txt discoverability), which is correct.

---

## 6. Plan Validation & Gaps Found

### What the plan gets right
- x402 ecosystem PRs are genuinely the best single signal source for early-stage agent companies; the plan correctly prioritizes this
- resolved.sh is the right distribution channel — it's the only agent-native data marketplace with x402 payment support that currently exists
- JSONL format is correct for machine consumption
- The phased approach (seed data → storefront → automation → enrichment) is sensible

### Gaps and issues to address

**G1: The 5-file cap on resolved.sh**
The plan describes 4 distinct dataset SKUs (Full Index, New This Week, Merged Only, Raw). That's fine — within the cap. But any future expansion hits a wall. We may need to think about how to bundle or whether to run multiple resolved.sh listings (e.g., one per sector pack).

**G2: Multiple payment protocol sources, not just x402**
The plan exclusively sources from x402 PRs. But AP2 (Google, 60+ partners), MPP (Stripe, March 2026), and ACP all have their own ecosystem companies that may not overlap with x402. Tracking only x402 misses a growing portion of the agent economy. This should be noted as a near-term Phase 3 expansion, not an afterthought.

**G3: The listing description is embarrassingly thin right now**
"An agent that agents agentically." needs to be replaced immediately. Agents discovering this via llms.txt need to understand in machine-readable terms: what data is available, what format, what cadence, what it costs, and why it's valuable. This is genuinely the highest-ROI action before any code is written.

**G4: The x402.org ecosystem page is a parallel source**
The official x402 website already maintains a curated ecosystem list with ~250-300 companies. This is separate from the GitHub PR stream and likely has different/additional companies. It should be scraped as an additional data source.

**G5: No mention of the awesome-x402 curated list**
GitHub has `Merit-Systems/awesome-x402` and `xpaysh/awesome-x402` — community-maintained lists of x402 ecosystem participants. These are additional signal sources that don't require API access to harvest.

**G6: Pricing may be too low**
At $2 for the full index, we're pricing like a commodity. The agents *buying* this data are doing due diligence, investment research, or building their own products on top of it. The value created by one good company lead likely exceeds the $2 purchase price by orders of magnitude. Worth testing higher prices once the dataset has demonstrated value — $5-$25 range for the full index is defensible once enrichment is solid.

**G7: No mention of the x402 V2 session token feature**
x402 V2 supports session tokens — a client makes one payment to authorize multiple future requests. For a high-frequency feed use case (an agent that checks for new entrants daily), this is a better UX than paying $0.50 per check. We should explore offering a "subscription session" model once the automation is running.

**G8: resolved.sh has a 10MB file size limit**
For now this is fine, but a fully enriched dataset of 500+ companies with rich profiles could approach this limit. We should track dataset size from the start and think about archiving older data.

---

## 7. Recommended Plan Adaptations

### Immediate (this week)
1. **Fix the listing description** — Write a proper llms.txt and agent-card.json for agentagent.sh before publishing any data. The description should be machine-optimized: structured fields describing data format, pricing, refresh cadence, and what signals each dataset captures.
2. **Add x402.org/ecosystem as a secondary scrape target** — 250+ companies already curated, no API required.
3. **Track AP2 and MPP ecosystems in the roadmap** — Add them explicitly to Phase 3.3's "Expand Data Sources" section.

### Short-term (Phase 1-2)
4. **Consider pricing tiers more carefully** — Start low to get first purchases, but plan a pricing experiment once 10+ purchases have occurred.
5. **Implement x402 V2 session tokens** for repeat-buyer agents once daily diff is running.
6. **Think about the 5-file cap** — Either limit to 4 SKUs permanently, or explore running a second resolved.sh listing for sector packs.

### Medium-term (Phase 3)
7. **Build a cross-protocol company graph** — A company that appears in the x402 PR list AND the AP2 ecosystem AND has an agent-card.json AND is on resolved.sh is a high-confidence, multi-signal entity. This cross-referencing is where Double Agent's data becomes genuinely defensible.
8. **Consider whether the data should also be queryable, not just downloadable** — An API where agents can POST a company name and GET back its intelligence profile would unlock higher-value use cases than flat file downloads.

---

## Sources

- [resolved.sh](https://resolved.sh)
- [agentagent.sh](https://agentagent.sh)
- [x402 GitHub repo](https://github.com/coinbase/x402)
- [x402 Ecosystem](https://www.x402.org/ecosystem)
- [x402 Foundation announcement — Coinbase](https://www.coinbase.com/blog/coinbase-and-cloudflare-will-launch-x402-foundation)
- [x402 Foundation announcement — Cloudflare](https://blog.cloudflare.com/x402/)
- [Agentic payments protocols compared — Crossmint](https://www.crossmint.com/learn/agentic-payments-protocols-compared)
- [awesome-x402 — Merit Systems](https://github.com/Merit-Systems/awesome-x402)
- [KnowMint on Glama](https://glama.ai/mcp/servers/Sou0327/knowmint)
- [The Agentic List 2026](https://www.agentconference.com/agenticlist/2026)
- [AI Agent market stats — Master of Code](https://masterofcode.com/blog/ai-agent-statistics)
- [MPP — WorkOS](https://workos.com/blog/x402-vs-stripe-mpp-how-to-choose-payment-infrastructure-for-ai-agents-and-mcp-tools-in-2026)
- [x402 and AP2 comparison — Medium](https://medium.com/@gwrx2005/ai-agents-and-autonomous-payments-a-comparative-study-of-x402-and-ap2-protocols-e71b572d9838)
