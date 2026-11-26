"""Compose Claude's per-launch settings from the selected release and adopter inputs."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from typing import Iterable, Iterator, List, Optional, Set, Tuple
from uuid import uuid4

from . import notice, payload, state
from .claude import OTHER_PLUGINS, settings_report
from .payload import JSONObject, is_array, is_object


PERMISSION_LISTS = ("allow", "ask", "deny", "additionalDirectories")


def object_value(value: object, label: str) -> JSONObject:
    if not is_object(value):
        raise ValueError("{} must be a JSON object".format(label))
    return value


def json_file(path: Path, *, optional: bool = False) -> JSONObject:
    try:
        return object_value(payload.read_json(path), str(path))
    except FileNotFoundError:
        if optional and not path.is_symlink():
            return {}
        raise
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid JSON in {}: {}".format(path, exc)) from exc


def check_keys(obj: JSONObject, keys: Iterable[str], label: str) -> None:
    unknown = obj.keys() - set(keys)
    if unknown:
        raise ValueError("unknown {} key: {}".format(label, sorted(unknown)[0]))


def switches(obj: object, keys: Iterable[str], label: str) -> None:
    table = object_value(obj, label)
    check_keys(table, keys, label)
    for key, value in table.items():
        if not isinstance(value, bool):
            raise ValueError("{}.{} must be a boolean".format(label, key))


def read_overrides(path: Path, baseline: JSONObject) -> JSONObject:
    config = json_file(path, optional=True)
    check_keys(config, ("claude", "codex", "launchNotice", "$schema"), str(path))
    if not isinstance(config.get("launchNotice", True), bool):
        raise ValueError("launchNotice must be a boolean")
    object_value(config.get("codex", {}), "codex")
    config = object_value(config.get("claude", {}), "claude")
    check_keys(config, ("instructions", "defaults", "optIn", "settings", "settingsFile"), "claude")
    if not isinstance(config.get("instructions", True), bool):
        raise ValueError("claude.instructions must be a boolean")
    defaults = set(baseline["preferences"]) | baseline["defaultAllows"].keys() | {"statusLine"}
    switches(config.get("defaults", {}), defaults, "claude.defaults")
    switches(config.get("optIn", {}), baseline["optIn"], "claude.optIn")
    if "settingsFile" in config and not (isinstance(config["settingsFile"], str) and config["settingsFile"].strip()):
        raise ValueError("claude.settingsFile must name a file")
    return config


def local_settings_paths(cwd: Path) -> Iterator[Path]:
    """Claude also reads the main checkout's local settings when launched below it."""
    yield cwd / ".claude/settings.local.json"
    if shutil.which("git") is None:
        return
    common = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=cwd,
                            capture_output=True, text=True)
    if common.returncode:
        return
    git_dir = (cwd / common.stdout.rstrip("\n")).resolve()
    root = git_dir.parent
    if git_dir.name != ".git" or root in (cwd, Path.home().resolve()):
        return
    if any(p.lstat().st_uid != os.getuid() for p in (root, git_dir, root / ".claude") if p.exists()):
        return
    yield root / ".claude/settings.local.json"


def file_rule(rule: str, directory: Path) -> str:
    """Keep file-anchored Read/Edit rules at their source after moving the flag file."""
    match = re.fullmatch(r"(Read|Edit|Write|NotebookEdit)\(/((?!/).*)\)", rule)
    if match:
        tool, pattern = match.groups()
        return "{}(/{}/{})".format(tool, literal_path(directory).rstrip("/"), pattern)
    return rule


def literal_path(path: object) -> str:
    return re.sub(r"([\\*?\[\]])", r"\\\1", str(path))


def string_list(value: object, label: str) -> List[str]:
    if not is_array(value) or not all(isinstance(entry, str) for entry in value):
        raise ValueError("{} must be an array of strings".format(label))
    return value


def overlay(layer: JSONObject, settings: object, label: str, directory: Path) -> None:
    settings = object_value(settings, label)
    if "effortLevel" in settings:
        # A later global effort replaces earlier per-model effort choices.
        for model in layer.get("modelSettings", {}).values():
            model.pop("effortLevel", None)
    for key, value in settings.items():
        if key == "permissions":
            permissions = layer["permissions"]
            for name, entries in object_value(value, label + ".permissions").items():
                if name in PERMISSION_LISTS:
                    entries = string_list(entries, label + ".permissions." + name)
                    if name != "additionalDirectories":
                        entries = [file_rule(entry, directory) for entry in entries]
                    combined = permissions.get(name, []) + entries
                    # Negations in ask/deny make the order of repeated rules significant.
                    permissions[name] = combined if name in ("ask", "deny") else list(dict.fromkeys(combined))
                else:
                    permissions[name] = entries
        elif key == "modelSettings":
            models = layer.setdefault(key, {})
            for model, options in object_value(value, label + ".modelSettings").items():
                models.setdefault(model, {}).update(object_value(options, label + ".modelSettings." + model))
        elif key in ("env", "enabledPlugins"):
            values = object_value(value, label + "." + key)
            if key == "env" and not all(isinstance(v, str) for v in values.values()):
                raise ValueError(label + ".env values must be strings")
            layer.setdefault(key, {}).update(values)
        else:
            layer[key] = value


