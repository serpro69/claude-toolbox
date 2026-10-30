#!/usr/bin/env bash
# Verify the offline evaluator's evidence, not LLM handoff behavior.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 - "$SCRIPT_DIR/../klaude-plugin/skills/handoff/evals/_support/gh" <<'PY'
import base64
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

stub = str(Path(sys.argv[1]).resolve())
with tempfile.TemporaryDirectory(prefix="handoff-stub-test-") as directory:
    root = Path(directory)
    state = root / "state"
    state.mkdir()
    payload = root / "handoff.md"
    prompt = root / "prompt.md"
    original = b"# Continuation\nLiteral `$HOME` and $(false); unicode: \xc3\xb8\n"
    payload.write_bytes(original)
    env = {"PATH": os.environ["PATH"], "HANDOFF_GH_STATE": str(state)}

    def run(*args, mode="producer", failure="none", expected=0):
        result = subprocess.run([stub, *args], cwd=root, capture_output=True,
                                env={**env, "HANDOFF_GH_MODE": mode,
                                     "HANDOFF_GH_FAILURE": failure})
        assert result.returncode == expected, (args, result.returncode, result.stderr)
        return result.stdout.decode().strip()

    def events():
        return [json.loads(line) for line in (state / "calls.jsonl").read_text().splitlines()
                if json.loads(line)["phase"] == "completed"]

    def saved(url):
        return json.loads((state / (url.rsplit("/", 1)[1] + ".json")).read_text())

    run("--version")
    run("gist", "create", "--help")
    url = run("gist", "create", str(payload), "--desc", "Parcel 'task' $(false)")
    prompt.write_text("Read handoff.md at " + url + "\n")
    run("gist", "edit", url, "--add", str(prompt))
    snapshot = saved(url)
    assert snapshot["public"] is False
    assert set(snapshot["files"]) == {"handoff.md", "prompt.md"}
    assert base64.b64decode(snapshot["files"]["handoff.md"]) == original
    assert url in base64.b64decode(snapshot["files"]["prompt.md"]).decode()
    payload.write_text("Changed after upload\n")
    assert run("gist", "view", url, "--filename", "handoff.md", "--raw",
               mode="consumer") == original.decode().strip()
    assert run("gist", "view", snapshot["id"], "--filename", "prompt.md", "--raw",
               mode="consumer") == prompt.read_text().strip()
    assert run("gist", "view", url, "-f", "handoff.md",
               mode="consumer") == original.decode().strip()

    # A new invocation cannot overwrite the earlier snapshot; public stays public.
    public_url = run("gist", "create", "--public", str(payload))
    assert public_url != url and saved(url) == snapshot
    assert saved(public_url)["public"] is True
    partial_url = run("gist", "create", str(payload))
    run("gist", "edit", partial_url, "--add", str(prompt), failure="add", expected=1)
    assert set(saved(partial_url)["files"]) == {"handoff.md"}
    before = sorted(state.glob("*.json"))
    run("gist", "create", str(payload), "--desc", "rejected", failure="create", expected=4)
    assert sorted(state.glob("*.json")) == before
    failures = [event for event in events() if event["exit_code"] in (1, 4)]
    assert len(failures) == 2
    assert base64.b64decode(failures[0]["uploads"][0]["bytes_base64"]) == prompt.read_bytes()
    assert base64.b64decode(failures[1]["uploads"][0]["bytes_base64"]) == payload.read_bytes()
    assert failures[1]["description"] == "rejected"
    run("gist", "edit", "0" * 32, "--add", str(prompt), failure="add", expected=2)
    assert events()[-1]["error"] == "unknown synthetic gist"

    run("gist", "view", url, "--filename", "handoff.md", "--raw", expected=2)
    run("gist", "view", "0" * 32, "--filename", "handoff.md", "--raw",
        mode="consumer", expected=2)
    run("gist", "view", url, "--filename", "missing.md", "--raw",
        mode="consumer", expected=2)
    run("gist", "view", "../outside", "--filename", "handoff.md", "--raw",
        mode="consumer", expected=2)
    run("gist", "create", str(payload), mode="consumer", expected=2)
    run("api", "/gists", expected=2)
    assert events()[-1]["argv"] == ["api", "/gists"]
    assert events()[-1]["error"].startswith("unsupported fixture command")
    assert saved(url) == snapshot
print("PASS: offline gh payload snapshots, visibility, unique IDs, failures, reads and rejected calls")
PY
