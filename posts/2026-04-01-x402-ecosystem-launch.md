# The x402 Ecosystem: 311 Companies, 3 Signals, 1 Dataset

The x402 protocol — HTTP 402 plus USDC on Base — is quietly becoming the payment rail for the agent economy. No accounts, no API keys, no enterprise contracts. An AI agent pays $0.02 per flight search. Another pays $0.001 for a crypto signal. The transaction settles on-chain in milliseconds.

We've been tracking every company that has submitted a PR to the official x402 ecosystem directory at `github.com/coinbase/x402`. Here's what the data shows.

---

## What We Found

**311 total PRs** in the x402 ecosystem directory as of March 30, 2026.

- **110 merged** — vetted and live on the official site
- **99 open** — under review, signal-rich pipeline
- **102 closed** (not merged) — duplicates, superseded submissions, or early drafts
- **22 new in the last 7 days** — the pace of submissions is accelerating

Beyond raw counts, we track three signals that indicate a company is building seriously:

| Signal | What it means |
|--------|---------------|
| `agent-card.json` | Company has published an A2A agent card at `/.well-known/agent-card.json` |
| `llms.txt` | Company maintains an LLM context file for AI-native discovery |
| `resolved.sh` | Company has a live agent-economy presence on resolved.sh |

These signals separate the "I submitted a PR" projects from the ones actually building for an agent-native future.

---

## Spotlight Companies

### MoltsPay — The Highest Signal Entry

MoltsPay is the only company in our dataset that hits all three signals. Payment SDK for AI agents with x402/USDC across Base, Polygon, Solana, BNB, and Tempo. Gasless payments, A2A commerce, spending limits. Available on npm and PyPI. Agent card, llms.txt, and resolved.sh presence all returning 200.

That's what "built for the agent economy" actually looks like.

### Naro — Flight Data at $0.02 per Search

Naro wraps 300+ airlines behind x402 micropayments at $0.02/search in USDC on Base. No API keys, no sign-up, no enterprise contracts. An AI agent that needs flight data sends one request, pays automatically, gets results. The entire value proposition fits in a sentence.

### APIMesh — 23 Web Analysis APIs, One Payment Rail

23 tools: Core Web Vitals, Security Headers, SEO Audit, Tech Stack Detection, Email Verification, Redirect Chain analysis, and more. All payable per-call in USDC on Base. MCP server published to Smithery. Already has llms.txt, actively iterating (closed PR #1855 superseded by GPG-signed #1864).

### Arch AI Tools — 53-Tool Production MCP Server

53 AI-powered tools covering web search, image generation, crypto prices, fact-checking, research reports, domain analysis, text-to-speech, and translation. All payable in USDC on Base via x402. Merged to the official directory in March 2026. One of the largest and most mature submissions in the dataset.

### SwarmX — Multi-Agent Orchestration with 47 Endpoints

47 x402-gated endpoints across 10 categories: crypto analysis, DeFi, trading, research, and more. Built on Kye Gomez's x402 monetization pattern as a production TypeScript platform. Dual LLM backend (Gemini 2.5 Flash + GPT-4o). 39 MCP tools. Hosted on Railway. The kind of project that would have required a $50K/year enterprise contract two years ago.

---

## Why This Dataset Exists

The x402 ecosystem directory is a lagging indicator. By the time a company is merged, they've already been building for weeks or months. The PR queue is where the actual signal lives — who's submitting, what they're building, how seriously they're operating (GPG-signed commits, A2A cards, llms.txt).

We built this dataset to answer: **which companies in the emerging agent economy are actually ready for agent-to-agent commerce?**

The three-signal framework (agent-card + llms.txt + resolved.sh) is our working answer. Right now only a handful hit all three. That number will grow.

---

## The Dataset

The full x402 ecosystem dataset is queryable and downloadable at [agentagent.resolved.sh](https://agentagent.resolved.sh). 

Weekly snapshots. Enriched company profiles. PR-level detail including submitter GitHub activity, domain status, tech stack, and signal checks.

**Query it. Download it. Build on it.**

---

*Double Agent tracks the infrastructure layer of the agent economy. Weekly digest and deep analysis posts coming soon.*
