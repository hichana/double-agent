#!/usr/bin/env python3
"""
AgentMail CLI — list inboxes, threads, and messages via the AgentMail Python SDK.

Usage:
    python scripts/agentmail.py inboxes               List all inboxes
    python scripts/agentmail.py threads [inbox_id]    List threads (org-wide or per inbox)
    python scripts/agentmail.py messages <inbox_id>   List messages in an inbox
    python scripts/agentmail.py read <inbox_id> <message_id>  Read a specific message
    python scripts/agentmail.py thread <inbox_id> <thread_id> Read a specific thread
"""

import sys
import os
import json
import textwrap
from agentmail import AgentMail

API_KEY = os.environ.get("AGENTMAIL_API_KEY")
if not API_KEY:
    print("Error: AGENTMAIL_API_KEY not set in environment.")
    print("  Source ~/.config/double-agent/.env before running this script.")
    sys.exit(1)

client = AgentMail(api_key=API_KEY)


def cmd_inboxes():
    resp = client.inboxes.list()
    inboxes = resp.inboxes if hasattr(resp, "inboxes") else resp
    if not inboxes:
        print("No inboxes found.")
        return
    for inbox in inboxes:
        print(f"  {inbox.inbox_id}  ({getattr(inbox, 'display_name', '')})")


def cmd_threads(inbox_id=None):
    if inbox_id:
        resp = client.inboxes.threads.list(inbox_id=inbox_id)
    else:
        resp = client.threads.list()
    threads = resp.threads if hasattr(resp, "threads") else resp
    if not threads:
        print("No threads found.")
        return
    for t in threads:
        subject = getattr(t, "subject", "(no subject)")
        thread_id = getattr(t, "thread_id", "?")
        snippet = getattr(t, "preview", "") or getattr(t, "snippet", "")
        print(f"  [{thread_id}] {subject}")
        if snippet:
            print(f"    {snippet[:120]}")


def cmd_messages(inbox_id):
    resp = client.inboxes.messages.list(inbox_id=inbox_id)
    messages = resp.messages if hasattr(resp, "messages") else resp
    if not messages:
        print(f"No messages in {inbox_id}.")
        return
    for msg in messages:
        msg_id = getattr(msg, "message_id", "?")
        subject = getattr(msg, "subject", "(no subject)")
        from_ = getattr(msg, "from_", None) or getattr(msg, "sender", "?")
        ts = getattr(msg, "timestamp", "")
        print(f"  [{msg_id}]  {ts}  From: {from_}  Subject: {subject}")


def cmd_read(inbox_id, message_id):
    msg = client.inboxes.messages.get(inbox_id=inbox_id, message_id=message_id)
    print(f"Subject : {getattr(msg, 'subject', '(no subject)')}")
    print(f"From    : {getattr(msg, 'from_', None) or getattr(msg, 'sender', '?')}")
    print(f"Date    : {getattr(msg, 'timestamp', '')}")
    print(f"To      : {getattr(msg, 'to', '')}")
    print()
    body = getattr(msg, "text", None) or getattr(msg, "extracted_text", None) or getattr(msg, "body", None) or "(no body)"
    print(textwrap.fill(body, width=100) if len(body) < 5000 else body[:5000] + "\n...[truncated]")


def cmd_thread(inbox_id, thread_id):
    thread = client.inboxes.threads.get(inbox_id=inbox_id, thread_id=thread_id)
    subject = getattr(thread, "subject", "(no subject)")
    print(f"Thread: {subject}")
    messages = getattr(thread, "messages", [])
    for msg in messages:
        msg_id = getattr(msg, "message_id", "?")
        from_ = getattr(msg, "from_", None) or getattr(msg, "sender", "?")
        ts = getattr(msg, "timestamp", "")
        body = getattr(msg, "text", None) or getattr(msg, "extracted_text", None) or getattr(msg, "body", None) or "(no body)"
        print(f"\n--- [{msg_id}] {ts} From: {from_} ---")
        print(body[:2000])


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]

    if cmd == "inboxes":
        cmd_inboxes()
    elif cmd == "threads":
        cmd_threads(args[1] if len(args) > 1 else None)
    elif cmd == "messages":
        if len(args) < 2:
            print("Usage: agentmail.py messages <inbox_id>")
            sys.exit(1)
        cmd_messages(args[1])
    elif cmd == "read":
        if len(args) < 3:
            print("Usage: agentmail.py read <inbox_id> <message_id>")
            sys.exit(1)
        cmd_read(args[1], args[2])
    elif cmd == "thread":
        if len(args) < 3:
            print("Usage: agentmail.py thread <inbox_id> <thread_id>")
            sys.exit(1)
        cmd_thread(args[1], args[2])
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
