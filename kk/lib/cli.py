"""Release staging, activation and offline recovery under one writer lock."""

import argparse
import hashlib
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile

from . import claude, claude_launch, codex_launch, codex_plugins, codex_profile, codex_trust, payload, state, validation
from . import live, migrate, mixed, notice
from .run import load_cli


def entry_link():
    return Path.home() / ".local/bin/kk"


def check_link(home, record):
    link = entry_link()
    if (home / "bin").is_symlink():
        raise ValueError("toolbox bin directory is a symlink: {}".format(home / "bin"))
    if os.path.lexists(link):
        if str(link) not in record["installed_paths"] or not link.is_symlink():
            raise ValueError("install path already exists: {}".format(link))
        destination = link.parent / os.readlink(link)
        # Check this link's destination. The stable dispatcher at that path
        # may itself be broken and is precisely what rollback must replace.
        if destination.parent.resolve() / destination.name != home / "bin/kk":
            raise ValueError("install path already exists: {}".format(link))


def recovery_command(home, version):
    return shlex.quote(str(home / "releases" / payload.release_id(version) / "kk/bin/kk")) + " rollback"


def entry_digest(path):
    if not path.is_symlink() and path.is_file() and os.access(path, os.R_OK | os.X_OK):
        return hashlib.sha256(path.read_bytes()).hexdigest()
    return None


def complete_publication(home, record):
    """A promoted release can finish publishing its dispatcher after a crash."""
    version = payload.release_id(record["pending_entry"])
    if version != record["active"]:
        raise ValueError("journaled dispatcher does not belong to the active release")
    expected = record["pending_entry_sha256"]
    draft = home / "bin/.kk-next"
    entry = home / "bin/kk"
    if not isinstance(expected, str) or len(expected) != 64:
        raise ValueError("invalid journaled dispatcher digest")
    if entry_digest(entry) != expected:
        if entry_digest(draft) != expected:
            wanted = (home / "releases" / version / "kk/bin/kk").read_bytes()
            if hashlib.sha256(wanted).hexdigest() != expected:
                raise ValueError("dispatcher bytes differ from the validated release; run kk rollback")
            state.atomic_write(draft, wanted, mode=0o755)
        os.replace(draft, entry)
    draft.unlink(missing_ok=True)
    del record["pending_entry"]
    del record["pending_entry_sha256"]
    state.write_json(home / "state.json", record)


def finish_install(home, record, release, codex_plan=...):
    """Run in the release being activated, under the caller's writer lock."""
    check_link(home, record)
    # Pre-Task-9 active releases invoke this entry point without a prepared plan.
    if codex_plan is ...:
        codex_plan = codex_profile.prepare_activation(release, record)
    def checkpoint(step):
        state.checkpoint(home, record, step)

    claude.activate(home, release, checkpoint)
    if codex_plan is not None:
        snapshot = codex_plan[3]
        restoring = record["candidate"].get("operation") == "rollback"
        if snapshot is not None and not restoring:
            codex_plugins.activate(home, record, release, snapshot["directory"], checkpoint)
        checkpoint("codex-files")
        codex_profile.publish(home, record, release.name, codex_plan)
        if snapshot is not None:
            if restoring:
                # Recover the previously validated files even if the vendor
                # executable cannot yet reconcile different plugin bytes.
                codex_plugins.activate(home, record, release, snapshot["directory"], checkpoint)
            checkpoint("codex-trust")
            saved = record["releases"][release.name]
            phase, issues = codex_trust.machine(release, saved, prompt=not restoring)
            state.record_codex_phase(saved, phase)
            codex_trust.report(phase, issues)
    checkpoint("entry-point")
    entry = home / "bin/kk"
    draft = home / "bin/.kk-next"
    wanted = (release / "kk/bin/kk").read_bytes()
    expected = hashlib.sha256(wanted).hexdigest()
    publication_due = entry_digest(entry) != expected
    if publication_due:
        state.atomic_write(draft, wanted, mode=0o755)
        if not record["active"]:
            os.replace(draft, entry)
            publication_due = False
    link = entry_link()
    if str(link) not in record["installed_paths"]:
        record["installed_paths"].append(str(link))
    checkpoint("entry-link")
    link.parent.mkdir(parents=True, exist_ok=True)
    if not os.path.lexists(link):
        link.symlink_to(entry)  # Atomic create-only publication of the recorded path.
    check_link(home, record)
    checkpoint("promote")
    pending = record["candidate"]
    state.remember_candidate(record, pending)
    _, issues = mixed.inspect("claude", Path("/"))
    claude_phase = "awaiting review" if issues else "ready"
    state.promote(record, release.name, claude_phase)
    state.remember_placed(home, record, pending.get("abandoned"))
    if publication_due:
        record["pending_entry"] = release.name
        record["pending_entry_sha256"] = expected
    else:
        record.pop("pending_entry", None)
        record.pop("pending_entry_sha256", None)
    state.write_json(home / "state.json", record)
    print("Claude {}:".format(claude_phase), release.name)
    for issue in issues:
        print("  " + issue)
    if record["rollback_target"]:
        print("Recovery command:", recovery_command(home, record["rollback_target"]), flush=True)
    if publication_due:
        complete_publication(home, record)
    else:
        draft.unlink(missing_ok=True)
    state.prune(home, record)