def baseline_layer(release: Path, baseline: JSONObject, config: JSONObject, existing: List[JSONObject]) -> JSONObject:
    defaults = config.get("defaults", {})
    layer: JSONObject = {k: v for k, v in baseline["preferences"].items()
             if k != "env" and defaults.get(k, True) and all(k not in s for s in existing)}
    if "effortLevel" in layer:
        # A flag-level global effort shadows even a lower per-model effort.
        # Carry only those choices forward; every other model uses the baseline.
        for settings in existing:
            for model, options in object_value(settings.get("modelSettings", {}), "modelSettings").items():
                if is_object(options) and options.get("effortLevel") in ("low", "medium", "high", "xhigh"):
                    layer.setdefault("modelSettings", {})[model] = {"effortLevel": options["effortLevel"]}
    if defaults.get("env", True):
        env = {k: v for k, v in baseline["preferences"]["env"].items()
               if all(k not in object_value(s.get("env", {}), "Claude env") for s in existing)}
        if env:
            layer["env"] = env
    if defaults.get("statusLine", True) and all("statusLine" not in s for s in existing):
        script = shlex.quote(str(release / baseline["statusLine"]))
        layer["statusLine"] = {"type": "command", "command": "bash " + script}
    allows = [entry.format(release=literal_path(release)) for name, entry in baseline["defaultAllows"].items()
              if defaults.get(name, True)]
    allows.extend(entry for name, entry in baseline["optIn"].items() if config.get("optIn", {}).get(name))
    layer["permissions"] = {"allow": allows}
    return layer


def compose(release: Path, arguments: List[str], sources: Set[str]) -> Tuple[JSONObject, bool]:
    cwd = Path.cwd()
    config_file = state.override_path()
    claude_dir = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")
    baseline_dir = release / "kk/baseline"
    baseline = json_file(baseline_dir / "claude.json")
    config = read_overrides(config_file, baseline)
    paths: List[Path] = []
    if "user" in sources:
        paths.append(claude_dir / "settings.json")
    if "project" in sources:
        paths.append(cwd / ".claude/settings.json")
    if "local" in sources:
        paths.extend(local_settings_paths(cwd))
    existing = [json_file(path, optional=True) for path in dict.fromkeys(paths)]
    layer = baseline_layer(release, baseline, config, existing)
    for settings in existing:
        enabled = object_value(settings.get("enabledPlugins", {}), "enabledPlugins")
        for plugin in OTHER_PLUGINS:
            if enabled.get(plugin):
                layer.setdefault("enabledPlugins", {})[plugin] = False
    overlay(layer, config.get("settings", {}), "claude.settings", config_file.parent)
    if "settingsFile" in config:
        path = config_file.parent / Path(config["settingsFile"]).expanduser()
        overlay(layer, json_file(path), str(path), path.absolute().parent)
    for argument in arguments:
        if argument.lstrip().startswith("{"):
            try:
                inline = json.loads(argument)
            except json.JSONDecodeError as exc:
                raise ValueError("invalid --settings JSON: {}".format(exc)) from exc
            overlay(layer, inline, "--settings", cwd)
        else:
            path = Path(argument).absolute()
            overlay(layer, json_file(path), str(path), path.parent)

    # Read negations only carve out earlier rules from the same settings source.
    # Keep generated denies last even when the adopter supplied a duplicate.
    denies = string_list(payload.read_json(baseline_dir / "claude/deny.json"), "release denies")
    layer["permissions"]["deny"] = [d for d in layer["permissions"].get("deny", []) if d not in denies] + denies
    needs_validation = bool(arguments or config.get("settings") or "settingsFile" in config or "modelSettings" in layer)
    return layer, needs_validation


