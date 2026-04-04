import { createWalletClient, http, toHex } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { base } from 'viem/chains';

const account = privateKeyToAccount(`0x${process.env.WALLET_PRIVATE_KEY}`);
const walletClient = createWalletClient({ account, chain: base, transport: http() });

console.log('Wallet address:', account.address);

const body = JSON.stringify({
  agent_name: 'double-agent',
  framework: 'custom',
  url: 'https://agentagent.resolved.sh',
  description: 'Autonomous x402 ecosystem intelligence — tracks 311+ companies, publishes queryable datasets'
});

const response = await fetch('https://revettr.com/v1/waitlist', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body
});

if (response.status !== 402) {
  console.log('Status:', response.status);
  console.log('Body:', await response.text());
  process.exit(0);
}

const paymentHeaderB64 = response.headers.get('payment-required');
const decoded = JSON.parse(Buffer.from(paymentHeaderB64, 'base64').toString('utf8'));
const raw = decoded.accepts[0];

console.log('Got 402 — manually signing with USD Coin domain, network=eip155:8453 in header');

const nonce = toHex(crypto.getRandomValues(new Uint8Array(32)));
const validAfter = BigInt(Math.floor(Date.now() / 1000) - 60);
const validBefore = BigInt(Math.floor(Date.now() / 1000) + raw.maxTimeoutSeconds);

// Sign with correct USDC EIP-712 domain
const signature = await walletClient.signTypedData({
  domain: {
    name: 'USD Coin',
    version: '2',
    chainId: 8453,
    verifyingContract: raw.asset,
  },
  types: {
    TransferWithAuthorization: [
      { name: 'from', type: 'address' },
      { name: 'to', type: 'address' },
      { name: 'value', type: 'uint256' },
      { name: 'validAfter', type: 'uint256' },
      { name: 'validBefore', type: 'uint256' },
      { name: 'nonce', type: 'bytes32' },
    ]
  },
  primaryType: 'TransferWithAuthorization',
  message: {
    from: account.address,
    to: raw.payTo,
    value: BigInt(raw.amount),
    validAfter,
    validBefore,
    nonce,
  }
});

// Build payment header using server's network format
const paymentPayload = {
  x402Version: decoded.x402Version,
  scheme: raw.scheme,
  network: raw.network,  // "eip155:8453"
  payload: {
    signature,
    authorization: {
      from: account.address,
      to: raw.payTo,
      value: raw.amount,
      validAfter: validAfter.toString(),
      validBefore: validBefore.toString(),
      nonce,
    }
  }
};

const payment = Buffer.from(JSON.stringify(paymentPayload)).toString('base64');
console.log('Payment payload network:', paymentPayload.network);
console.log('Sending...');

const r2 = await fetch('https://revettr.com/v1/waitlist', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-PAYMENT': payment,
    'Access-Control-Expose-Headers': 'X-PAYMENT-RESPONSE'
  },
  body
});

console.log('Status:', r2.status);
console.log('Result:', await r2.text());
