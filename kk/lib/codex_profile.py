"""Compose, validate and publish the Codex files owned by the active release."""

import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

from . import codex_plugins, mixed, payload, state
from .claude_launch import check_keys, object_value, switches
from .state import override_path


TIP_TABLE = "\n[tui.model_availability_nux]\n"
# Codex's ModelAvailabilityNuxConfig stores one uint32 per model. Keep the rest of the
# managed profile byte-exact: it can affect the trust check for batch launches.
TIP_COUNTER = re.compile(r'([A-Za-z0-9_-]+|"[^"\\\x00-\x1f\x7f]+") = (0|[1-9][0-9]{0,9})')


def codex_home():
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").resolve()


def override_bytes():
    path = override_path()
    try:
        return path.read_bytes()
    except FileNotFoundError:
        if path.is_symlink():
            raise
        return None


def digest(raw):
    return hashlib.sha256(raw).hexdigest() if raw is not None else "missing"


def report_drift(record):
    if "codex_override_hash" not in record:
        return
    try:
        current = digest(override_bytes())
    except OSError as exc:
        print("kk: cannot check override changes at {}: {}".format(override_path(), exc), file=sys.stderr)
        return
    if record["codex_override_hash"] != current:
        print("kk: Codex overrides changed. Run kk apply to apply them.", file=sys.stderr)


def toml_value(value):
    """TOML basic strings, scalars, arrays and inline tables for JSON values."""
    if isinstance(value, dict):
        return "{ " + ", ".join(toml_value(k) + " = " + toml_value(v) for k, v in value.items()) + " }"
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(v) for v in value) + "]"
    if value is None:
        raise ValueError("Codex profile values cannot be null")
    return json.dumps(value, ensure_ascii=False, allow_nan=False).replace(chr(127), r"\u007f")


def toml_entries(table):
    return "".join(toml_value(k) + " = " + toml_value(v) + "\n" for k, v in table.items())


def matches_profile(actual, expected):
    if actual == expected:
        return True
    header = TIP_TABLE.encode()
    prefix = expected.partition(header)[0] + header
    if not actual.startswith(prefix):
        return False
    try:
        counters = actual[len(prefix):].decode("utf-8")
    except UnicodeDecodeError:
        return False
    models = set()
    for line in counters.split("\n"):
        if not line:
            continue
        entry = TIP_COUNTER.fullmatch(line)
        if not entry or int(entry[2]) > 2**32 - 1:
            return False
        model = entry[1].strip('"')
        if model in models:
            return False
        models.add(model)
    return True


def overlay(table, overrides):
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(table.get(key), dict):
            overlay(table[key], value)
        else:
            table[key] = value


def codex_settings(raw):
    try:
        config = object_value(json.loads(raw) if raw is not None else {}, str(override_path()))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid JSON in {}: {}".format(override_path(), exc)) from exc
    check_keys(config, ("claude", "codex", "launchNotice", "$schema"), str(override_path()))
    config = object_value(config.get("codex", {}), "codex")
    check_keys(config, ("settings", "optIn"), "codex")
    return config


def compose(release, config):
    baseline = payload.read_json(release / "kk/baseline/codex.json")
    selected = config.get("optIn", {})
    switches(selected, set(baseline["optIn"]) | {"nativeForbids"}, "codex.optIn")
    settings = object_value(config.get("settings", {}), "codex.settings")
    features = object_value(settings.get("features", {}), "codex.settings.features")
    plugins = object_value(settings.get("plugins", {}), "codex.settings.plugins")
    if ("hooks" in settings or {"hooks", "plugins"} & features.keys()
            or any(isinstance(plugin, dict) and "enabled" in plugin for plugin in plugins.values())):
        raise ValueError("configure hook and plugin enablement in native Codex configuration")
    if "developer_instructions" in settings:
        raise ValueError("kk composes developer_instructions; use confirmed AGENTS.md imports for extra text")
    profile = baseline["profile"]
    profile.update({k: v for k, v in baseline["optIn"].items() if selected.get(k)})
    overlay(profile, settings)
    rules = payload.read_json(release / "kodex-guard/scripts/guard/guard-rules.json")
    advisory = ("Protected files: reading paths matching these secrets globs is prohibited by policy: "
                + ", ".join(rules["secrets"]) + ". Ask the user for the needed value or a redacted copy.")
    instructions = "\n\n".join([p.read_text(encoding="utf-8").rstrip() for p in (
        release / "kk/baseline/codex/bootstrap.md", release / "klaude-plugin/instructions/behavior.md"
    )] + [advisory]) + "\n"
    profile["developer_instructions"] = instructions
    # Inline TUI tables get reformatted by Codex on the first interactive
    # launch. Emit a regular table last so its model-tip counters append cleanly.
    tui = object_value(profile.pop("tui"), "codex.settings.tui")
    tips = None
    if "model_availability_nux" in tui:
        tips = object_value(tui.pop("model_availability_nux"), "codex.settings.tui.model_availability_nux")
    rendered = toml_entries(profile) + "\n[tui]\n" + toml_entries(tui)
    if tips is not None:
        rendered += TIP_TABLE + toml_entries(tips)
    return rendered.encode(), instructions.encode(), selected.get("nativeForbids", False)


