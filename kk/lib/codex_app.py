"""Ask one Codex app-server session about hooks and configuration without changing either."""

import json
import os
import subprocess
from threading import Timer


class NoMethod(Exception):
    """The vendor explicitly reported that a requested method is unavailable."""


def session(directory, workspace, flags, executable, requests, timeout):
    """Return the results of the ordered (method, params) requests.

    Raises NoMethod when the vendor lacks a requested method, ValueError for any other
    vendor error, a malformed reply, an early exit or the kill timeout, and OSError when
    the vendor cannot be started or stops reading requests.
    """
    with subprocess.Popen([executable, *flags, "app-server"], cwd=workspace,
                          env=dict(os.environ, CODEX_HOME=str(directory)), text=True,
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as proc:
        timer = Timer(timeout, proc.kill)
        timer.start()

        def send(message):
            proc.stdin.write(json.dumps(dict(jsonrpc="2.0", **message)) + "\n")
            proc.stdin.flush()

        def request(number, method, params):
            send({"id": number, "method": method, "params": params})
            for line in proc.stdout:
                msg = json.loads(line)
                if not isinstance(msg, dict) or msg.get("id") != number:
                    continue
                if "error" in msg:
                    error = msg["error"]
                    # A vendor that rejects the handshake is broken, not older.
                    if method != "initialize" and isinstance(error, dict) and error.get("code") == -32601:
                        raise NoMethod("Codex has no {} method".format(method))
                    raise ValueError("Codex {} failed: {}".format(method, error))
                if "result" not in msg:
                    raise ValueError("Codex {} returned no result".format(method))
                return msg["result"]
            raise ValueError("Codex app-server stopped or timed out during " + method)

        try:
            request(1, "initialize", {"clientInfo": {"name": "kk", "version": "1"}})
            send({"method": "initialized"})
            return [request(number, method, params) for number, (method, params) in enumerate(requests, 2)]
        finally:
            timer.cancel()
            proc.kill()
            proc.wait()


def origins(directory, workspace, flags, executable, timeout):
    """Return which layer set each configuration leaf for a directory, and the effective config.

    Origins map a dotted canonical path (array elements indexed) to its layer. Codex
    reports no origin for an empty array or table; those appear only in the config.
    """
    result, = session(directory, workspace, flags, executable,
                      [("config/read", {"cwd": str(workspace), "includeLayers": False})], timeout)
    if not (isinstance(result, dict) and isinstance(result.get("origins"), dict)
            and isinstance(result.get("config"), dict)):
        raise ValueError("Codex config/read returned an unexpected result")
    return result["origins"], result["config"]
