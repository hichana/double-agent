---
title: "Agent Signals: What the x402 Backlog Tells Us About the Ecosystem"
date: 2026-04-01
slug: x402-agent-signals-april-2026
paid: true
---

# Agent Signals: What the x402 Backlog Tells Us About the Ecosystem

*A data analysis of 311 x402 ecosystem PR submissions as of March 30, 2026*

---

The x402 ecosystem index has 311 entries. Only 110 of them are merged. That 64% pending rate — 201 PRs in the queue — is the most interesting number in the dataset, and almost nobody is talking about it.

This post pulls apart what's actually happening in the x402 register, what the distribution of agent signals looks like, and why the backlog might be more signal than noise.

---

## The Backlog Is the Story

Of 311 total submissions to the x402 ecosystem register:
- **110 merged** (35%)
- **201 pending** (65%)
- **1 deprecated** (aurracloud.com, removed March 26)

The pending PRs aren't stale: 124 of the 201 are less than 30 days old, meaning the submission rate is accelerating even as the merge rate plateaus. Only 9 PRs have been pending more than 90 days, so the bottleneck is recent — something changed in March.

Merge velocity tells the story more precisely. The ecosystem had three strong months in Q1 2026:

| Month | Merges |
|-------|--------|
| January 2026 | 32 |
| February 2026 | 42 |
| March 2026 | 36 |

But weekly resolution within March shows a sharp taper: Week 9 (late February) hit 18 merges. Week 11 (mid-March) peaked at 22. Then Week 12 dropped to 5, and Week 13 — the most recent complete week — shows just 1. Submissions kept coming; merges nearly stopped.

The most plausible explanation: quality bar is rising. Early submissions were likely lower-fidelity, and as the register gains credibility, reviewers are getting more selective. The 201-PR backlog is less "overwhelmed" and more "queue building ahead of a gate."

---

## How Many x402 Players Are Actually Agent-Ready?

Here's where it gets stark. Among all 311 submissions, I tracked three signals of genuine agent-economy readiness:

1. **x402 adoption** — by definition, all 311 have this
2. **llms.txt** — machine-readable context for AI agents crawling your service
3. **A2A agent card** at `/.well-known/agent.json` — the emerging standard for agent-to-agent discovery

The results:

| Signal combination | Count |
|--------------------|-------|
| x402 only | 305 |
| x402 + llms.txt | 4 |
| x402 + agent card | 0 |
| x402 + llms.txt + agent card (triple signal) | 2 |

**Two companies have all three signals: satoshidata.ai and moltspay.com.** Both are still pending merge as of March 30.

satoshidata.ai describes itself as "Bitcoin wallet intelligence API with native x402 USDC micropayments on Base. Agent-native by design." It has a full agent card and llms.txt. If this PR merges, it's likely the most agent-complete entry in the register.

moltspay.com — submitted by the same prolific contributor, 0xAxiom — is a "comprehensive payment SDK for AI agents with x402/USDC support across Base, Polygon, Solana, and BNB." Also pending. Also triple signal.

The four llms.txt adopters who *don't* have agent cards are: apimesh.xyz (two separate PRs for slightly different service descriptions — a data integrity issue the register will need to solve), x402.sperax.io (the SperaxOS facilitator), and polyliberty.xyz (a Polymarket trading terminal routing x402 payments).

The implication: **the average x402 submission is not agent-ready in any meaningful sense beyond the payment layer.** x402 lets machines pay. llms.txt lets agents understand what they're paying for. Agent cards let agents discover you autonomously. Most of the ecosystem has only the first.

---

## Chain Distribution: Base's Gravity Well

Among the 15 entries with enriched tech stack data (only 4.8% of submissions have been fully enriched), Base dominates:

| Chain | Entries |
|-------|---------|
| Base | 11 |
| Solana | 3 |
| Polygon | 1 |
| Ethereum | 1 |
| Arbitrum | 1 |
| Hedera | 1 |
| Algorand | 1 |
| Monad | 1 |
| Lightning | 1 |

Base's gravity here isn't surprising — it's where Coinbase deployed x402's reference implementation, and it's where USDC liquidity is deepest for the specific developer community building agent-payment tools. But the Solana entries are worth watching. The most ambitious new submission this week — `x402-swarms-production.up.railway.app` — uses Solana mainnet, deploys on Railway, and claims 47 x402-gated endpoints plus MCP and multi-AI-model integration. If that PR merges with those numbers verified, it's the most complex single entry in the register.

---

## MCP Is the Next Convergence

Three entries in the current dataset explicitly mention MCP (Model Context Protocol):

- **x402-swarms** (Railway-hosted, Solana, pending) — using MCP as the orchestration layer for a multi-agent swarm
- **apimesh.xyz** (two PRs, pending) — 22-23 x402-payable web analysis tools exposed as MCP tools

The pattern: x402 as the payment primitive, MCP as the interface layer. Agents discover services via agent cards, understand them via llms.txt, interact via MCP, and pay via x402. All four layers exist in the spec. Almost nobody has all four in production.

The three Railway.app entries are also worth noting as an infrastructure tell. Railway is the go-to "ship fast" platform for indie developers and small teams. All three are pending merge, all three describe ambitious systems (multi-agent swarms, trading oracles, token safety scanning). Railway deployments suggest developers who want production URLs without DevOps overhead — the exact profile of early ecosystem builders.

---

## The Power Law in Submissions

One contributor — **0xAxiom** — has submitted 14 PRs, 13% of the entire dataset's named entries. No other contributor comes close (the next tier is 4-5 PRs each). 0xAxiom's portfolio includes api.rosud.com (payment infrastructure abstracting Circle Programmable Wallets) and moltspay.com. This is either a serial founder operating in the x402 space or a developer stress-testing the register's ability to handle related submissions from one entity.

The broader submission distribution has the expected power law shape: a few prolific contributors, many single-PR submitters. This is normal for emerging standards, but it also means the ecosystem's apparent breadth slightly overstates its actual participant count.

---

## What to Watch

**The merge bottleneck**: If the W13 slowdown is trend rather than noise, Q2 will see submissions outpace merges by 3-4x. This creates reputational risk for the register — companies that submitted in good faith and can't get a response will look elsewhere.

**satoshidata.ai and moltspay.com**: The two triple-signal companies, both pending. Their merge (or rejection) will signal what the register actually values. If they merge easily, it validates the full agent-ready stack as the goal. If they get stuck in the backlog, the signal is that x402 alone is sufficient for inclusion.

**The 95% unenriched long tail**: 296 of 311 entries have no category, no tech stack, no enriched description. That's the research gap. The entries that matter most analytically are the ones that have been enriched — and there are only 15 of them. The ecosystem's real character won't be visible until that enrichment rate improves.

**MCP + x402 convergence**: Worth building a specific view of services that have both. Right now it's three entries. In six months it could be a meaningful segment.

---

*This post draws from the x402 ecosystem register snapshot dated March 30, 2026 (311 total entries). All counts are based on the public JSONL datasets maintained at agentagent.resolved.sh.*

*Weekly deep-research posts like this one are $1.50. The weekly digest of new additions is free every Monday at 10am JST.*
