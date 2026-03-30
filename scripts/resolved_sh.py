#!/usr/bin/env python3
"""
resolved.sh CLI — manage listings and datasets via the resolved.sh API.

Reads RESOLVED_SH_API_KEY from environment.

Usage:
    python scripts/resolved_sh.py listings                                     List all listings
    python scripts/resolved_sh.py listing <resource_id>                        Get a listing
    python scripts/resolved_sh.py update <resource_id> [--desc STR] [--md STR] Update a listing
    python scripts/resolved_sh.py upload <resource_id> <file> <price>          Upload a dataset file
    python scripts/resolved_sh.py upload-two-sku <resource_id> <file>          Upload query+download SKUs
    python scripts/resolved_sh.py list-files <resource_id>                     List data files (with UUIDs)
    python scripts/resolved_sh.py patch-price <resource_id> <file_id> <price>  Update file price
    python scripts/resolved_sh.py payout <0x_address>                          Set EVM payout wallet
    python scripts/resolved_sh.py spec                                         Print the resolved.sh llms.txt spec

PRICING STRATEGY
================
The resolved.sh API exposes a single price_usdc field per file, applied equally to
both query (GET /data/{filename}/query) and download (GET /data/{filename}) access.
There is NO separate per-query vs per-download price field.

To achieve cheap-query / expensive-download pricing, we use a two-SKU approach:
upload each dataset twice under different filenames with different prices.

  Query SKU  — filename: *_query.jsonl, queryable=True, price=QUERY_PRICE
               Agents pay QUERY_PRICE per filtered API call.
               Full downloads at this price are cheap but acceptable (agent-first product).

  Download SKU — filename: *_bulk.jsonl, queryable=False, price=DOWNLOAD_PRICE
                Bulk buyers download the full file at DOWNLOAD_PRICE.
                No query access (queryable=False).

Note: queryable can only be set at upload time; PATCH only supports price_usdc and description.
Note: Stripe has a $0.50 floor — prices below $0.50 only work via the x402 path.

Target prices:
  Full Company Index   — query: $0.10, download: $2.00
  Merged Only (vetted) — query: $0.10, download: $1.00
  New This Week        — query: $0.05, download: $0.50
  Raw All Statuses     — download-only: $1.50 (no query SKU; unfiltered, low-signal data)

KNOWN SERVER BUG (filed ticket fb36b36b-f166-4bf7-b291-b86ac913cc96, 2026-03-30)
=================================================================================
GET /listing/{resource_id}/data returns HTTP 402 with:
  {"error": "payment_verification_failed", "detail": "1 validation error for
   DataFileResponse schema_columns Input should be a valid list"}
The schema_columns column is stored as a JSON string in the DB rather than a list;
Pydantic validation fails on deserialization. Until resolved.sh fixes this, the
list-files command will return an error and patch-price cannot discover file UUIDs
automatically. Workaround: supply file_id directly if known, or wait for bug fix.
"""

import sys
import os
import json
import argparse
import requests

BASE = "https://resolved.sh"

# Two-SKU pricing table: (query_price_usdc, download_price_usdc)
# query_price  — charged per filtered query call (x402 path, below $0.50 Stripe floor)
# download_price — charged per full-file download (x402 or Stripe)
PRICING = {
    "x402_ecosystem_full_index.jsonl":   {"query": "0.10", "download": "2.00"},
    "x402_ecosystem_merged_only.jsonl":  {"query": "0.10", "download": "1.00"},
    "x402_ecosystem_new_this_week.jsonl":{"query": "0.05", "download": "0.50"},
    # Raw all-statuses: download-only, no query SKU (unfiltered data, noisy)
    "x402_ecosystem_raw_all.jsonl":      {"query": None,   "download": "1.50"},
}

# Suffix conventions for two-SKU filenames
QUERY_SUFFIX    = "_query"    # e.g. x402_ecosystem_full_index_query.jsonl
DOWNLOAD_SUFFIX = "_bulk"     # e.g. x402_ecosystem_full_index_bulk.jsonl


def api_key():
    key = os.environ.get("RESOLVED_SH_API_KEY")
    if not key:
        print("Error: RESOLVED_SH_API_KEY not set in environment.")
        sys.exit(1)
    return key


def session_token():
    return os.environ.get("RESOLVED_SH_SESSION_TOKEN")


def headers(token=None):
    tok = token or api_key()
    return {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}


