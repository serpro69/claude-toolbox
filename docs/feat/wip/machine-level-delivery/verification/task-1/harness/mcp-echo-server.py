#!/usr/bin/env python3
"""Minimal stdio MCP server with one tool, `kkprobe_echo`, for probe 1.6.

Newline-delimited JSON-RPC 2.0. Answers initialize, tools/list and tools/call;
ignores notifications. Standard library only; Python 3.8 syntax.
"""
import json
import sys

TOOL = {
    "name": "kkprobe_echo",
    "description": "Echo the given text back. Probe tool for machine-level-delivery Task 1.",
    "inputSchema": {
        "type": "object",
        "properties": {"text": {"type": "string"}},
        "required": ["text"],
    },
}


def reply(req_id, result):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result}) + "\n")
    sys.stdout.flush()


for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    msg = json.loads(line)
    method, req_id = msg.get("method"), msg.get("id")
    if req_id is None:
        continue
    if method == "initialize":
        reply(req_id, {
            "protocolVersion": msg.get("params", {}).get("protocolVersion", "2025-06-18"),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "kkprobe", "version": "0.0.0"},
        })
    elif method == "tools/list":
        reply(req_id, {"tools": [TOOL]})
    elif method == "tools/call":
        text = msg.get("params", {}).get("arguments", {}).get("text", "")
        reply(req_id, {"content": [{"type": "text", "text": "echo: " + text}]})
    else:
        sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id,
                                     "error": {"code": -32601, "message": "method not found"}}) + "\n")
        sys.stdout.flush()