def validate_files(release, directory, profile, rules, executable):
    # An isolated working directory avoids a trusted project's config masking
    # candidate errors. Retain base user configuration (e.g. custom providers).
    with tempfile.TemporaryDirectory(prefix="kk-codex-check-") as temp:
        scratch = Path(temp)
        base = directory / "config.toml"
        if base.exists():
            (scratch / "config.toml").symlink_to(base)
        (scratch / "kk.config.toml").write_bytes(profile)
        env = dict(os.environ, CODEX_HOME=str(scratch))
        def run(args, capture=False):
            result = subprocess.run([executable] + args, cwd=scratch, env=env, stdin=subprocess.DEVNULL,
                                    stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                                    stderr=subprocess.PIPE, text=True, timeout=30)
            if result.returncode:
                raise ValueError("Codex rejected {}: {}".format(" ".join(args), result.stderr.strip()))
            return result.stdout
        run(["--profile", "kk", "debug", "prompt-input"])
        if rules is None:
            return
        candidate = scratch / "kk.rules"
        candidate.write_bytes(rules)
        command = ["execpolicy", "check", "--rules", str(candidate)]
        declaration = payload.read_json(release / "kodex-guard/scripts/guard/guard-rules.json")
        for category in declaration["destructive"].values():
            for rule in category:
                for native in rule.get("codex", []):
                    for example in native["match"]:
                        decision = json.loads(run(command + ["--"] + shlex.split(example), True))
                        if not isinstance(decision, dict) or decision.get("decision") != "forbidden":
                            raise ValueError("candidate kk.rules does not forbid " + example)
        for path in sorted((directory / "rules").glob("*.rules")):
            if path.name != "kk.rules":
                command.extend(["--rules", str(path)])
        run(command + ["--", "echo", "ok"])


def check_destinations(paths, owned):
    for path in paths:
        if path.parent.resolve() != path.parent:
            raise ValueError("install directory is a symlink: {}".format(path.parent))
        if os.path.lexists(path) and (str(path) not in owned or path.is_symlink() or not path.is_file()):
            raise ValueError("install path already exists: {}".format(path))


def prepare(release, record, *, required=False, snapshot=...):
    executable = shutil.which("codex")
    if not executable and snapshot is ...:
        if required or record.get("codex_paths"):
            raise ValueError("codex executable not found on PATH")
        return None
    if snapshot is not ...:
        saved = snapshot
        if saved is None:
            return {}, [Path(p) for p in record.get("codex_paths", [])], None, None
        directory = Path(saved["directory"])
    else:
        directory = codex_home()
        raw = override_bytes()
        saved = {"directory": str(directory), "settings": codex_settings(raw), "override_hash": digest(raw)}
    profile, instructions, native = compose(release, saved["settings"])
    files = {directory / "kk.config.toml": profile}
    agents = release / "kk/baseline/codex/agents"
    for agent in sorted(agents.iterdir()):
        if agent.suffix == ".toml":
            files[directory / "agents" / ("kk-" + agent.name)] = agent.read_bytes()
    rules = None
    if native:
        rules = (release / "kk/baseline/codex/kk.rules").read_bytes()
        files[directory / "rules/kk.rules"] = rules
    obsolete = [Path(p) for p in record.get("codex_paths", []) if Path(p) not in files]
    if any(str(path) not in record["installed_paths"] for path in obsolete):
        raise ValueError("inconsistent Codex installed-paths record")
    check_destinations(list(files) + obsolete, record["installed_paths"])
    # The target's immutable payload and saved overrides reproduce its validated
    # files. A broken vendor CLI must not strand recovery of the Claude release.
    if snapshot is ...:
        validate_files(release, directory, profile, rules, str(Path(executable).absolute()))
    return files, obsolete, instructions, saved