def replace_pending(source, destination, work):
    """Replace only an unpromoted directory owned by this first installation."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        with tempfile.TemporaryDirectory(dir=work) as backup:
            destination.rename(Path(backup) / "previous")
            source.rename(destination)
    else:
        source.rename(destination)


def prepare(home, record, args, archive_file, work):
    candidate = record["candidate"]
    source = {"local": str(args.local.resolve())} if args.local else {
        "tag": args.version, "repository": os.environ.get("KK_REPOSITORY", "serpro69/claude-toolbox")}
    if candidate and not args.local and not args.version:
        source = candidate["source"]
    if record["active"] and candidate and candidate["phase"] == "activating" and source != candidate["source"]:
        raise ValueError("upgrade in progress; run kk upgrade without a source to resume, or kk status for recovery options")
    if candidate and source == candidate["source"]:
        version = payload.release_id(candidate["version"])
        stage = home / "staging" / version
        existing = stage if stage.is_dir() else home / "releases" / version
        try:
            payload.verify_saved(existing, candidate)
            validation.validate(existing)
        except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
            if record["active"] and candidate["phase"] == "activating":
                raise ValueError("cannot resume candidate {}; run kk rollback: {}".format(version, exc)) from exc
            print("kk: rebuilding incomplete candidate {}: {}".format(version, exc), file=sys.stderr)
        else:
            return version
    elif candidate:
        print("kk: staging the requested source in place of the pending candidate", file=sys.stderr)
    local = Path(source["local"]) if "local" in source else None
    if record["active"] and local is None:
        version = payload.tag_name(source["tag"]) if source["tag"] else payload.latest_tag(source["repository"])
        source["tag"] = version
        existing = record["releases"].get(version, {})
        if existing.get("source") == source:
            needs_codex = shutil.which("codex") and not codex_plugins.receipt(record, codex_profile.codex_home(), "kk-guard")
            if version == record["active"] and not needs_codex:
                print("Already active:", version)
                if record["rollback_target"]:
                    print("Recovery command:", recovery_command(home, record["rollback_target"]))
                state.prune(home, record)
                return None
            placed = home / "releases" / version
            payload.verify_saved(placed, existing)
            validation.validate(placed)
            record["candidate"] = {"version": version, "phase": "staged", "source": source,
                                   "digest_format": 2, "digest": payload.fingerprint(placed)}
            if version == record["active"]:
                record["candidate"]["operation"] = "add-codex"
            state.write_json(home / "state.json", record)
            return version
    with tempfile.TemporaryDirectory(dir=work) as temp:
        stage = Path(temp) / "payload"
        stage.mkdir()
        version = payload.stage(stage, local, source.get("tag"), archive_file, source.get("repository"))
        if local is None:
            source["tag"] = version
        placed = home / "releases" / version
        if placed.exists() and (record["active"] or not (
                candidate and candidate["version"] == version and candidate["source"] == source)):
            raise ValueError("retained release {} already occupies {}; choose a different tag or --local".format(
                version, placed))
        codex_plugins.stage_guard(stage, record, codex_profile.codex_home(), local is not None)
        validation.validate(stage)
        digest = payload.fingerprint(stage)
        reader_hash = hashlib.sha256((stage / "kk/lib/payload.py").read_bytes()).hexdigest()
        replace_pending(stage, home / "staging" / version, work)
    if candidate and candidate["version"] != version and (home / "releases" / payload.release_id(candidate["version"])).is_dir():
        state.remember_candidate(record, candidate)
    record["candidate"] = {"version": version, "phase": "staged", "source": source,
                           "digest_format": 2, "digest": digest, "reader_sha256": reader_hash,
                           "codex_guard_staged": True}
    state.write_json(home / "state.json", record)
    return version


def install_locked(home, args, archive_file=None):
    record = state.load(home)
    codex_profile.reconcile_claim(home, record)
    if record.get("pending_entry"):
        check_link(home, record)
        complete_publication(home, record)
        print("Published dispatcher for:", record["active"])
        if not args.local and not args.version and not record["candidate"]:
            if record["rollback_target"]:
                print("Recovery command:", recovery_command(home, record["rollback_target"]))
            state.prune(home, record)
            return
    if record["active"] and args.command == "install":
        if record["candidate"]:
            raise ValueError("mixed installation; run kk status for recovery commands")
        print("Already installed:", record["active"])
        return
    if (record["candidate"] or {}).get("operation") == "rollback":
        raise ValueError("rollback in progress; run kk rollback to finish restoring the release")
    check_link(home, record)
    work = home / ".first-install-work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    try:
        version = prepare(home, record, args, archive_file, work)
        if version is None:
            return
        stage = home / "staging" / version
        release = home / "releases" / version
        source = stage if stage.is_dir() else release
        staged_cli = load_cli(source / "kk/lib", "_kk_preflight")
        codex_plan = staged_cli.codex_profile.prepare_activation(source, record)
        if record["active"] and record["candidate"]["phase"] == "staged":
            active = record["releases"][record["active"]]
            if active["tools"].get("claude") == "awaiting review":
                _, issues = mixed.inspect("claude", Path("/"))
                if not issues:
                    active["tools"]["claude"] = "ready"
            if active.get("codex_snapshot") and record.get("codex_plugins"):
                old = home / "releases" / record["active"]
                phase, _ = codex_trust.machine(old, active)
                state.record_codex_phase(active, phase)
        state.checkpoint(home, record, "place")
        if record["candidate"].get("operation") == "add-codex":
            print("Adding Codex to the active release. If interrupted, resume offline with kk upgrade.", flush=True)
        elif record["active"]:
            print("If activation stops, restore the active release with",
                  recovery_command(home, record["active"]), flush=True)
        if stage.exists():
            if record["active"]:
                if release.exists():
                    raise ValueError("cannot overwrite a placed release: {}".format(release))
                stage.rename(release)
            else:
                replace_pending(stage, release, work)
        # Staging is private to this writer. Placed releases may already
        # service hooks in open sessions and follow the retention policy.
        if (home / "staging").is_dir():
            shutil.rmtree(home / "staging")
        candidate = load_cli(release / "kk/lib", "_kk_candidate")
        candidate.finish_install(home, record, release, codex_plan)
    finally:
        shutil.rmtree(work)


def rollback_locked(home, record):
    pending = record["candidate"] or {}
    if pending.get("operation") == "add-codex" and pending["phase"] == "activating":
        raise ValueError("first Codex installation on the active release is unfinished; "
                         "there is no earlier Codex installation to restore. Resume offline with kk upgrade")
    target = state.rollback_version(record)
    if not target:
        raise ValueError("no previous release to restore")
    codex_profile.reconcile_claim(home, record)
    release = home / "releases" / payload.release_id(target)
    check_link(home, record)
    saved = record["releases"][target]
    for tool, phase in saved.get("tools", {}).items():
        if phase not in ("ready", "unverified"):
            print("Restoring {} with {} previously {}.".format(target, tool, phase))
    payload.verify_saved(release, saved)
    validation.validate(release)
    plan = codex_profile.prepare(release, record, snapshot=saved.get("codex_snapshot"))
    previous = record["candidate"]
    if plan and plan[3]:
        installed = codex_plugins.receipt(record, Path(plan[3]["directory"]), "kk-guard")
        if record.get("codex_plugin_pending") == codex_plugins.GUARD_ID or (
                installed and installed["identity"] != codex_plugins.guard_identity(release / "kodex-guard")):
            print("Restoring a different Codex guard. Open sessions may run without protection until "
                  "the restored hooks are reviewed. Continuing offline recovery.", file=sys.stderr, flush=True)
    if not previous or previous.get("operation") != "rollback":
        rollback = {"operation": "rollback", "phase": "activating", "version": target}
        if previous and previous["version"] != target:
            rollback["abandoned"] = previous["version"]
            if (home / "releases" / payload.release_id(previous["version"])).is_dir():
                state.remember_candidate(record, previous)
        record["candidate"] = rollback
        record.pop("pending_entry", None)
        record.pop("pending_entry_sha256", None)
    state.checkpoint(home, record, "restore")
    finish_install(home, record, release, plan)
    staging = home / "staging"
    if staging.is_dir():
        shutil.rmtree(staging)


def tool_status(home, record, tool, saved, check_live):
    workspace = Path.cwd().resolve()
    directory = codex_profile.codex_home()
    copies, issues = mixed.inspect(tool, workspace, directory)
    for entry in copies:
        print("Git-marketplace {} install: {} ({} scope, {}{})".format(
            tool, entry.plugin, entry.scope, "enabled" if entry.enabled else "disabled",
            ", " + entry.project if entry.project else ""))
    configured = tool in saved["tools"] and (tool == "claude" or codex_plugins.receipt(record, directory, "kk-guard"))
    if configured and any(i.scope == "user" for i in copies):
        print("Run kk status --remove-mixed to review user-scope removal.")
    if not configured:
        print("{}: managed guard is not installed in this CODEX_HOME; {}".format(tool, codex_plugins.activation_hint(saved)))
        for issue in issues:
            print("  " + issue)
        if check_live and tool not in saved["tools"]:
            print("{} live: skipped (not managed by this installation)".format(tool))
        return not check_live or tool not in saved["tools"]
    phase = "awaiting review" if issues else saved["tools"][tool]
    changing = (record["candidate"] or {}).get("phase") == "activating" or record.get("codex_write_pending")
    if tool == "codex" and not changing:
        if saved.get("codex_snapshot", {}).get("directory") != str(directory):
            phase = "awaiting review"
            issues.append("managed guard missing in this CODEX_HOME; " + codex_plugins.activation_hint(saved))
        else:
            phase, issues = codex_trust.machine(home / "releases" / record["active"], saved, inventory_issues=issues)
    elif tool == "claude" and not changing and not issues:
        phase = "ready"
    print("{}: {}".format(tool, phase))
    for issue in issues:
        print("  " + issue)
    if check_live:
        if changing:
            print("{} live: cannot verify while activation is pending".format(tool))
            return False
        try:
            print("{} live: {}".format(tool, live.run(tool, home)))
        except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
            print("{} live: failed: {}".format(tool, exc))
            return False
    return True


def remove_mixed(home):
    with state.writer(home):
        record = state.load(home)
        if not record["active"] or not record["installed_paths"] or (record["candidate"] or {}).get("phase") == "activating":
            raise ValueError("finish activation before reviewing Git-marketplace copies")
        workspace = Path.cwd().resolve()
        directory = codex_profile.codex_home()
        release = home / "releases" / record["active"]
        for tool in record["releases"][record["active"]]["tools"]:
            if tool == "claude":
                mixed.remove_user_copies(tool, workspace, directory)
            elif codex_plugins.receipt(record, directory, "kk-guard"):
                _, issues = codex_trust.check(release, directory, workspace)
                mixed.remove_user_copies(tool, workspace, directory, issues)


def status(home, check_live=False):
    record = state.load(home)
    active = record["active"]
    print("Active:", active or "none")
    verified = bool(active)
    if active and not record["installed_paths"]:
        # The staging smoke test dispatches through a private journal before
        # there are any published paths or vendor installations to inspect.
        for tool, phase in record["releases"][active]["tools"].items():
            print("Recorded {}: {} (no published installation)".format(tool, phase))
        verified = False
    elif active:
        saved = record["releases"][active]
        tools = list(saved["tools"])
        if "codex" not in tools and shutil.which("codex"):
            tools.append("codex")
        for tool in tools:
            if not tool_status(home, record, tool, saved, check_live):
                verified = False
    codex_profile.report_drift(record)
    if record.get("codex_write_pending"):
        print("Codex file update interrupted. Resume the pending operation.")
    if record.get("codex_paths"):
        codex_launch.report_imports(home)
    if record.get("pending_entry"):
        print("Dispatcher publication pending. Run kk upgrade to finish, or kk rollback to restore the rollback target.")
    if record["candidate"]:
        print("Candidate: {version} ({phase})".format(**record["candidate"]))
        candidate = record["candidate"]
        if not active:
            print("Run install.sh again to finish the first install.")
        elif candidate.get("operation") == "add-codex":
            print("First Codex installation on this release is pending. Resume offline with kk upgrade.")
        elif candidate.get("operation") == "rollback":
            print("Mixed installation. Finish rollback with kk rollback.")
            print("Recovery command:", recovery_command(home, candidate["version"]))
        elif candidate["phase"] == "activating":
            print("Mixed installation. Resume with kk upgrade or restore the active release with kk rollback.")
            print("Recovery command:", recovery_command(home, active))
        else:
            print("Run kk upgrade to activate the staged release.")
        if candidate.get("step"):
            print("Journaled step:", candidate["step"])
    print("Rollback target:", record["rollback_target"] or "none")
    return 1 if check_live and not verified else 0


def main():
    parser = argparse.ArgumentParser(prog="kk")
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("install", "upgrade"):
        action = commands.add_parser(command)
        source = action.add_mutually_exclusive_group()
        source.add_argument("--local", type=Path, metavar="CHECKOUT")
        source.add_argument("--version", metavar="TAG")
    status_options = commands.add_parser("status").add_mutually_exclusive_group()
    status_options.add_argument("--live", action="store_true", help="verify each managed guard with a scratch session")
    status_options.add_argument("--remove-mixed", action="store_true", help="confirm removal of user-scope Git-marketplace copies")
    commands.add_parser("rollback")
    migration = commands.add_parser("migrate", help="preview and retire the legacy template in this repository")
    migration.add_argument("--retirement-version", metavar="TAG", default=migrate.RETIREMENT_VERSION,
                           help="use this retirement release (default: %(default)s)")
    commands.add_parser("apply", help="rewrite the active release's Codex files from current overrides")
    commands.add_parser("codex", help="launch Codex with the managed profile")
    commands.add_parser("claude", help="launch Claude with the active release's settings (--print-layer to inspect)")
    home = state.toolbox_home()
    try:
        if sys.argv[1:2] == ["claude"]:
            claude_launch.launch(home, sys.argv[2:])
            return 0
        if sys.argv[1:2] == ["codex"]:
            codex_launch.launch(home, sys.argv[2:])
            return 0
        args = parser.parse_args()
        if args.command == "status":
            if args.remove_mixed:
                remove_mixed(home)
            return status(home, args.live)
        else:
            with state.writer(home):
                record = state.load(home)
                owner = state.rollback_version(record) if args.command == "rollback" else record["active"]
                if owner and Path(__file__).resolve().parents[2] != home / "releases" / payload.release_id(owner):
                    # The lock may have changed hands since the shell read state.
                    raise ValueError("release selection changed; rerun kk " + args.command)
                if args.command == "rollback":
                    rollback_locked(home, record)
                elif args.command == "migrate":
                    migrate.migrate(home, record, args.retirement_version)
                elif args.command == "apply":
                    if not owner or (record["candidate"] or {}).get("phase") == "activating" or record.get("pending_entry"):
                        raise ValueError("finish install, upgrade or rollback before running kk apply")
                    release = home / "releases" / payload.release_id(owner)
                    codex_profile.reconcile_claim(home, record)
                    plan = codex_profile.prepare(release, record, required=True)
                    codex_profile.publish(home, record, owner, plan)
                    saved = record["releases"][owner]
                    if record.get("codex_plugins") and saved.get("codex_snapshot"):
                        phase, issues = codex_trust.machine(release, saved, prompt=True)
                        state.record_codex_phase(saved, phase)
                        state.write_json(home / "state.json", record)
                        codex_trust.report(phase, issues)
                else:
                    install_locked(home, args)
        return 0
    except (OSError, ValueError, KeyError, tarfile.TarError, subprocess.SubprocessError) as exc:
        print("kk:", exc, file=sys.stderr)
        return 1
