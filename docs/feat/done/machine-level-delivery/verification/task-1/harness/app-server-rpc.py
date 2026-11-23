#!/usr/bin/env python3
"""Send one request to `codex [ARGS...] app-server` over stdio JSON-RPC.

Usage: app-server-rpc.py METHOD PARAMS_JSON [CODEX_ARG ...]

Example: app-server-rpc.py hooks/list '{"cwds": ["/repo"]}' -c features.hooks=false

CODEX_ARGs go before the `app-server` subcommand; Codex 0.170.0 accepts `-c`
there but rejects `--profile`. Prints {"request": ..., "response": ...} as JSON
on stdout and the wall-clock time of the whole exchange on stderr. Gives up
after DEADLINE_SECONDS. Uses the environment's CODEX_HOME. Standard library
only; Python 3.8 syntax; POSIX only (SIGALRM).
"""
import json
import signal
import subprocess
import sys
import time

DEADLINE_SECONDS = 60


def main():
    method, params = sys.argv[1], json.loads(sys.argv[2])
    signal.alarm(DEADLINE_SECONDS)
    codex_args = sys.argv[3:]
    start = time.monotonic()
    proc = subprocess.Popen(
        ["codex"] + codex_args + ["app-server"],
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
            if line:
                msg = json.loads(line)
                if msg.get("id") == req_id:
                    return msg
        raise SystemExit("app-server closed before answering request %r" % req_id)

    send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
          "params": {"clientInfo": {"name": "kkprobe", "version": "0.0.0"}}})
    wait_for(1)
    send({"jsonrpc": "2.0", "method": "initialized"})
    request = {"jsonrpc": "2.0", "id": 2, "method": method, "params": params}
    send(request)
    response = wait_for(2)
    elapsed = time.monotonic() - start
    stdin.close()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
    json.dump({"codex_args": codex_args, "request": request, "response": response}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    sys.stderr.write("elapsed_seconds=%.3f\n" % elapsed)


if __name__ == "__main__":
    main()