def prepare_activation(release, record):
    candidate = record["candidate"]
    home = release.parent.parent
    if candidate["phase"] == "activating" and "codex_inputs" in candidate:
        saved = candidate["codex_inputs"]
        mixed.check_claude_pilot(home)
        mixed.check_codex_pilot(home, record, saved["directory"] if saved else None)
        return None if saved is None else prepare(release, record, snapshot=saved)
    plan = prepare(release, record)
    if plan:
        directory = Path(plan[3]["directory"])
        # A previous release's staging code may predate guard stamping. Its
        # preflight runs here before the private staging directory is placed.
        if not candidate.get("codex_guard_staged") and release.parent.name == "staging":
            codex_plugins.stage_guard(release, record, directory, "local" in candidate["source"])
            candidate["digest"] = payload.fingerprint(release)
            candidate["codex_guard_staged"] = True
        previous = candidate.get("confirmed_guard_change")
        codex_plugins.confirm_change(record, release, directory)
        if candidate.get("confirmed_guard_change") != previous:
            # A pilot still has its working guard here. A confirmed switch may
            # pause for vendor cleanup; resuming the same change needs no new consent.
            state.write_json(home / "state.json", record)
    mixed.check_claude_pilot(home)
    mixed.check_codex_pilot(home, record, plan[3]["directory"] if plan else None)
    # The place checkpoint persists exactly the inputs validated at staging.
    candidate["codex_inputs"] = None if plan is None else plan[3]
    return plan


def reconcile_claim(home, record):
    """Finish or relinquish an interrupted create-only publication under the writer lock."""
    claim = record.get("codex_claim")
    if not claim:
        return
    path = Path(claim["path"])
    temporary = Path(claim["temporary"])
    if temporary.parent != path.parent or path.parent.resolve() != path.parent:
        raise ValueError("cannot recover Codex destination in a replaced directory: {}".format(path))
    try:
        info = temporary.lstat()
    except FileNotFoundError:
        if "linked" not in claim:
            raise ValueError("missing Codex publication evidence: {}".format(temporary))
    else:
        if [info.st_dev, info.st_ino] != claim["identity"]:
            raise ValueError("Codex publication temporary file was replaced: {}".format(temporary))
        if "linked" not in claim:
            try:
                destination = path.lstat()
                linked = os.path.samestat(info, destination)
            except FileNotFoundError:
                linked = False
            if not linked:
                record["installed_paths"].remove(str(path))
                record["codex_paths"].remove(str(path))
            claim["linked"] = linked
            state.write_json(home / "state.json", record)
        temporary.unlink()
    del record["codex_claim"]
    state.write_json(home / "state.json", record)


def publish_new(home, record, path, data):
    # Keep the source inode until the ownership decision is durable. On retry,
    # a file someone else created after our reservation remains theirs.
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".kk-", delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
            info = os.fstat(stream.fileno())
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    # Once journal publication starts we may already have committed the claim,
    # even if the write raises. Recovery must still have its proof inode.
    record["codex_claim"] = {"path": str(path), "temporary": str(temporary),
                             "identity": [info.st_dev, info.st_ino]}
    record["installed_paths"].append(str(path))
    record["codex_paths"].append(str(path))
    state.write_json(home / "state.json", record)
    try:
        os.link(temporary, path)
    finally:
        reconcile_claim(home, record)


def publish(home, record, version, plan):
    if plan is None:
        return
    files, obsolete, instructions, saved = plan
    if any(str(path) not in record["installed_paths"] for path in obsolete):
        raise ValueError("inconsistent Codex installed-paths record")
    check_destinations(list(files) + obsolete, record["installed_paths"])
    record["codex_write_pending"] = True
    state.write_json(home / "state.json", record)
    record.setdefault("codex_paths", [])
    for path, data in files.items():
        if str(path) in record["installed_paths"]:
            state.atomic_write(path, data)
        else:
            publish_new(home, record, path, data)
    for path in obsolete:
        path.unlink(missing_ok=True)
        record["installed_paths"].remove(str(path))
    sidecar = home / "codex-instructions.md"
    release_state = record["releases"].setdefault(version, {})
    if saved is None:
        sidecar.unlink(missing_ok=True)
        record.pop("codex_override_hash", None)
        release_state.setdefault("tools", {}).pop("codex", None)
    else:
        state.atomic_write(sidecar, instructions)
        record["codex_override_hash"] = saved["override_hash"]
        release_state["codex_snapshot"] = saved
        release_state.setdefault("tools", {}).setdefault("codex", "awaiting review")
    if any(path.name == "kk.rules" for path in files) and not record.get("codex_rules_announced"):
        print("kk: native forbids now affect every Codex session on this account, including bare Codex and temporary cleanup.")
        record["codex_rules_announced"] = True
    record["codex_paths"] = sorted(str(p) for p in files)
    del record["codex_write_pending"]
    state.write_json(home / "state.json", record)
