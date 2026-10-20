"""Public receipt/use helpers extracted from the historical Codex adapters.

The caller supplies the already configured client and credential values. This
module never reads account configuration or changes plugin/trust registrations.
Collected records do not establish exact submitted prompt content.
"""
import json
from pathlib import Path
import re


def public(value):
    if isinstance(value, dict):
        if value.get("type") in ("reasoning", "thinking", "redacted_thinking"):
            return {"type": "omitted_private_reasoning"}
        return {key: public(item) for key, item in value.items()
                if key != "encrypted_content"}
    if isinstance(value, list):
        return [public(item) for item in value]
    return value


def sanitized(value, credentials=()):
    def redact(item):
        if isinstance(item, str):
            for credential in credentials:
                if credential:
                    item = item.replace(credential, "[credential redacted]")
        elif isinstance(item, dict):
            return {redact(key): redact(entry) for key, entry in item.items()}
        elif isinstance(item, list):
            return [redact(entry) for entry in item]
        return item
    return redact(public(value))


def child_ids(item):
    result = set(item.get("receiverThreadIds", [])) if item.get("type") == "collabAgentToolCall" else set()
    if item.get("type") == "subAgentActivity":
        result.add(item["agentThreadId"])
    return result


def collect_history(server, root_thread, evidence, credentials=()):
    """Collect public paginated history through an existing client's call API.

The client owns transport timeouts and shutdown. A fresh destination is required;
failed attempts remain for inspection. No provider process is launched here.
"""
    evidence = Path(evidence)
    evidence.mkdir(parents=True, exist_ok=False)
    pending, collected = [root_thread], set()
    for message in server.received:
        pending.extend(child_ids(message.get("params", {}).get("item", {})))
    while pending:
        thread = pending.pop(0)
        if not isinstance(thread, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", thread):
            raise ValueError("Unsafe thread identifier")
        if thread in collected:
            continue
        collected.add(thread)
        items, cursor, cursors = [], None, set()
        while True:
            params = {"threadId": thread, "limit": 100}
            if cursor:
                params["cursor"] = cursor
            page = server.call("thread/items/list", params)
            items.extend(page["data"])
            cursor = page.get("nextCursor")
            if not cursor:
                break
            if cursor in cursors:
                raise ValueError("Repeated history cursor")
            cursors.add(cursor)
        # Retain successfully fetched history even if supplementary metadata fails.
        with (evidence / f"items-{thread}.json").open("x") as stream:
            json.dump(sanitized(items, credentials), stream, indent=2)
            stream.write("\n")
        metadata = server.call("thread/read", {"threadId": thread, "includeTurns": False})
        with (evidence / f"thread-{thread}.json").open("x") as stream:
            json.dump(sanitized(metadata, credentials), stream, indent=2)
            stream.write("\n")
        for row in items:
            pending.extend(child_ids(row["item"]))
    return sorted(collected)
