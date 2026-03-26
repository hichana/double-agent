#!/usr/bin/env python3
"""
resolved.sh CLI — manage listings and datasets via the resolved.sh API.

Reads RESOLVED_SH_API_KEY from environment.

Usage:
    python scripts/resolved_sh.py listings                              List all listings
    python scripts/resolved_sh.py listing <resource_id>                 Get a listing
    python scripts/resolved_sh.py update <resource_id> [--desc STR] [--md STR]  Update a listing
    python scripts/resolved_sh.py upload <resource_id> <file> <price>  Upload a dataset file
    python scripts/resolved_sh.py payout <resource_id> <0x_address>    Set EVM payout wallet
    python scripts/resolved_sh.py spec                                  Print the resolved.sh llms.txt spec
"""

import sys
import os
import json
import argparse
import requests

BASE = "https://resolved.sh"


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


def cmd_upload(resource_id, filepath, price_usdc, description=None):
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
