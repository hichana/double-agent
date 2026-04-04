/**
 * buy_well_knowns_delta.js
 * Purchases the Daily Delta Feed from well-knowns.resolved.sh via x402 micropayment.
 * Uses PAYMENT-SIGNATURE header (resolved.sh x402 V2) with EIP-712 USDC authorization.
 */
import { createWalletClient, http, toHex, getAddress } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { base } from 'viem/chains';
import { writeFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const BASE_URL = 'https://well-knowns.resolved.sh';

// ─── Wallet setup ────────────────────────────────────────────────────────────
const account = privateKeyToAccount(`0x${process.env.WALLET_PRIVATE_KEY}`);
const walletClient = createWalletClient({ account, chain: base, transport: http() });
console.log('Wallet:', account.address);

// ─── Date candidates: today (JST) then fallback ──────────────────────────────
// Sandbox runs UTC; Matt is JST (UTC+9), add 9 hours to find today's date
const nowJST = new Date(Date.now() + 9 * 60 * 60 * 1000);
const today = nowJST.toISOString().slice(0, 10);
const candidates = [today, '2026-03-24'];

// ─── Build EIP-712 PAYMENT-SIGNATURE payload ─────────────────────────────────
async function buildPaymentHeader(spec, version) {
  const raw = spec.accepts[0];

  const nonce       = toHex(crypto.getRandomValues(new Uint8Array(32)));
  const validAfter  = '0';
  const validBefore = String(Math.floor(Date.now() / 1000) + raw.maxTimeoutSeconds);

  // Sign TransferWithAuthorization
  const signature = await walletClient.signTypedData({
    domain: {
      name:              raw.extra?.name    ?? 'USD Coin',
      version:           raw.extra?.version ?? '2',
      chainId:           8453,
      verifyingContract: getAddress(raw.asset),
    },
    types: {
      TransferWithAuthorization: [
        { name: 'from',        type: 'address' },
        { name: 'to',          type: 'address' },
        { name: 'value',       type: 'uint256' },
        { name: 'validAfter',  type: 'uint256' },
        { name: 'validBefore', type: 'uint256' },
        { name: 'nonce',       type: 'bytes32' },
      ],
    },
    primaryType: 'TransferWithAuthorization',
    message: {
      from:        getAddress(account.address),
      to:          getAddress(raw.payTo),
      value:       BigInt(raw.amount),
      validAfter:  BigInt(validAfter),
      validBefore: BigInt(validBefore),
      nonce,
    },
  });

  // V2 payload structure per resolved.sh docs
  const paymentPayload = {
    x402Version: version,
    payload: {
      authorization: {
        from:        account.address,
        to:          raw.payTo,
        value:       raw.amount,
        validAfter,
        validBefore,
        nonce,
      },
      signature,
    },
    // CDP facilitator verify() uses maxAmountRequired; resolved.sh sends amount — map it
    accepted: { ...raw, maxAmountRequired: raw.amount },
  };

  return Buffer.from(JSON.stringify(paymentPayload)).toString('base64');
}

// ─── Attempt purchase for a given date ───────────────────────────────────────
async function attemptPurchase(date) {
  const url = `${BASE_URL}/data/delta-${date}.jsonl`;
  console.log(`\nTrying: ${url}`);

  const r1 = await fetch(url);
  console.log('Status:', r1.status);

  if (r1.status === 200) {
    console.log('Available without payment — downloading.');
    return { data: await r1.text(), date, paid: null };
  }
  if (r1.status === 404) {
    console.log('Not found.');
    return null;
  }
  if (r1.status !== 402) {
    throw new Error(`Unexpected ${r1.status}: ${await r1.text()}`);
  }

  // Decode 402 spec (body JSON or base64 header)
  let spec;
  const ct = r1.headers.get('content-type') ?? '';
  if (ct.includes('application/json') || ct.includes('text/')) {
    const text = await r1.text();
    try { spec = JSON.parse(text); }
    catch { throw new Error(`Non-JSON 402 body: ${text}`); }
  } else {
    const hdr = r1.headers.get('payment-required') ?? r1.headers.get('x-payment-required');
    if (!hdr) throw new Error('No payment spec in 402 response');
    spec = JSON.parse(Buffer.from(hdr, 'base64').toString('utf8'));
  }

  console.log('\nPayment spec:', JSON.stringify(spec, null, 2));
  const raw = spec.accepts[0];
  const amountUsdc = (Number(raw.amount) / 1e6).toFixed(4);
  console.log(`\nPaying $${amountUsdc} USDC → ${raw.payTo} on ${raw.network}`);

  const payment = await buildPaymentHeader(spec, spec.x402Version ?? 2);

  const r2 = await fetch(url, {
    headers: {
      'PAYMENT-SIGNATURE': payment,
      'Access-Control-Expose-Headers': 'X-PAYMENT-RESPONSE',
    },
  });

  console.log('Paid status:', r2.status);

  // Log payment response if present
  const xpr = r2.headers.get('X-PAYMENT-RESPONSE');
  if (xpr) {
    try { console.log('Payment response:', JSON.stringify(JSON.parse(Buffer.from(xpr, 'base64').toString()), null, 2)); }
    catch { console.log('X-PAYMENT-RESPONSE:', xpr); }
  }

  if (r2.status !== 200) {
    const body = await r2.text();
    throw new Error(`Payment rejected (${r2.status}): ${body}`);
  }

  return { data: await r2.text(), date, paid: raw.amount };
}

// ─── Main ─────────────────────────────────────────────────────────────────────
let result = null;
for (const date of candidates) {
  result = await attemptPurchase(date);
  if (result) break;
}

if (!result) {
  console.error('No delta file found for any candidate date:', candidates);
  process.exit(1);
}

// ─── Save ─────────────────────────────────────────────────────────────────────
const publicDir = join(__dirname, '..', 'public');
mkdirSync(publicDir, { recursive: true });
const outFile = join(publicDir, `well-knowns-delta-${result.date}.jsonl`);
writeFileSync(outFile, result.data, 'utf8');

console.log(`\n✓ Saved → ${outFile}`);
if (result.paid) {
  const usdc = (Number(result.paid) / 1e6).toFixed(6);
  console.log(`✓ Paid: $${usdc} USDC (${result.paid} units)`);
}

// ─── Preview ─────────────────────────────────────────────────────────────────
const lines = result.data.split('\n').filter(l => l.trim());
console.log(`\n--- First ${Math.min(5, lines.length)} lines of ${lines.length} total ---`);
lines.slice(0, 5).forEach(l => console.log(l));
