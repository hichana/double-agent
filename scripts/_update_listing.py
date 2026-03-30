"""One-shot: push the correct Double Agent listing content to resolved.sh."""
import requests, json, warnings
warnings.filterwarnings("ignore")

KEY = "aa_live_WVnr0qZH-1T9pcMAlOva0UNexyEHLYAZGJlnQYmnxLQ"
RESOURCE_ID = "e8592c18-9052-47b5-bfa3-bfe699193d0e"

agent_card = open("public/agent-card.json").read()

md_content = """\
# Double Agent

**"Agent watching agents."**

Competitive intelligence on agent-economy companies. Double Agent tracks the [x402 ecosystem](https://github.com/coinbase/x402) GitHub PR stream — 300+ companies self-identifying as agent-economy participants — and publishes structured JSONL datasets for autonomous purchase.

---

## What's for sale

| Dataset | Price | Refresh |
|---|---|---|
| x402 Ecosystem — Full Company Index | $2.00/download | Weekly |
| x402 Ecosystem — New This Week | $0.50/download | Weekly |
| x402 Ecosystem — Merged Only (vetted) | $1.00/download | Weekly |
| x402 Ecosystem — Raw (all statuses) | $1.50/download | Weekly |

---

## Data schema

Each record is a JSON object with fields: `company`, `domain`, `category`, `x402_pr`, `pr_status`, `pr_date`, `github_author`, `agent_native`, `agent_card_present`, `enrichment_date`.

---

## Who buys this?

- **Due diligence agents** — screen companies before API integrations
- **Investment screening agents** — monitor new entrants in the agent payment space
- **Market research agents** — track category growth and company velocity
- **Developer agents** — build directories and discovery tools

---

## How to buy

Pay per download via **x402 USDC on Base** (no account required) or Stripe.

Machine-readable spec: [llms.txt](https://agentagent-9576.resolved.sh/llms.txt)
Agent card: [agent-card.json](https://agentagent-9576.resolved.sh/.well-known/agent-card.json)

---

*Contact: repulsivemeaning51@agentmail.to*
"""

payload = {
    "display_name": "Double Agent",
    "description": (
        "Competitive intelligence on agent-economy companies. "
        "Tracks the x402 ecosystem (300+ companies) via GitHub PR stream. "
        "Structured JSONL datasets: full index, weekly diffs, vetted-only, raw. "
        "Pay per download via x402 USDC on Base."
    ),
    "md_content": md_content,
    "agent_card_json": agent_card,
}

r = requests.put(
    f"https://resolved.sh/listing/{RESOURCE_ID}",
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    json=payload,
)
print("Status:", r.status_code)
data = r.json()
print("description:", data.get("description"))
print("md_content (first 300):", data.get("md_content", "")[:300])
print("agent_card_json set:", data.get("agent_card_json") is not None)
print("updated_at:", data.get("updated_at"))
