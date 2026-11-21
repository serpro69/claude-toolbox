"""Launch Codex with the managed profile and repository-confirmed instructions."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from contextlib import ExitStack

from . import codex_plugins, codex_profile, codex_trust, payload, state


ARG_LIMIT = 122880  # Linux per-argument limit less 8 KiB, including TOML escaping.
VALUE_OPTIONS = {
    "-c", "--config", "-i", "--image", "-m", "--model", "-p", "--profile", "-s", "--sandbox",
    "-C", "--cd", "-a", "--ask-for-approval", "--enable", "--disable", "--remote",
    "--remote-auth-token-env", "--local-provider", "--add-dir", "--thread-source",
    "--cyber-access-program", "--output-schema", "--color", "-o", "--output-last-message",
}


def display(value):
    return json.dumps(str(value), ensure_ascii=True)


def launch_options(args):
    directory = Path.cwd()
    profile = command = None
    trust_flags = []
    dynamic_workspace = False
    it = iter(args)
    for arg in it:
        if arg == "--":
            break
        key, separator, value = arg.partition("=")
        if len(arg) > 2 and arg[:2] in VALUE_OPTIONS:
            key, separator, value = arg[:2], "attached", arg[2:]
            if value.startswith("="):
                value = value[1:]
        if key in VALUE_OPTIONS:
            if not separator:
                value = next(it, None)
            if value is None or (key in ("-C", "--cd", "-p", "--profile") and not value):
                raise ValueError("{} requires a value".format(key))
            if key in ("-C", "--cd"):
                directory = Path.cwd() / value
            elif key in ("-p", "--profile"):
                profile = value
            elif key == "--remote":
                dynamic_workspace = True
            elif key in ("-c", "--config", "--enable", "--disable"):
                trust_flags.extend([key, value])
        elif arg == "--worktree":
            dynamic_workspace = True
        elif command is None and not arg.startswith("-"):
            command = arg
            dynamic_workspace = dynamic_workspace or command in ("resume", "fork", "agents")
        elif command in ("exec", "e") and arg in ("resume", "fork"):
            dynamic_workspace = True
    return None if dynamic_workspace else directory.resolve(), profile, command in ("exec", "e", "review"), trust_flags


def workspace_root(directory):
    env = {k: v for k, v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR")}
    result = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=directory,
                            env=dict(env, LC_ALL="C"), capture_output=True)
    if result.returncode == 0:
        return Path(os.fsdecode(result.stdout[:-1])).resolve()  # Git adds one line terminator.
    if result.stderr.startswith(b"fatal: not a git repository"):
        return directory
    raise ValueError("cannot resolve Codex workspace: " + display(os.fsdecode(result.stderr).strip()))


def import_workspace(directory):
    try:
        return workspace_root(directory)
    except (OSError, ValueError) as exc:
        print("kk: cannot determine workspace for repository imports: " + display(exc), file=sys.stderr)
        return None


def import_policy(root):
    """Use the release guard's secret rules for reads performed by the launcher."""
    engine = Path(__file__).resolve().parents[2] / "kodex-guard/scripts/guard/guard.py"
    spec = importlib.util.spec_from_file_location("_kk_import_guard", engine)
    guard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guard)
    env = dict(os.environ, KK_GUARD_PROJECT_ROOT=str(root))
    try:
        ctx = guard.context_from_payload({"tool_name": "Read", "tool_input": {}, "cwd": str(root)}, env)
        policy, messages = guard.effective_policy(guard.load_rules(guard.default_rules_path()), ctx, env)
    except guard.Denied as exc:
        raise ValueError(exc.reason()) from exc
    for message in messages:
        print("kk: " + display(message), file=sys.stderr)
    return lambda paths: guard.secrets_match(paths, policy)


