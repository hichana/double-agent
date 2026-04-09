#!/usr/bin/env python3
"""
resolved.sh CLI — manage listings and datasets via the resolved.sh API.

Reads RESOLVED_SH_API_KEY from environment.

Usage:
    python scripts/resolved_sh.py listings                                          List all listings
    python scripts/resolved_sh.py listing <resource_id>                             Get a listing
    python scripts/resolved_sh.py update <resource_id> [--desc STR] [--md STR]     Update a listing
    python scripts/resolved_sh.py upload <resource_id> <file> <price>               Upload a dataset file
    python scripts/resolved_sh.py list-files <resource_id>                          List data files (with UUIDs)
    python scripts/resolved_sh.py patch-price <resource_id> <file_id>               Update file pricing
    python scripts/resolved_sh.py publish-post <resource_id> <slug> <title> <md_file> [--price 0] [--published-at ISO]  Publish a post
    python scripts/resolved_sh.py payout <0x_address>                               Set EVM payout wallet
    python scripts/resolved_sh.py spec                                              Print the resolved.sh llms.txt spec

PRICING
=======
The API supports two separate price fields per file:
  query_price_usdc    — charged per filtered query call (GET /data/{filename}/query)
  download_price_usdc — charged per full file download  (GET /data/{filename})

Both can be set independently on upload (query params) or via PATCH (request body).
If only price_usdc is set, it applies to both query and download (fallback).
effective_query_price and effective_download_price in responses show the resolved values.

Note: Stripe has a $0.50 floor — prices below $0.50 only work via the x402 path.

Live prices (resource e8592c18-9052-47b5-bfa3-bfe699193d0e / agentagent.resolved.sh):

  File                               query_price  download_price  queryable
  x402_ecosystem_full_index.jsonl    $0.10        $2.00           true
  x402_ecosystem_merged_only.jsonl   $0.05        $1.00           true
  x402_ecosystem_new_this_week.jsonl $0.05        $0.50           true
  x402_ecosystem_raw_all.jsonl       —            $1.50           false

File UUIDs:
  x402_ecosystem_full_index.jsonl    b2b44492-5e6a-4aff-910f-f714b0cec595
  x402_ecosystem_merged_only.jsonl   232cc77c-3b95-4b26-9f08-7f053a554b42
  x402_ecosystem_new_this_week.jsonl 59ddecd5-38f1-4740-88d3-e6ef3f0f7e27
  x402_ecosystem_raw_all.jsonl       2168cb16-4948-422b-a804-ce723f80e943
"""

import sys
import os
import json
import argparse
import requests

BASE = "https://resolved.sh"

# Pricing table for dataset uploads.
# query    — per filtered query call; None = not queryable (download-only)
# download — per full file download
PRICING = {
    "x402_ecosystem_full_index.jsonl":    {"query": "0.10", "download": "2.00"},
    "x402_ecosystem_merged_only.jsonl":   {"query": "0.05", "download": "1.00"},
    "x402_ecosystem_new_this_week.jsonl": {"query": "0.05", "download": "0.50"},
    "x402_ecosystem_raw_all.jsonl":       {"query": None,   "download": "1.50"},
}


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


def cmd_upload(resource_id, filepath, price_usdc, query_price_usdc=None,
               download_price_usdc=None, description=None):
    """
    Upload a dataset file. Supports split pricing via query_price_usdc and
    download_price_usdc. If only price_usdc is given, it applies to both.

    For known filenames, pricing is auto-resolved from the PRICING table
    when query_price_usdc / download_price_usdc are not explicitly passed.
    """
    filename = os.path.basename(filepath)

    # Auto-resolve from PRICING table if not explicitly set
    pricing = PRICING.get(filename, {})
    if query_price_usdc is None and pricing.get("query") is not None:
        query_price_usdc = pricing["query"]
    if download_price_usdc is None and pricing.get("download") is not None:
        download_price_usdc = pricing["download"]

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
    if query_price_usdc is not None:
        params["query_price_usdc"] = query_price_usdc
    if download_price_usdc is not None:
        params["download_price_usdc"] = download_price_usdc
    if description:
        params["description"] = description

    r = requests.put(
        f"{BASE}/listing/{resource_id}/data/{filename}",
        headers={"Authorization": f"Bearer {api_key()}", "Content-Type": content_type},
        params=params,
        data=content,
    )
    r.raise_for_status()
    result = r.json()
    print(json.dumps(result, indent=2))
    _print_pricing(result)


