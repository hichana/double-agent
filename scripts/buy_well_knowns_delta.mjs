import { readFileSync, writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { toHex } from 'viem';
import { createSigner } from 'x402/types';

// Load .env manually
const envPath = join(dirname(fileURLToPath(import.meta.url)), '../.env');
const env = Object.fromEntries(
  readFileSync(envPath, 'utf8')
    .split('\n')
    .filter(l => l.includes('=') && !l.startsWith('#'))
    .map(l => { const i = l.indexOf('='); return [l.slice(0, i).trim(), l.slice(i + 1).trim()]; })
);

const PRIVATE_KEY = env.WALLET_PRIVATE_KEY.startsWith('0x')
  ? env.WALLET_PRIVATE_KEY
  : `0x${env.WALLET_PRIVATE_KEY}`;

// createSigner returns a Promise for the multi-network export
const walletClient = await createSigner('base', PRIVATE_KEY);
const fromAddress = walletClient.account.address;
console.log('Wallet:', fromAddress);

const RESOURCE_URL = 'https://well-knowns.resolved.sh/data/delta-2026-03-24.jsonl';

// ── Step 1: initial probe to get the 402 payment requirements ──────────────
console.log('Requesting:', RESOURCE_URL);
const res402 = await fetch(RESOURCE_URL);
console.log('Initial response status:', res402.status);

if (res402.status !== 402) {
  const body = await res402.text();
  console.log('Unexpected status, body:', body);
  process.exit(res402.ok ? 0 : 1);
}

const data = await res402.json();
const req = data.accepts[0]; // { scheme, network, asset, amount, payTo, maxTimeoutSeconds, extra }
console.log('Payment required:', JSON.stringify(req, null, 2));

// ── Step 2: build EIP-712 authorization fields ─────────────────────────────
const nonce = toHex(crypto.getRandomValues(new Uint8Array(32)));
const validAfter = BigInt(Math.floor(Date.now() / 1000) - 60);    // 1 min ago
const validBefore = BigInt(Math.floor(Date.now() / 1000) + req.maxTimeoutSeconds);

// Parse chainId from network string "eip155:8453" → 8453
const chainId = parseInt(req.network.split(':')[1], 10);

// ── Step 3: sign via the library's wallet client (viem signTypedData) ───────
const signature = await walletClient.signTypedData({
  domain: {
    name:              req.extra?.name ?? 'USD Coin',
    version:           req.extra?.version ?? '2',
    chainId,
    verifyingContract: req.asset,
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
    from:        fromAddress,
    to:          req.payTo,
    value:       BigInt(req.amount),
    validAfter,
    validBefore,
    nonce,
  },
});

console.log('Signed EIP-3009 authorization');

// ── Step 4: build resolved.sh x402 v2 envelope ────────────────────────────
// Format documented at https://resolved.sh/llms.txt :
//   { x402Version, payload: { authorization, signature }, accepted: <accepts[0]> }
const paymentPayload = {
  x402Version: data.x402Version,
  payload: {
    authorization: {
      from:        fromAddress,
      to:          req.payTo,
      value:       req.amount,                  // string "10000"
      validAfter:  validAfter.toString(),
      validBefore: validBefore.toString(),
      nonce,
    },
    signature,
  },
  // CDP facilitator expects maxAmountRequired; resolved.sh sends "amount" — bridge them
  accepted: { ...req, maxAmountRequired: req.amount },
};

const paymentHeader = Buffer.from(JSON.stringify(paymentPayload)).toString('base64');
console.log('Payment payload (decoded):', JSON.stringify(paymentPayload, null, 2));

// ── Step 5: retry with PAYMENT-SIGNATURE header ────────────────────────────
console.log('Sending payment...');
const res = await fetch(RESOURCE_URL, {
  headers: {
    'PAYMENT-SIGNATURE': paymentHeader,
    'Access-Control-Expose-Headers': 'X-PAYMENT-RESPONSE',
  },
});

console.log('Response status:', res.status);

if (res.ok) {
  const text = await res.text();
  const lines = text.trim().split('\n');
  console.log(`\nSuccess! Downloaded ${lines.length} records.`);
  console.log('\nFirst 3 records:');
  lines.slice(0, 3).forEach(l => {
    try { console.log(JSON.stringify(JSON.parse(l), null, 2)); } catch { console.log(l); }
  });
  const outPath = join(dirname(fileURLToPath(import.meta.url)), '../public/well-knowns-delta-2026-03-24.jsonl');
  writeFileSync(outPath, text);
  console.log(`\nSaved to public/well-knowns-delta-2026-03-24.jsonl`);
} else {
  const errText = await res.text();
  console.log('Error body:', errText);
}