def read_inside(root, path, protected, limit=None):
    """Open the resolved in-repo file without following a substituted symlink."""
    relative = path.resolve(strict=True).relative_to(root)
    if protected((os.path.normpath(path), str(root / relative))):
        raise ValueError("path is protected by the guard")
    if not relative.parts:
        raise ValueError("expected a file")
    with ExitStack() as stack:
        directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        stack.callback(os.close, directory)
        for part in relative.parts[:-1]:
            directory = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            stack.callback(os.close, directory)
        fd = os.open(relative.name, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW, dir_fd=directory)
        with os.fdopen(fd, "rb") as stream:
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                raise ValueError("expected a regular file")
            return stream.read() if limit is None else stream.read(limit)


def import_names(root, protected):
    agents = root / "AGENTS.md"
    try:
        content = read_inside(root, agents, protected).decode("utf-8")
    except FileNotFoundError:
        return []
    except (ValueError, RuntimeError, OSError) as exc:
        print("kk: skipped AGENTS.md ({})".format(display(exc)), file=sys.stderr)
        return []
    fence = ""
    names = []
    for line in content.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1].startswith(fence) and not marker[2].strip():
                fence = ""
        elif marker:
            fence = marker[1]
        elif re.match(r"^ {0,3}@\S", line):
            name = line.lstrip()[1:].strip()
            if name not in names:
                names.append(name)
    return names


def import_record(home, root):
    key = hashlib.sha256(os.fsencode(root)).hexdigest()
    return home / "imports" / (key + ".json")


def saved_consent(path, names):
    try:
        entry = payload.read_json(path)
    except FileNotFoundError:
        return None
    if not isinstance(entry, dict) or type(entry.get("approved")) is not bool:
        raise ValueError("invalid import decision in {}".format(path))
    return entry["approved"] if entry.get("paths") == sorted(names) else None


def eligible_imports(root, protected):
    sizes = {}
    for name in import_names(root, protected):
        try:
            if Path(name).is_absolute():
                raise ValueError("expected a repository-relative path")
            path = (root / name).resolve(strict=True)
            path.relative_to(root)
            if protected((os.path.normpath(root / name), str(path))):
                raise ValueError("path is protected by the guard")
            info = path.stat()
            if not stat.S_ISREG(info.st_mode):
                raise ValueError("expected a regular file")
            sizes[name] = info.st_size
        except (OSError, RuntimeError, ValueError) as exc:
            print("kk: skipped import {} ({})".format(display(name), display(exc)), file=sys.stderr)
    return sizes


def import_argument(home, root, interactive):
    if not (root / "AGENTS.md").exists():
        return []
    protected = import_policy(root)
    sizes = eligible_imports(root, protected)
    if not sizes:
        return []
    path = import_record(home, root)
    approved = saved_consent(path, sizes)
    if approved is None and interactive:
        print("Inject these files alongside toolbox instructions? This replaces any repository "
              "developer_instructions for this session.", file=sys.stderr)
        for name, size in sizes.items():
            print("  {} ({} bytes)".format(display(name), size), file=sys.stderr)
        print("Approve imports for {}? Your answer is remembered for this list. [y/N] ".format(display(root)),
              file=sys.stderr, end="", flush=True)
        approved = sys.stdin.readline().strip().lower() in ("y", "yes")
        state.write_json(path, {"root": str(root), "paths": sorted(sizes), "approved": approved})
    if not approved:
        if not interactive:
            print("kk: repository imports were not injected (no stored approval for this list).", file=sys.stderr)
        return []
    text = (home / "codex-instructions.md").read_text(encoding="utf-8")
    argument = None
    for name, size in sizes.items():
        try:
            if size > ARG_LIMIT:
                raise ValueError("exceeds the import argument limit")
            data = read_inside(root, root / name, protected, ARG_LIMIT + 1).decode("utf-8")
            extended = text + "\n\n# " + name + "\n\n" + data
            candidate = "developer_instructions=" + codex_profile.toml_value(extended)
            if len(candidate.encode()) > ARG_LIMIT:
                raise ValueError("exceeds the import argument limit")
            argument, text = candidate, extended
        except (OSError, RuntimeError, ValueError) as exc:
            print("kk: skipped import {} ({})".format(display(name), display(exc)), file=sys.stderr)
    return ["-c", argument] if argument is not None else []