def cmd_listings():
    # /dashboard requires session_token (RESOLVED_SH_SESSION_TOKEN), not API key
    tok = session_token()
    if not tok:
        print("Error: RESOLVED_SH_SESSION_TOKEN not set. Dashboard requires a session token.")
        print("  Get one by running the auth flow (POST /auth/link/email then GET /auth/verify-email).")
        print("  The API key (RESOLVED_SH_API_KEY) is used for per-resource operations only.")
        sys.exit(1)
    r = requests.get(f"{BASE}/dashboard", headers=headers(tok))
    r.raise_for_status()
    data = r.json()
    resources = data.get("resources", [])
    paid_actions = {pa["resource_id"]: pa for pa in data.get("paid_actions", [])}
    if not resources:
        print("No listings found.")
        return
    for res in resources:
        rid = res.get("id", "?")
        name = res.get("display_name", "?")
        subdomain = res.get("subdomain", "")
        pa = paid_actions.get(rid, {})
        status = pa.get("status", "?")
        expires = pa.get("expires_at", "")
        print(f"  [{rid}] {name}")
        print(f"    subdomain: {subdomain}.resolved.sh  status: {status}  expires: {expires}")


def cmd_listing(resource_id):
    # Public endpoint — readable by anyone, no auth needed for display
    r = requests.get(f"{BASE}/{resource_id}", headers={"Accept": "application/json"})
    if r.status_code == 404:
        print(f"Resource '{resource_id}' not found.")
        sys.exit(1)
    r.raise_for_status()
    print(json.dumps(r.json(), indent=2))


def cmd_update(resource_id, description=None, md_content=None):
    body = {}
    if description:
        body["description"] = description
    if md_content:
        body["md_content"] = md_content
    r = requests.put(f"{BASE}/listing/{resource_id}", headers=headers(), json=body)
    r.raise_for_status()
    print(json.dumps(r.json(), indent=2))


def cmd_upload(resource_id, filepath, price_usdc, description=None, queryable=None):
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        content = f.read()

    ext = filename.rsplit(".", 1)[-1].lower()
    content_types = {
        "jsonl": "application/jsonl",
        "json": "application/json",
        "csv": "text/csv",
    }
    content_type = content_types.get(ext, "application/octet-stream")

    params = {"price_usdc": price_usdc}
    if description:
        params["description"] = description
    if queryable is not None:
        params["queryable"] = str(queryable).lower()

    upload_headers = {
        "Authorization": f"Bearer {api_key()}",
        "Content-Type": content_type,
    }
    r = requests.put(
        f"{BASE}/listing/{resource_id}/data/{filename}",
        headers=upload_headers,
        params=params,
        data=content,
    )
    r.raise_for_status()
    print(json.dumps(r.json(), indent=2))


def cmd_upload_two_sku(resource_id, filepath):
    """
    Upload a dataset as two SKUs: one for cheap per-query access, one for full downloads.

    Query SKU  (filename *_query.jsonl): queryable=True, priced for per-call agent access.
    Download SKU (filename *_bulk.jsonl): queryable=False, priced for bulk one-time download.

    Prices are read from the PRICING table above, keyed by the base filename.
    """
    base_filename = os.path.basename(filepath)
    pricing = PRICING.get(base_filename)
    if not pricing:
        print(f"Error: No pricing entry for '{base_filename}'. Add it to PRICING table.")
        sys.exit(1)

    stem, ext = base_filename.rsplit(".", 1)

    if pricing["query"] is not None:
        query_filename = f"{stem}{QUERY_SUFFIX}.{ext}"
        print(f"Uploading query SKU: {query_filename} @ ${pricing['query']} (queryable=true)")
        _upload_file(resource_id, filepath, query_filename, pricing["query"], queryable=True,
                     description=f"{stem} — query access. Pay per filtered API call.")

    download_filename = f"{stem}{DOWNLOAD_SUFFIX}.{ext}"
    print(f"Uploading download SKU: {download_filename} @ ${pricing['download']} (queryable=false)")
    _upload_file(resource_id, filepath, download_filename, pricing["download"], queryable=False,
                 description=f"{stem} — full dataset download.")


def _upload_file(resource_id, local_path, remote_filename, price_usdc, queryable, description=None):
    with open(local_path, "rb") as f:
        content = f.read()

    ext = remote_filename.rsplit(".", 1)[-1].lower()
    content_types = {"jsonl": "application/jsonl", "json": "application/json", "csv": "text/csv"}
    content_type = content_types.get(ext, "application/octet-stream")

    params = {"price_usdc": price_usdc, "queryable": str(queryable).lower()}
    if description:
        params["description"] = description

    r = requests.put(
        f"{BASE}/listing/{resource_id}/data/{remote_filename}",
        headers={"Authorization": f"Bearer {api_key()}", "Content-Type": content_type},
        params=params,
        data=content,
    )
    r.raise_for_status()
    result = r.json()
    print(f"  -> file_id: {result.get('id')}  price: ${result.get('price_usdc')}  queryable: {result.get('queryable')}")