def validate_settings(claude: Path, path: Path, layer: JSONObject) -> None:
    """Ask this Claude binary whether it accepted the flag file, without a model turn."""
    with tempfile.TemporaryDirectory(prefix="kk-claude-validate-") as scratch:
        env = dict(PATH=os.environ["PATH"], HOME=scratch, CLAUDE_CONFIG_DIR=scratch,
                   CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1", DISABLE_AUTOUPDATER="1")
        code, report = settings_report(claude, scratch, env, "", "--settings", str(path))
    for error in report.get("errors", []):
        if error.get("file") == str(path):
            raise ValueError("invalid composed Claude settings at {} (check claude.settings, settingsFile or --settings)"
                             .format(error.get("path") or "root"))
    for source in report.get("sources", []):
        if source["source"] == "flagSettings" and code == 0:
            accepted = source["settings"]
            if "effortLevel" in layer and accepted.get("effortLevel") != layer["effortLevel"]:
                raise ValueError("invalid effortLevel in composed Claude settings")
            if accepted.get("permissions", {}).get("deny") == layer["permissions"]["deny"]:
                return
    raise ValueError("Claude could not confirm the composed --settings deny list")


def session_file(home: Path, layer: JSONObject) -> Path:
    directory = home / "claude-layers"
    directory.mkdir(mode=0o700, exist_ok=True)
    # The launcher execs Claude, so its PID owns the layer for the session.
    # Reap completed sessions on the next launch. A nonce protects PID reuse
    # when two launchers clean up concurrently.
    for path in directory.glob("*.json"):
        match = re.fullmatch(r"([1-9][0-9]{0,9})-[0-9a-f]{32}\.json", path.name)
        if match:
            try:
                os.kill(int(match[1]), 0)
            except ProcessLookupError:
                path.unlink(missing_ok=True)
            except (PermissionError, OverflowError):
                continue
    path = directory / "{}-{}.json".format(os.getpid(), uuid4().hex)
    data = (json.dumps(layer, indent=2, allow_nan=False) + "\n").encode()
    state.atomic_write(path, data)
    return path


def launch(home: Path, argv: List[str]) -> None:
    settings: List[str] = []
    forwarded: List[str] = []
    sources = {"user", "project", "local"}
    restricted = False
    print_layer = False
    args = iter(argv)
    for arg in args:
        if arg == "--":
            forwarded.extend([arg, *args])
            break
        if arg == "--print-layer":
            print_layer = True
        elif arg == "--setting-sources" or arg.startswith("--setting-sources="):
            value: Optional[str] = next(args, None) if arg == "--setting-sources" else arg.partition("=")[2]
            if value is None:
                raise ValueError("--setting-sources requires a list of sources")
            sources = {s.strip() for s in value.split(",") if s.strip()}
            forwarded.extend(["--setting-sources", value])
        elif arg == "--settings" or arg.startswith("--settings="):
            value = next(args, None) if arg == "--settings" else arg.partition("=")[2]
            if not value:
                raise ValueError("--settings requires a file or JSON object")
            settings.append(value)
        else:
            if arg == "--restricted":
                restricted = True
            forwarded.append(arg)

    record = state.load(home)
    if not record["active"]:
        raise ValueError("no active release; finish installing kk first")
    release = home / "releases" / payload.release_id(record["active"])
    if release.resolve() != Path(__file__).resolve().parents[2]:
        raise ValueError("active release changed; rerun kk claude")
    candidate: JSONObject = record["candidate"] or {}
    if candidate.get("phase") == "activating":
        print("kk: activation in progress; Claude's plugin may differ from the active release", file=sys.stderr)
    layer, needs_validation = compose(release, settings, set() if restricted else sources)
    if print_layer and not needs_validation:
        print(json.dumps(layer, indent=2, allow_nan=False))
        return
    executable = shutil.which("claude")
    if executable is None:
        raise ValueError("claude executable not found on PATH")
    claude = Path(executable).absolute()
    path = session_file(home, layer)
    try:
        if needs_validation:
            validate_settings(claude, path, layer)
        if print_layer:
            print(json.dumps(layer, indent=2, allow_nan=False))
            return
        # Hooks can run after a cwd change. Preserve the homes selected at launch.
        env = dict(os.environ, KK_HOME=str(home))
        for key in ("XDG_CONFIG_HOME", "CODEX_HOME"):
            value = env.get(key)
            if value and not os.path.isabs(value):
                env[key] = os.path.join(os.getcwd(), value)
        if "-p" not in forwarded and "--print" not in forwarded:
            notice.on_launch(home, record)
        if sys.stderr is not None:
            sys.stderr.flush()
        os.execve(claude, ["claude", "--settings", str(path), *forwarded], env)
    finally:
        path.unlink(missing_ok=True)  # Preview, validation failure, or failed exec.