def report_imports(home):
    root = import_workspace(Path.cwd().resolve())
    if root is None:
        return
    path = import_record(home, root)
    names = eligible_imports(root, import_policy(root)) if (root / "AGENTS.md").exists() else {}
    if names or path.exists():
        answer = saved_consent(path, names)
        print("Codex imports: {} ({})".format({True: "approved", False: "declined", None: "undecided"}[answer], path))


def launch(home, args):
    directory, explicit, batch, trust_flags = launch_options(args)
    record = state.load(home)
    if (record.get("candidate") or {}).get("phase") == "activating" or record.get("codex_write_pending"):
        raise ValueError("Codex files are changing; finish kk apply, upgrade or rollback before launching")
    active = record["active"]
    if not active:
        raise ValueError("no active release; finish installing kk first")
    if Path(__file__).resolve().parents[2] != (home / "releases" / payload.release_id(active)).resolve():
        raise ValueError("active release changed; rerun kk codex")
    saved = record["releases"][active]
    phase = saved.get("tools", {}).get("codex")
    if phase not in ("ready", "unverified", "awaiting review"):
        raise ValueError("Codex is not configured for the active release; " + codex_plugins.activation_hint(saved))
    executable = codex_plugins.executable()
    if batch:
        if directory is None or explicit not in (None, "kk"):
            raise ValueError("cannot verify the Codex guard for this session's workspace or named profile; "
                             "use an interactive session or select a local directory with the kk profile")
        release = home / "releases" / active
        codex_home = codex_profile.codex_home()
        profile = codex_home / "kk.config.toml"
        snapshot = saved["codex_snapshot"]
        if (str(codex_home) != snapshot["directory"] or profile.is_symlink() or not profile.is_file()
                or profile.read_bytes() != codex_profile.compose(release, snapshot["settings"])[0]):
            raise ValueError("cannot verify the managed Codex profile in this CODEX_HOME; run kk apply")
        if not codex_plugins.receipt(record, codex_home, "kk-guard"):
            raise ValueError("Codex guard is not installed in this CODEX_HOME; " + codex_plugins.activation_hint(saved))
        phase, issues = codex_trust.check(release, codex_home, directory, trust_flags,
                                          acknowledged=phase == "unverified", executable=executable)
        if phase == "awaiting review":
            raise ValueError("Codex guard awaiting review for {}: {}".format(display(directory), "; ".join(issues)))
        if phase == "unverified":
            print("kk: Codex guard is unverified for this run.", file=sys.stderr)
    elif not codex_plugins.receipt(record, codex_profile.codex_home(), "kk-guard"):
        print("kk: Codex guard is not installed in this CODEX_HOME; " + codex_plugins.activation_hint(saved),
              file=sys.stderr)
    codex_profile.report_drift(record)
    flags = []
    if explicit is None:
        profile_path = codex_profile.codex_home() / "kk.config.toml"
        if str(profile_path) not in record.get("codex_paths", []) or not profile_path.is_file() or profile_path.is_symlink():
            raise ValueError("managed profile is missing from this CODEX_HOME; run kk apply")
        flags = ["--profile", "kk"]
        if directory is None:
            print("kk: skipping repository imports because Codex selects the session workspace.", file=sys.stderr)
        else:
            root = import_workspace(directory)
            if root is not None:
                flags += import_argument(home, root, sys.stdin.isatty() and not batch)
    env = dict(os.environ, CODEX_HOME=str(codex_profile.codex_home()), KK_HOME=str(home))
    if env.get("XDG_CONFIG_HOME"):
        env["XDG_CONFIG_HOME"] = str(Path(env["XDG_CONFIG_HOME"]).absolute())
    os.execve(executable, ["codex", *flags, *args], env)