def cmd_list_files(resource_id):
    """List data files with UUIDs and effective pricing."""
    r = requests.get(f"{BASE}/listing/{resource_id}/data", headers=headers())
    r.raise_for_status()
    files = r.json().get("files", [])
    for f in files:
        qp = f.get("effective_query_price", "—")
        dp = f.get("effective_download_price", "—")
        print(f"  [{f['id']}] {f['filename']}")
        print(f"    query=${qp}  download=${dp}  queryable={f.get('queryable')}  rows={f.get('row_count')}")


def cmd_patch_price(resource_id, file_id, price_usdc=None, query_price_usdc=None,
                    download_price_usdc=None, description=None):
    """
    Update pricing (and optionally description) of an existing data file.
    Set query_price_usdc and download_price_usdc independently.
    Pass "0" to clear a split override and revert to price_usdc fallback.
    """
    body = {}
    if price_usdc is not None:
        body["price_usdc"] = price_usdc
    if query_price_usdc is not None:
        body["query_price_usdc"] = query_price_usdc
    if download_price_usdc is not None:
        body["download_price_usdc"] = download_price_usdc
    if description is not None:
        body["description"] = description
    if not body:
        print("Nothing to patch — supply at least one of: --price, --query-price, --download-price, --desc")
        sys.exit(1)
    r = requests.patch(
        f"{BASE}/listing/{resource_id}/data/{file_id}",
        headers=headers(),
        json=body,
    )
    r.raise_for_status()
    result = r.json()
    print(f"Updated: {result.get('filename')}")
    _print_pricing(result)


def _print_pricing(result):
    qp = result.get("effective_query_price")
    dp = result.get("effective_download_price")
    queryable = result.get("queryable")
    if queryable:
        print(f"  query=${qp}  download=${dp}")
    else:
        print(f"  download=${dp}  (not queryable)")


def cmd_publish_post(resource_id, slug, title, md_content, price_usdc=0, published_at=None):
    """
    Publish or update a post on the listing.
    PUT /listing/{id}/posts/{slug}
    """
    body = {"title": title, "md_content": md_content, "price_usdc": price_usdc}
    if published_at:
        body["published_at"] = published_at
    r = requests.put(
        f"{BASE}/listing/{resource_id}/posts/{slug}",
        headers=headers(),
        json=body,
    )
    r.raise_for_status()
    print(json.dumps(r.json(), indent=2))


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
        parser = argparse.ArgumentParser()
        parser.add_argument("resource_id")
        parser.add_argument("file")
        parser.add_argument("price_usdc")
        parser.add_argument("--query-price", default=None, dest="query_price")
        parser.add_argument("--download-price", default=None, dest="download_price")
        parser.add_argument("--desc", default=None)
        args = parser.parse_args(sys.argv[2:])
        cmd_upload(args.resource_id, args.file, args.price_usdc,
                   query_price_usdc=args.query_price,
                   download_price_usdc=args.download_price,
                   description=args.desc)

    elif cmd == "list-files":
        if len(sys.argv) < 3:
            print("Usage: resolved_sh.py list-files <resource_id>")
            sys.exit(1)
        cmd_list_files(sys.argv[2])

    elif cmd == "publish-post":
        parser = argparse.ArgumentParser()
        parser.add_argument("resource_id")
        parser.add_argument("slug")
        parser.add_argument("title")
        parser.add_argument("md_file")
        parser.add_argument("--price", default=0, type=float)
        parser.add_argument("--published-at", default=None, dest="published_at")
        args = parser.parse_args(sys.argv[2:])
        with open(args.md_file) as f:
            md_content = f.read()
        cmd_publish_post(args.resource_id, args.slug, args.title, md_content,
                         price_usdc=args.price, published_at=args.published_at)

    elif cmd == "patch-price":
        parser = argparse.ArgumentParser()
        parser.add_argument("resource_id")
        parser.add_argument("file_id")
        parser.add_argument("--price", default=None)
        parser.add_argument("--query-price", default=None, dest="query_price")
        parser.add_argument("--download-price", default=None, dest="download_price")
        parser.add_argument("--desc", default=None)
        args = parser.parse_args(sys.argv[2:])
        cmd_patch_price(args.resource_id, args.file_id,
                        price_usdc=args.price,
                        query_price_usdc=args.query_price,
                        download_price_usdc=args.download_price,
                        description=args.desc)

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
