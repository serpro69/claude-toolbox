#!/usr/bin/env python3
"""Observation-only Codex hook: no stdout, decisions, rewrites or model context."""

import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
import uuid


def main():
    event = json.load(sys.stdin)
    workspace = Path(__file__).resolve().parent.parent
    root = workspace / ".runner/tool-events"
    root.mkdir(exist_ok=True)
    event["captured_at_ns"] = time.time_ns()
    payloads = []
    if event.get("hook_event_name") == "PreToolUse":
        for name in set(re.findall(r'/[^\s"<>`\\]+', json.dumps(event.get("tool_input", {})))):
            path = Path(name.rstrip(".,:;)\\"))
            try:
                resolved = path.resolve(strict=True)
                local = resolved.is_relative_to(workspace) and not resolved.is_relative_to(workspace / ".runner")
                temporary = resolved.parent == Path("/private/tmp") and resolved.name.startswith("kk-review-")
                if not (local or temporary) or not resolved.is_file():
                    continue
                content = resolved.read_bytes()
                if len(content) > 2_000_000:
                    continue
                digest = hashlib.sha256(content).hexdigest()
                destination = workspace / ".runner/payloads" / digest
                destination.parent.mkdir(exist_ok=True)
                destination.write_bytes(content)
                payloads.append({"path": str(path), "sha256": digest})
            except (OSError, ValueError):
                continue
    event["captured_payloads"] = payloads
    # One file per invocation: child hooks may run concurrently.
    target = root / (str(event["captured_at_ns"]) + "-" + uuid.uuid4().hex + ".json")
    descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as stream:
        json.dump(event, stream)
        stream.write("\n")


if __name__ == "__main__":
    main()
