# x402 Ecosystem Daily Diff — 2026-03-27

## Run Summary

- **Date:** 2026-03-27
- **Total PRs fetched:** 309 (across 4 API pages)
- **PR range:** #554 – #1838
- **Cutoff for "new" entries:** 2026-03-25 (last ~48 hours)
- **New entries found:** 8 PRs (7 new additions + 1 deprecation)
- **Snapshot saved:** `x402_ecosystem_snapshot_2026-03-27.json`
- **Enriched JSONL:** `x402_daily_diff_2026-03-27.jsonl`

> ⚠️ **Note:** The project directory `~/Documents/double-agent` was not accessible from this run environment (no folder mounted). A full diff against the `research/` snapshot could not be performed. The cutoff of 2026-03-25 was used as a proxy for "since last run." The snapshot and enriched JSONL have been saved to the outputs folder for manual merge into the project repo.

---

## New Entries (2026-03-25 to 2026-03-26)

### ✅ High Signal

| # | PR | Name | Domain | Agent Card | llms.txt | resolved.sh |
|---|-----|------|--------|-----------|---------|------------|
| 1 | [#1838](https://github.com/coinbase/x402/pull/1838) | **Sperax / SperaxOS** | x402.sperax.io / chat.sperax.io | ❌ | ✅ | ❌ |
| 2 | [#1824](https://github.com/coinbase/x402/pull/1824) | **satoshidata.ai** | satoshidata.ai | ✅ | ✅ | ❌ |
| 3 | [#1801](https://github.com/coinbase/x402/pull/1801) | **MoltsPay** | moltspay.com | ✅ | ✅ | ✅ |

**MoltsPay** is the standout: all three well-known files present, multi-chain (Base/Polygon/Solana/BNB/Tempo), npm + PyPI packages, submitted by prolific ecosystem contributor `@0xAxiom`.

**satoshidata.ai** also has agent-card.json + llms.txt, supports both x402 and L402 (Lightning), strong integration posture.

---

### 📋 New Entries Detail

#### #1838 — Sperax Facilitator + SperaxOS
- **Submitter:** @nirholas (78 public repos)
- **Domains:** `x402.sperax.io` (facilitator) + `chat.sperax.io` (DeFi workspace)
- **Category:** Facilitator + Services/Endpoints
- **Networks:** Base, Base Sepolia, Arbitrum, Ethereum
- **Token:** USDC + USDs (Sperax stablecoin)
- **Protocols:** EIP-3009, EIP-2612
- **Well-known:** llms.txt ✅ at chat.sperax.io
- **Notes:** First facilitator adding native USDs stablecoin support alongside USDC.

#### #1829 — AgentBridge
- **Submitter:** @tianzizhiming-svg (3 repos; bio: "Building the Chinese web data layer for AI Agents")
- **Domain:** `api.060504.shop`
- **Category:** Services/Endpoints
- **Price:** $0.003/request
- **Description:** Fetches Chinese web content (Xiaohongshu, Zhihu) as clean markdown, USDC on Base
- **Well-known:** All 404
- **Notes:** Non-branded domain. Only 3 GitHub repos. Listed on 402index.io. Low integration signal.

#### #1828 — PolyLiberty
- **Submitter:** @miinimes1 (1 repo)
- **Domain:** `polyliberty.xyz`
- **Category:** Services/Endpoints
- **Description:** Polymarket trading terminal, 6 machine-payable API endpoints. Accepts USDC, WETH, USDT via PayAI facilitator.
- **Well-known:** llms.txt ✅
- **Notes:** PR includes full discovery endpoint + llms.txt. Treasury: `0x11FD3946B5040c48e707bC6185B56CF40B61E108`. Submitter has only 1 repo.

#### #1824 — satoshidata.ai
- **Submitter:** @wrbtc (5 repos)
- **Domain:** `satoshidata.ai`
- **Category:** Services/Endpoints
- **Price:** $0.01 USDC per endpoint
- **Endpoints:** `/v1/wallets/{address}/summary`, `/v1/wallets/{address}/detail`, `/v1/tx/verify`
- **Well-known:** agent-card.json ✅, llms.txt ✅
- **Notes:** Also supports L402 (Lightning). Self-hosted facilitator. Strong agent-native posture.

#### #1822 — UtilShed
- **Submitter:** @KarlbottAgent (11 repos)
- **Domain:** `utilshed.com`
- **Category:** Services/Endpoints
- **APIs:** SEO Audit ($0.05), Screenshot ($0.02), Health Check ($0.10)
- **Facilitator:** CDP production
- **Well-known:** All 404
- **Notes:** Website markets free developer tools; x402 layer is a monetized premium tier. Registered on x402scan.com. No well-known files.

#### #1820 — TokenSafe
- **Submitter:** @ampactor (0 public repos)
- **Domain:** `tokensafe-production.up.railway.app`
- **Category:** Services/Endpoints
- **Price:** $0.008 USDC
- **Description:** Solana token safety scanner, risk score 0–100. Analyzes mint authority, holder concentration, honeypot risk.
- **Well-known:** All 404
- **Notes:** Resubmission of #1386. No custom domain (Railway deployment URL). Submitter has no public repos. Low integration signal.

#### #1816 — Deprecation: aurracloud.com
- **Submitter:** @ya7ya (@monemetrics, 60 repos)
- **Type:** REMOVAL — removing aurracloud facilitator from ecosystem
- **Status:** Closed
- **Notes:** Not a new entry. Marks aurracloud.com as deprecated/removed.

#### #1801 — MoltsPay (Closed/Merged)
- **Submitter:** @0xAxiom (25 repos, prolific ecosystem contributor)
- **Domain:** `moltspay.com`
- **Category:** Client-Side Integrations
- **Description:** Payment SDK for AI agents, multi-chain x402/USDC (Base, Polygon, Solana, BNB, Tempo)
- **Well-known:** agent-card.json ✅, resolved.sh ✅, llms.txt ✅
- **npm:** `moltspay` | **PyPI:** `moltspay`
- **GitHub:** github.com/Yaqing2023/moltspay
- **Notes:** Best integration signal of this batch. Full well-known trinity. Already closed (merged or rejected).

---

## 7-Day New Entries Overview (2026-03-20 to 2026-03-26)

35 total PRs in the last 7 days. Selected highlights beyond today's batch:

| PR | Name | State | Submitter | Notable |
|----|------|-------|-----------|---------|
| #1780 | Ultravioleta DAO facilitator | open | @0xultravioleta | DAO-governed facilitator |
| #1771 | Pyrimid + MYA | open | @pyrimid | Two entries in one PR |
| #1765 | CardZero | open | @mrocker | AI agent payment wallet with x402 buyer support |
| #1750 | Fronesis Labs | open | @DariRinch | Verifiable AI audit service |
| #1745 | resolved.sh | open | @hichana | The resolved.sh project itself submitting to ecosystem |
| #1739 | Satoshi API | open | @Bortlesboat | Bitcoin data micropayments |
| #1726 | Flow EVM x402 Facilitator | closed | @lmcmz | Flow blockchain integration |
| #1719 | WalletIQ | open | @iJaack | Wallet intelligence API |
| #1730 | x402-cfo | closed | @Upn-130guthub | Agent spend control plane |

---

## Action Items for Next Run

1. **Merge snapshot** — copy `x402_ecosystem_snapshot_2026-03-27.json` to `~/Documents/double-agent/research/` to establish baseline for future diffs
2. **Merge JSONL** — append `x402_daily_diff_2026-03-27.jsonl` to the master dataset
3. **Review resolved.sh PR #1745** — submitted by `@hichana` (the project owner); confirmed PR is open
4. **MoltsPay** — already closed; check if merged into x402 main branch
5. **Flow EVM Facilitator** (#1726) — closed PR; check if merged; significant ecosystem expansion for Flow blockchain users

---

## Files Produced This Run

| File | Description |
|------|-------------|
| `x402_ecosystem_snapshot_2026-03-27.json` | Full snapshot of all 309 ecosystem PRs from GitHub API |
| `x402_daily_diff_2026-03-27.jsonl` | Enriched JSONL records for 8 newest PRs (2026-03-25/26) |
| `x402_daily_diff_report_2026-03-27.md` | This report |

_Could not complete: git commit to `~/Documents/double-agent` (project directory not accessible from run environment)._