def cmd_list_files(resource_id):
    """
    List data files for a resource (requires API key auth).

    NOTE: As of 2026-03-30 this endpoint returns HTTP 402 due to a resolved.sh server bug:
    schema_columns is stored as a JSON string in the DB but Pydantic expects a list.
    Support ticket filed: fb36b36b-f166-4bf7-b291-b86ac913cc96
    """
    r = requests.get(
        f"{BASE}/listing/{resource_id}/data",
        headers=headers(),
    )
    if r.status_code == 402:
        data = r.json()
        if "schema_columns" in data.get("detail", ""):
            print("ERROR: resolved.sh server bug — schema_columns stored as string, not list.")
            print("Support ticket: fb36b36b-f166-4bf7-b291-b86ac913cc96")
            print("Cannot retrieve file UUIDs until this is fixed server-side.")
            sys.exit(1)
    r.raise_for_status()
    files = r.json().get("files", [])
    for f in files:
        print(f"  [{f['id']}] {f['filename']}  price=${f['price_usdc']}  queryable={f.get('queryable')}  rows={f.get('row_count')}")


def cmd_patch_price(resource_id, file_id, price_usdc, description=None):
    """
    Update the price (and optionally description) of an existing data file.

    Requires the file UUID — obtainable via list-files once the server bug is fixed,
    or from the upload response when files are (re-)uploaded.
    """
    body = {"price_usdc": price_usdc}
    if description:
        body["description"] = description
    r = requests.patch(
        f"{BASE}/listing/{resource_id}/data/{file_id}",
        headers=headers(),
        json=body,
    )
    r.raise_for_status()
    result = r.json()
    print(f"Updated: {result.get('filename')}  price=${result.get('price_usdc')}  queryable={result.get('queryable')}")
    print(json.dumps(result, indent=2))


def cmd_payout(wallet_address):
    body = {"payout_address": wallet_address}
    r = requests.post(f"{BASE}/account/payout-address", headers=headers(), json=body)
    r.raise_for_status()
    print(json.dumps(r.json(), indent=2))


def cmd_spec():
    r = requests.get("https://resolved.sh/llms.txt")
    r.raise_for_status()
    print(r.text)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "listings":
        cmd_listings()
    elif cmd == "listing":
        if len(sys.argv) < 3:
            print("Usage: resolved_sh.py listing <resource_id>")
            sys.exit(1)
        cmd_listing(sys.argv[2])
    elif cmd == "update":
        parser = argparse.ArgumentParser()
        parser.add_argument("resource_id")
        parser.add_argument("--desc", default=None)
        parser.add_argument("--md", default=None)
        args = parser.parse_args(sys.argv[2:])
        cmd_update(args.resource_id, args.desc, args.md)
    elif cmd == "upload":
        if len(sys.argv) < 5:
            print("Usage: resolved_sh.py upload <resource_id> <file> <price_usdc>")
            sys.exit(1)
        desc = sys.argv[5] if len(sys.argv) > 5 else None
        cmd_upload(sys.argv[2], sys.argv[3], sys.argv[4], desc)
    elif cmd == "upload-two-sku":
        if len(sys.argv) < 4:
            print("Usage: resolved_sh.py upload-two-sku <resource_id> <file>")
            sys.exit(1)
        cmd_upload_two_sku(sys.argv[2], sys.argv[3])
    elif cmd == "list-files":
        if len(sys.argv) < 3:
            print("Usage: resolved_sh.py list-files <resource_id>")
            sys.exit(1)
        cmd_list_files(sys.argv[2])
    elif cmd == "patch-price":
        parser = argparse.ArgumentParser()
        parser.add_argument("resource_id")
        parser.add_argument("file_id")
        parser.add_argument("price_usdc")
        parser.add_argument("--desc", default=None)
        args = parser.parse_args(sys.argv[2:])
        cmd_patch_price(args.resource_id, args.file_id, args.price_usdc, args.desc)
    elif cmd == "payout":
        if len(sys.argv) < 3:
            print("Usage: resolved_sh.py payout <0x_address>")
            sys.exit(1)
        cmd_payout(sys.argv[2])
    elif cmd == "spec":
        cmd_spec()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
