#!/usr/bin/env python3
"""Read Codex hook trust from outside a session through `codex app-server` hooks/list.

Usage: hooks-list.py [cwd ...]

Starts `codex app-server` (stdio JSON-RPC, one JSON object per line) with the
CODEX_HOME of the environment, sends initialize / initialized / hooks/list with
the given cwds, prints the raw request and response as JSON on stdout, and the
wall-clock time of the whole exchange (process start to response) on stderr.
Gives up after DEADLINE_SECONDS. Standard library only; Python 3.8 syntax;
POSIX only (SIGALRM). app-server-rpc.py is the general form of this client.
"""
import json
import signal
import subprocess
import sys
import time

DEADLINE_SECONDS = 60


def main():
    cwds = sys.argv[1:]
    signal.alarm(DEADLINE_SECONDS)
    start = time.monotonic()
    proc = subprocess.Popen(
        ["codex", "app-server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        universal_newlines=True,
    )
    assert proc.stdin is not None and proc.stdout is not None
    stdin, stdout = proc.stdin, proc.stdout

    def send(obj):
        stdin.write(json.dumps(obj) + "\n")
        stdin.flush()

    def wait_for(req_id):
        for line in stdout:
            line = line.strip()
            if not line:
                continue
            msg = json.loads(line)
            if msg.get("id") == req_id:
                return msg
        raise SystemExit("app-server closed before answering request %r" % req_id)

    send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
          "params": {"clientInfo": {"name": "kkprobe", "version": "0.0.0"}}})
    init = wait_for(1)
    send({"jsonrpc": "2.0", "method": "initialized"})
    request = {"jsonrpc": "2.0", "id": 2, "method": "hooks/list", "params": {"cwds": cwds}}
    send(request)
    response = wait_for(2)
    elapsed = time.monotonic() - start
    stdin.close()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
    json.dump({"initialize": init, "request": request, "response": response}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    sys.stderr.write("elapsed_seconds=%.3f\n" % elapsed)


if __name__ == "__main__":
    main()
