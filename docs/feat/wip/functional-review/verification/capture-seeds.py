#!/usr/bin/env python3
"""Task 2 controller for four fixed seeds; not the Task 7 general staging helper.

Run outside actor inputs. Uses the Task 1 immutable filtered snapshot. All
destinations are fresh, caller-selected controller/actor directories. Python 3.11+
is needed only to read the locally installed PAL configuration via tomllib.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tomllib

from probe_state import run_environment

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SEEDS = {
    "R1": ("review-code", "functional-cleanup-ownership", ("standard", "isolated")),
    "R3": ("review-code", "functional-disabled-provider-history", ("standard", "isolated")),
    "I1": ("implement", "functional-plan-delivery-conflict", ("plan",)),
    "I2": ("implement", "functional-standalone-patch-contract", ("standalone",)),
}
BASELINE = "c2d28c9e3064a0a71a0e5ac3748a9616c794eb61"
OWNED = {".git", ".runner", ".capy.toml", ".agents", ".codex", ".claude", "plugins"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def write_new_json(path, value):
    with path.open("x") as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True) + "\n")


def seal(evidence, credential_values=None):
    """Sanitize the entire package before hashing, including stderr and snapshots."""
    if credential_values is None:
        pal_env = tomllib.loads((Path.home() / ".codex/config.toml").read_text())["mcp_servers"]["pal"].get("env", {})
        credential_values = [v for k,v in pal_env.items() if any(s in k for s in ("KEY", "TOKEN", "SECRET")) and v]
    changes = []
    for path in sorted(evidence.rglob("*")):
        if not path.is_file() or path.name == "manifest.json":
            continue
        original = path.read_bytes()
        sanitized = original
        for value in credential_values:
            sanitized = sanitized.replace(value.encode(), b"[credential redacted]")
        if sanitized != original:
            path.write_bytes(sanitized)
            changes.append({"path": str(path.relative_to(evidence)), "sanitized_sha256": sha(sanitized)})
    record = evidence / "credential-redactions.json"
    previous = json.loads(record.read_text()).get("redactions", []) if record.exists() else []
    write_json(record, {"redactions": previous + changes,
        "coverage": "redacted content cannot establish exact payload bytes" if previous or changes else "no configured credential value present"})
    inventory = files(evidence)
    inventory.pop("manifest.json", None)
    write_json(evidence / "manifest.json", inventory)


def fixture(case):
    skill, name, _ = SEEDS[case]
    return REPO / "klaude-plugin/skills" / skill / "evals" / name


def files(root):
    return {p.relative_to(root).as_posix(): sha(p.read_bytes())
            for p in sorted(root.rglob("*")) if p.is_file()}


def git(workspace, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
               GIT_AUTHOR_DATE="2026-10-08T00:00:00Z", GIT_COMMITTER_DATE="2026-10-08T00:00:00Z")
    return subprocess.check_output(["git", "-c", "core.hooksPath=" + os.devnull,
        "-c", "commit.gpgsign=false", "-c", "user.name=Workflow Eval",
        "-c", "user.email=eval@example.invalid", "-C", str(workspace), *args], env=env)


def copy_subject(source, workspace):
    # Fixed seeds contain regular files only. Fail closed if that changes.
    for path in source.rglob("*"):
        rel = path.relative_to(source)
        if path.is_symlink() or rel.parts[0] in OWNED or any(p == ".git" for p in rel.parts):
            raise ValueError("Unexpected fixture input: " + str(rel))
        if path.is_file():
            target = workspace / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def replace_subject(source, workspace):
    for path in workspace.iterdir():
        if path.name not in OWNED:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
    copy_subject(source, workspace)


def subject_snapshot(workspace, destination):
    destination.mkdir(parents=True, exist_ok=False)
    # Exclude runner metadata and ignored artifacts. Include new actor files.
    paths = git(workspace, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
    for name in sorted(set(paths.decode().split("\0")) - {""}):
        path = workspace / name
        if path.is_symlink():
            raise ValueError("Unexpected actor-created symlink: " + name)
        if path.is_file():
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    return files(destination)


def prompt_for(case, mode, provider):
    prompt = json.loads((fixture(case) / "eval.json").read_text())["prompt"]
    if mode == "isolated":
        prompt = prompt.replace("/kk:review-code`", "/kk:review-code:isolated`")
    if provider == "codex":
        # Generated skills use $kk: names; isolated is an argument to review-code.
        prompt = prompt.replace("/kk:review-code:isolated", "$kk:review-code isolated")
        prompt = prompt.replace("/kk:", "$kk:")
    return prompt


def freeze(destination):
    data = {"actor_revision": BASELINE, "fixtures": {}, "prompts": {},
            "rubric_sha256": sha((HERE / "task2-rubric.md").read_bytes()),
            "controller_sha256": sha(Path(__file__).read_bytes()),
            "runtimes": {}, "concrete_grader": "pending Task 8; no grades assigned"}
    for case, (_, _, modes) in SEEDS.items():
        data["fixtures"][case] = files(fixture(case))
        for mode in modes:
            for provider in ("claude", "codex"):
                data["prompts"][f"{provider}/{case}/{mode}"] = prompt_for(case, mode, provider)
    for name in ("claude", "codex", "capy", "python3"):
        data["runtimes"][name] = subprocess.check_output([name, "--version"], text=True).strip()
    if destination.exists():
        raise FileExistsError(destination)
    write_json(destination, data)


def verify_frozen(frozen):
    data = json.loads(frozen.read_text())
    for case in SEEDS:
        if files(fixture(case)) != data["fixtures"][case]:
            raise ValueError("Fixture changed after freeze: " + case)
    if sha((HERE / "task2-rubric.md").read_bytes()) != data["rubric_sha256"]:
        raise ValueError("Rubric changed after freeze")
    return data


def prepare(args):
    frozen = verify_frozen(args.frozen)
    if args.mode not in SEEDS[args.case][2]:
        raise ValueError("Unsupported case/mode")
    identity = json.loads((args.snapshot / "identity.json").read_text())
    if identity["revision"] != BASELINE:
        raise ValueError("Not the declared baseline")
    w = args.workspace.resolve()
    w.mkdir(parents=True, exist_ok=False)
    args.evidence.mkdir(parents=True, exist_ok=False)
    git(w, "init", "--template=", "-q")
    (w / ".git/info").mkdir(exist_ok=True)
    (w / ".git/info/exclude").write_text("\n".join(OWNED - {".git"}) + "\n")
    source = fixture(args.case) / "test-files"
    history = source / "history.json"
    if history.exists():
        for entry in json.loads(history.read_text())["snapshots"]:
            if entry != {"path": "history/released", "tag": "eval-release"}:
                raise ValueError("Unexpected fixed-seed history entry")
            copy_subject(source / entry["path"], w)
            git(w, "add", ".")
            git(w, "commit", "-qm", "Released provider")
            git(w, "tag", entry["tag"])
    paired = (source / "before").is_dir()
    replace_subject(source / "before" if paired else source, w)
    git(w, "add", ".")
    git(w, "commit", "-qm", "Review base" if paired else "Initial subject")
    base = git(w, "rev-parse", "HEAD").decode().strip()
    if paired:
        replace_subject(source / "after", w)
        git(w, "add", ".")
    runner = w / ".runner"
    runner.mkdir()
    (w / ".capy.toml").write_text('[store]\npath = ".runner/knowledge.db"\nkey_file = ""\n')
    tree = "klaude-plugin" if args.provider == "claude" else "kodex-plugin"
    bundle = w / "plugins/kk"
    shutil.copytree(args.snapshot / "retained" / tree, bundle, symlinks=True)
    subprocess.run([sys.executable, "-B", str(HERE / "prepare-bundles.py"), "verify", str(bundle),
                    str(args.snapshot / "retained-manifest.json"), tree], check=True)
    capy = {"command": "env", "args": ["-u", "CAPY_VAULT_KEY", "-u", "CAPY_DB_KEY",
        "CAPY_DB_KEY=synthetic-functional-review-probe-key-20261008",
        "CAPY_VAULT_PATH=" + str(runner / "vault"), "XDG_CONFIG_HOME=" + str(runner / "xdg"),
        shutil.which("capy"), "--project-dir", str(w), "serve"]}
    pal_config = tomllib.loads((Path.home() / ".codex/config.toml").read_text())["mcp_servers"]["pal"]
    pal = {k: pal_config[k] for k in ("command", "args") if k in pal_config}
    # Existing credentials are used by the configured local PAL server only.
    # Supply credentials via the launcher environment, not an actor-readable file.
    mcp = {"capy": capy, "pal": pal}
    write_json(runner / "mcp.json", {"mcpServers": mcp})
    (runner / "mcp.json").chmod(0o600)
    marketplace = "fr-c2d28c9e-seeds"
    if args.provider == "claude":
        write_json(runner / "registry.json", {"version": 2, "plugins": {"kk@" + marketplace: [
            {"scope": "project", "projectPath": str(w), "installPath": str(bundle), "version": "0.23.0",
             "installedAt": "2026-10-08T00:00:00Z"}]}})
        write_json(runner / "settings.json", {"autoMemoryEnabled": False,
                   "permissions": {"additionalDirectories": [str(bundle)]}})
    else:
        write_json(w / ".agents/plugins/marketplace.json", {"name": marketplace,
            "plugins": [{"name": "kk", "source": {"source": "local", "path": "./plugins/kk"},
                         "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                         "category": "Productivity"}]})
        shutil.copytree(args.snapshot / "retained/.codex/agents", w / ".codex/agents")
        config = ('model = "gpt-6-astra"\nmodel_reasoning_effort = "xhigh"\n'
                  'approval_policy = "never"\nsandbox_mode = "workspace-write"\n'
                  '[plugins."kk@fr-c2d28c9e-seeds"]\nenabled = true\n'
                  '[plugins."kk@claude-toolbox"]\nenabled = false\n'
                  '[mcp_servers.capy]\ncommand = "env"\nargs = ' + json.dumps(capy["args"]) + '\n')
        for name in ("context7", "linear"):
            config += '[mcp_servers.' + name + ']\nenabled = false\n'
        (w / ".codex/config.toml").write_text(config)
    expected = w / ".runner/knowledge.db"
    resolved = subprocess.check_output(["capy", "--project-dir", str(w), "which"],
                                      env=run_environment(w), cwd=w, text=True).strip()
    if Path(resolved).resolve() != expected or expected.exists():
        raise ValueError("Not a fresh, run-local knowledge store")
    initial = subject_snapshot(w, args.evidence / "initial")
    expected_files = files(source / "after" if paired else source)
    if initial != expected_files:
        raise ValueError("Staged subject differs from fixed fixture")
    (args.evidence / "initial.patch").write_bytes(git(w, "diff", "--cached", "--binary"))
    prompt = frozen["prompts"][f"{args.provider}/{args.case}/{args.mode}"]
    (args.evidence / "prompt.txt").write_text(prompt + "\n")
    metadata = {"provider": args.provider, "case": args.case, "mode": args.mode,
        "workspace": str(w), "actor": identity, "review_base": base, "initial_files": initial,
        "fixture_manifest_sha256": sha(args.frozen.read_bytes()), "rubric_sha256": frozen["rubric_sha256"],
        "initial_knowledge": "empty; database absent", "knowledge_path": resolved,
        "vault": "unavailable; private path and unset key", "prompt": prompt,
        "models": {"claude": "claude-opus-4-8[1m]/high", "codex": "gpt-6-astra/xhigh",
                   "codex_reviewer": "gpt-6.1-sol/xhigh", "pal": "gemini-3.1-pro-preview/max"},
        "mcp": {k: {**{a:b for a,b in v.items() if a != "env"},
                         "environment_keys": sorted(v.get("env", {}))} for k,v in mcp.items()},
        "read_confinement": "No OS-wide confinement; audit actual reads for evaluator material"}
    if history.exists():
        metadata["release_revision"] = git(w, "rev-parse", "eval-release").decode().strip()
        metadata["release_blob"] = git(w, "rev-parse", "eval-release:provider/settings.py").decode().strip()
        (args.evidence / "released-provider.py").write_bytes(git(w, "show", "eval-release:provider/settings.py"))
        if (w / "provider/settings.py").exists() or b"provider/settings.py" in git(w, "diff", "--cached"):
            raise ValueError("Historical source leaked into candidate or PR diff")
    write_json(args.evidence / "launch.json", metadata)
    print(json.dumps({"status": "prepared", "workspace": str(w), "evidence": str(args.evidence)}))


def sanitize_claude(event):
    """Retain observable tool traffic and reports, never private thinking blocks."""
    if event.get("type") in ("assistant", "user"):
        message = event.get("message", {})
        if not isinstance(message, dict):
            return None
        content = message.get("content", [])
        if not isinstance(content, list):
            return None
        allowed = [b for b in content if isinstance(b, dict) and b.get("type") in ("tool_use", "tool_result", "text")]
        if not allowed:
            return None
        return {k:v for k,v in event.items() if k != "message"} | {
            "message": {k:v for k,v in event["message"].items() if k != "content"} | {"content": allowed}}
    if event.get("type") in ("system", "result", "tool_progress", "tool_use_summary"):
        return event
    return None


def capture_payloads(arguments, workspace, evidence, sequence):
    """Save actual referenced files at submission, before a reviewer can delete them."""
    text = json.dumps(arguments)
    candidates = set(re.findall(r'/[^\s"<>`\\]+', text))
    captured = []
    for name in candidates:
        path = Path(name.rstrip(".,:;)\\"))
        try:
            resolved = path.resolve(strict=True)
            # Only actor inputs or its temporary review artifacts, never controller data.
            actor_input = resolved.is_relative_to(workspace) and not resolved.is_relative_to(workspace / ".runner")
            temp_input = resolved.parent == Path("/private/tmp") and resolved.name.startswith("kk-review-")
            if not (actor_input or temp_input) or not resolved.is_file():
                continue
            content = resolved.read_bytes()
            if len(content) > 2_000_000:
                captured.append({"path": str(path), "status": "too large; coverage incomplete"})
                continue
            digest = sha(content)
            target = evidence / "payloads" / digest
            target.parent.mkdir(exist_ok=True)
            target.write_bytes(content)
            captured.append({"path": str(path), "sha256": digest, "artifact": str(target.relative_to(evidence))})
        except (OSError, ValueError):
            continue
    if captured:
        with (evidence / "payload-events.jsonl").open("a") as stream:
            stream.write(json.dumps({"event_sequence": sequence, "files": captured}) + "\n")


def run_claude(evidence):
    if any((evidence / name).exists() for name in ("command.json", "events.jsonl", "manifest.json")):
        raise FileExistsError("Refuse to overwrite a run")
    try:
        _run_claude(evidence)
    finally:
        # Run only after this attempt owns command.json; a refused retry writes nothing.
        if (evidence / "command.json").exists():
            seal(evidence)


def _run_claude(evidence):
    meta = json.loads((evidence / "launch.json").read_text())
    w = Path(meta["workspace"])
    env = run_environment(w)
    env.pop("CLAUDECODE", None)
    env["CPR_PLUGINS_FILE"] = str(w / ".runner/registry.json")
    pal_env = tomllib.loads((Path.home() / ".codex/config.toml").read_text())["mcp_servers"]["pal"].get("env", {})
    env.update({key:value for key,value in pal_env.items() if key != "PATH"})
    # Same policy on both sides; normal plugin hooks stay enabled.
    allowed = ["Read", "Glob", "Grep", "Skill", "Agent", "Edit", "Write", "TodoWrite",
        "Bash(git *)", "Bash(python3 *)", "Bash(rg *)", "Bash(ls *)", "Bash(cat *)", "Bash(sed *)",
        "Bash(pwd)", "Bash(wc *)", "Bash(mktemp *)", "Bash(rm /tmp/kk-review-*)",
        "Bash(command -v *)", "Bash(capy *)", "Bash(printenv TOOLBOX_PLUGIN_ROOT)",
        "mcp__capy__capy_search", "mcp__capy__capy_index", "mcp__capy__capy_vault_search",
        "mcp__pal__listmodels", "mcp__pal__codereview"]
    command = ["claude", "-p", "--model", "claude-opus-4-8[1m]", "--effort", "high",
        "--plugin-dir", "./plugins/kk", "--setting-sources", "project,local",
        "--settings", ".runner/settings.json", "--mcp-config", ".runner/mcp.json", "--strict-mcp-config",
        "--no-session-persistence", "--permission-mode", "dontAsk", "--output-format", "stream-json",
        "--verbose", "--include-hook-events", "--forward-subagent-text", "--allowedTools", *allowed,
        "--", meta["prompt"]]
    write_new_json(evidence / "command.json", {"argv":command,
        "controller_sha256": sha(Path(__file__).read_bytes()),
        "policy": "explicit tools; normal hooks; no requirement-changing replies"})
    with (evidence / "stderr.txt").open("x") as errors, (evidence / "events.jsonl").open("x") as events:
        process = subprocess.Popen(command, cwd=w, env=env, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=errors, text=True, start_new_session=True)
        try:
            for seq, line in enumerate(process.stdout, 1):
                event = json.loads(line)
                message = event.get("message", {})
                content = message.get("content", []) if isinstance(message, dict) else []
                for block in content if isinstance(content, list) else []:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        capture_payloads(block.get("input", {}), w, evidence, seq)
                retained = sanitize_claude(event)
                if retained:
                    serialized = json.dumps({"sequence": seq, "event": retained})
                    for key, value in pal_env.items():
                        if any(part in key for part in ("KEY", "TOKEN", "SECRET")) and value:
                            serialized = serialized.replace(value, "[credential redacted]")
                    events.write(serialized + "\n")
                    events.flush()
                if event.get("type") == "result":
                    (evidence / "report.md").write_text(event.get("result", "") + "\n")
            status = process.wait()
        except BaseException as exc:
            write_json(evidence / "capture-error.json", {"error": type(exc).__name__, "message": str(exc),
                "coverage": "incomplete; cannot count as a complete workflow capture"})
            raise
        finally:
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
            process.stdout.close()
    final = subject_snapshot(w, evidence / "final")
    (evidence / "final.patch").write_bytes(git(w, "diff", "HEAD", "--binary"))
    write_json(evidence / "completion.json", {"exit_code": status, "final_files": final,
        "grading": "not graded; concrete workflow grader pending", "private_reasoning": "omitted at capture"})
    print(json.dumps({"evidence": str(evidence), "exit_code": status}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    frozen = sub.add_parser("freeze")
    frozen.add_argument("destination", type=Path)
    prep = sub.add_parser("prepare")
    prep.add_argument("provider", choices=("claude", "codex"))
    prep.add_argument("case", choices=SEEDS)
    prep.add_argument("mode")
    prep.add_argument("snapshot", type=Path)
    prep.add_argument("workspace", type=Path)
    prep.add_argument("evidence", type=Path)
    prep.add_argument("frozen", type=Path)
    run = sub.add_parser("claude")
    run.add_argument("evidence", type=Path)
    args = parser.parse_args()
    if args.command == "freeze":
        freeze(args.destination)
    elif args.command == "prepare":
        prepare(args)
    else:
        run_claude(args.evidence)


if __name__ == "__main__":
    main()
