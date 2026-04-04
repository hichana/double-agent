#!/usr/bin/env node
/**
 * register_payout_wallet.js
 *
 * Derives the EVM address from WALLET_PRIVATE_KEY, checks whether a payout
 * address is already registered on resolved.sh, and registers it if not.
 *
 * Usage (Node 20+):
 *   node --env-file=.env scripts/register_payout_wallet.js
 *
 * Or with dotenv installed:
 *   node -r dotenv/config scripts/register_payout_wallet.js
 */

import { privateKeyToAccount } from "viem/accounts";
import { readFileSync } from "fs";
import { resolve } from "path";

// ── Load .env manually if not pre-loaded ─────────────────────────────────────
// Node 20+ supports --env-file; this fallback handles running without it.
function loadEnv() {
  const envPath = resolve(process.cwd(), ".env");
  try {
    const lines = readFileSync(envPath, "utf8").split("\n");
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith("#")) continue;
      const eq = trimmed.indexOf("=");
      if (eq === -1) continue;
      const key = trimmed.slice(0, eq).trim();
      const val = trimmed.slice(eq + 1).trim();
      if (!process.env[key]) process.env[key] = val;
    }
  } catch {
    // .env not found — rely on environment variables already set
  }
}

loadEnv();

// ── Validate env vars ─────────────────────────────────────────────────────────
const rawKey = process.env.WALLET_PRIVATE_KEY;
const apiKey = process.env.RESOLVED_SH_API_KEY;

if (!rawKey) {
  console.error("❌  WALLET_PRIVATE_KEY not set in .env");
  process.exit(1);
}
if (!apiKey) {
  console.error("❌  RESOLVED_SH_API_KEY not set in .env");
  process.exit(1);
}

// ── Derive EVM address ────────────────────────────────────────────────────────
const privateKey = rawKey.startsWith("0x") ? rawKey : `0x${rawKey}`;
const account = privateKeyToAccount(privateKey);
const walletAddress = account.address;

console.log(`\n🔑  Derived wallet address: ${walletAddress}`);

// ── resolved.sh helpers ───────────────────────────────────────────────────────
const BASE = "https://resolved.sh";
const authHeaders = {
  Authorization: `Bearer ${apiKey}`,
  "Content-Type": "application/json",
};

async function getAccountStatus() {
  const res = await fetch(`${BASE}/account`, { headers: authHeaders });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`GET /account failed ${res.status}: ${body}`);
  }
  return res.json();
}

async function registerPayoutAddress(address) {
  const res = await fetch(`${BASE}/account/payout-address`, {
    method: "POST",
    headers: authHeaders,
    body: JSON.stringify({ payout_address: address }),
  });
  const body = await res.text();
  let parsed;
  try { parsed = JSON.parse(body); } catch { parsed = body; }
  if (!res.ok) {
    throw new Error(`POST /account/payout-address failed ${res.status}: ${body}`);
  }
  return parsed;
}

// ── Main ──────────────────────────────────────────────────────────────────────
(async () => {
  console.log("📡  Fetching account status from resolved.sh…\n");

  let account;
  try {
    account = await getAccountStatus();
  } catch (err) {
    console.error(`❌  ${err.message}`);
    process.exit(1);
  }

  console.log("Account status:", JSON.stringify(account, null, 2));

  const existing = account?.payout_address ?? account?.payoutAddress ?? null;

  if (existing) {
    console.log(`\n✅  Payout address already registered: ${existing}`);
    if (existing.toLowerCase() === walletAddress.toLowerCase()) {
      console.log("    Matches derived wallet — nothing to do.");
    } else {
      console.log(`⚠️   Registered address differs from derived wallet (${walletAddress}). Updating…`);
      try {
        const result = await registerPayoutAddress(walletAddress);
        console.log("\n✅  Updated payout address:", JSON.stringify(result, null, 2));
      } catch (err) {
        console.error(`❌  ${err.message}`);
        process.exit(1);
      }
    }
  } else {
    console.log(`\n⚙️   No payout address registered. Registering ${walletAddress}…`);
    try {
      const result = await registerPayoutAddress(walletAddress);
      console.log("\n✅  Registered:", JSON.stringify(result, null, 2));
    } catch (err) {
      console.error(`❌  ${err.message}`);
      process.exit(1);
    }
  }
})();
