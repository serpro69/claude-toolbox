"""Ask one Codex app-server session about hooks and configuration without changing either."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from threading import Timer
from typing import Any, Dict, Iterable, List, Sequence, Tuple

from .payload import JSONObject, is_object


class NoMethod(Exception):
    """The vendor explicitly reported that a requested method is unavailable."""


def session(directory: Path, workspace: Path, flags: Sequence[str], executable: str,
            requests: Sequence[Tuple[str, JSONObject]], timeout: float) -> List[Any]:
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
        stdin, stdout = proc.stdin, proc.stdout
        assert stdin is not None and stdout is not None  # Both are pipes.

        def send(message: JSONObject) -> None:
            stdin.write(json.dumps(dict(jsonrpc="2.0", **message)) + "\n")
            stdin.flush()

        def request(number: int, method: str, params: JSONObject) -> Any:
            send({"id": number, "method": method, "params": params})
            for line in stdout:
                msg = json.loads(line)
                if not is_object(msg) or msg.get("id") != number:
                    continue
                if "error" in msg:
                    error = msg["error"]
                    # A vendor that rejects the handshake is broken, not older.
                    if method != "initialize" and is_object(error) and error.get("code") == -32601:
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


def origins(directory: Path, workspace: Path, flags: Sequence[str], executable: str,
            timeout: float) -> Tuple[JSONObject, JSONObject]:
    """Return which layer set each configuration leaf for a directory, and the effective config.

    Origins map a dotted canonical path (array elements indexed) to its layer. Codex
    reports no origin for an empty array or table; those appear only in the config.
    """
    result, = session(directory, workspace, flags, executable,
                      [("config/read", {"cwd": str(workspace), "includeLayers": False})], timeout)
    if not (is_object(result) and is_object(result.get("origins")) and is_object(result.get("config"))):
        raise ValueError("Codex config/read returned an unexpected result")
    return result["origins"], result["config"]


def layers(directory: Path, workspace: Path, flags: Sequence[str], executable: str,
           timeout: float) -> Tuple[Dict[str, str], JSONObject]:
    """Return the layer type that set each origin key, and the effective configuration."""
    found, config = origins(directory, workspace, flags, executable, timeout)
    types: Dict[str, str] = {}
    for key, origin in found.items():
        name = origin.get("name") if is_object(origin) else None
        layer = name.get("type") if is_object(name) else None
        if not isinstance(layer, str):
            raise ValueError("Codex config/read returned an unexpected origin for " + key)
        types[key] = layer
    return types, config


def origin_keys(keys: Iterable[str], path: Sequence[str]) -> List[str]:
    """Return the origin keys that stand for the leaf at a path of key components."""
    # Codex reports array elements separately: tui.status_line.0, tui.status_line.1, ...
    name = ".".join(path)
    return [key for key in keys if key == name or key.startswith(name + ".")]
