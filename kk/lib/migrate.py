"""Retire a repository's legacy template using the retirement release's own scripts."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from . import claude, codex_plugins, codex_profile, codex_trust, live, payload


RETIREMENT_VERSION = "v0.26.0-rc.4"
MANIFEST = ".github/template-state.json"


def prerequisites():
    if not shutil.which("curl"):
        raise ValueError("curl is required for this migration step only")
    if shutil.which("yq"):
        version = subprocess.run(["yq", "--version"], capture_output=True, text=True, timeout=10)
        if version.returncode == 0 and "github.com/mikefarah/yq" in version.stdout:
            return
    raise ValueError("Mike Farah's yq is required for this migration step only")


def confirm(question):
    print(question + " [y/N] ", end="", file=sys.stderr, flush=True)
    return sys.stdin.readline().strip().lower() in ("yes", "y")


def repository_tools(workspace):
    tools = [tool for tool in ("claude", "codex") if os.path.lexists(workspace / ("." + tool))]
    if not tools:
        raise ValueError("no legacy .claude or .codex configuration in " + str(workspace))
    return tools


def verify_workspace(tool, home, record, workspace):
    release = home / "releases" / record["active"]
    saved = record["releases"][record["active"]]
    if tool not in saved["tools"]:
        raise ValueError("this repository uses {}, but its managed guard is not installed".format(tool))
    if tool == "claude":
        claude.verify_workspace(claude.vendor(workspace, "list"), release / "klaude-plugin", workspace)
        return
    directory = codex_profile.codex_home()
    if (saved.get("codex_snapshot", {}).get("directory") != str(directory)
            or not codex_plugins.receipt(record, directory, "kk-guard")):
        raise ValueError("managed Codex guard missing in this CODEX_HOME; " + codex_plugins.activation_hint(saved))
    phase, issues = codex_trust.check(release, directory, workspace, acknowledged=saved["tools"][tool] == "unverified")
    if phase not in ("ready", "unverified"):
        raise ValueError("{} guard in {}: {}".format(tool, workspace, "; ".join(issues)))
    if phase == "unverified":
        print("Codex cannot report hook trust here. The scratch live check is required.", flush=True)


def fetch_scripts(directory, repository, tag):
    base = "https://raw.githubusercontent.com/{}/refs/tags/{}/.claude/toolbox/scripts".format(repository, tag)
    for name in ("template-sync.sh", "semver-compare.sh"):
        subprocess.run(["curl", "--disable", "--fail", "--silent", "--show-error", "--location",
                        "--proto", "=https", "--max-time", "60", "--output", str(directory / name),
                        base + "/" + name], check=True)
    script = directory / "template-sync.sh"
    help_text = subprocess.run(["bash", str(script), "--help"], check=True, capture_output=True, text=True)
    if "--retire" not in help_text.stdout.split():
        raise ValueError("{} does not provide the template retirement mode".format(tag))
    return script


def route_legacy_upstream(env, upstream, repository, scratch):
    # RC4 reads the downstream manifest again, and can rewrite starter-kit to
    # claude-toolbox during sync. Bind those Git fetches to the verified source.
    if upstream == repository:
        return
    def git_url(slug):
        url = "https://github.com/{}.git".format(slug)
        # Like RC4's git clone, resolve inherited settings outside the adopter repository.
        return subprocess.check_output(["git", "ls-remote", "--get-url", url],
                                       cwd=scratch, env=env, text=True).strip()

    target = git_url(repository)
    aliases = [upstream]
    if upstream == "serpro69/claude-starter-kit":
        aliases.append("serpro69/claude-toolbox")
    count = int(env.get("GIT_CONFIG_COUNT") or 0)
    for alias in aliases:
        env["GIT_CONFIG_KEY_{}".format(count)] = "url.{}.insteadOf".format(target)
        env["GIT_CONFIG_VALUE_{}".format(count)] = "https://github.com/{}.git".format(alias)
        count += 1
        env["GIT_CONFIG_COUNT"] = str(count)
        # Git keeps the first of equally specific insteadOf rules.
        if git_url(alias) != target:
            raise ValueError("conflicting Git URL rewrite for {}; align it with {} before migrating".format(
                alias, repository))


def migrate(home, record, tag):
    tag = payload.tag_name(tag)
    if (not record["active"] or not record["installed_paths"] or record.get("pending_entry")
            or record.get("codex_write_pending") or (record["candidate"] or {}).get("phase") == "activating"):
        raise ValueError("finish installing or activating kk before migrating")
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], check=True, text=True, stdout=subprocess.PIPE)
    workspace = Path(root.stdout.rstrip("\n")).resolve()
    if not (workspace / MANIFEST).is_file():
        raise ValueError("no legacy {} in {}".format(MANIFEST, workspace))
    saved = record["releases"][record["active"]]
    source = saved.get("source", {})
    repository = payload.canonical_repository(source.get("repository", payload.upgrade_repository()))
    payload.api_root(repository)  # Validate the trusted install source before using it in a URL.
    upstream = payload.read_json(workspace / MANIFEST)["upstream_repo"]
    if payload.canonical_repository(upstream) != repository:
        raise ValueError("the manifest names {}, but the migration scripts would come from {}".format(upstream, repository))
    prerequisites()
    tools = repository_tools(workspace)
    for tool in tools:
        verify_workspace(tool, home, record, workspace)
        print("{} live: {}".format(tool, live.run(tool, home)), flush=True)
    print("Close any Codex sessions opened before kk was installed and its hooks reviewed. "
          "Those sessions can run commands without guard protection after retirement. "
          "kk cannot detect open sessions.", flush=True)
    if not confirm("Continue with migration in {}?".format(workspace)):
        print("Migration cancelled before sync.")
        return

    with tempfile.TemporaryDirectory(prefix="kk-migrate-") as temp:
        directory = Path(temp)
        script = fetch_scripts(directory, repository, tag)
        env = dict(os.environ, TEMPLATE_SYNC_NO_HANDOFF="1")
        env.pop("TEMPLATE_SYNC_HANDOFF_CLEANUP", None)
        env.pop("TEMPLATE_SYNC_MERGE_DENY", None)
        route_legacy_upstream(env, upstream, repository, directory)
        sync_env = dict(env, TEMPLATE_SYNC_MERGE_DENY="1")

        def run(options, environment):
            subprocess.run(["bash", str(script), *options, "--version", tag], cwd=workspace, env=environment,
                           stdin=subprocess.DEVNULL, check=True)

        report = directory / "sync-report"
        run(["--dry-run", "--ci"], dict(sync_env, GITHUB_OUTPUT=str(report)))
        # The first output is the sync script's boolean. Its multiline diff
        # summary can contain arbitrary repository text, including other keys.
        with report.open(encoding="utf-8") as stream:
            changes = stream.readline().strip()
        if changes == "has_changes=true":
            if not confirm("Apply the previewed sync, including overwrites of modified template files?"):
                print("Migration cancelled before sync.")
                return
            run(["--local"], sync_env)
        elif changes != "has_changes=false":
            raise ValueError("retirement release did not report whether sync changes are needed")
        run(["--retire", "--dry-run"], env)
        if not confirm("Apply the previewed retirement and leave the changes uncommitted?"):
            print("Retirement declined. The repository remains synced with its legacy guard in place.")
            return
        # Sync can introduce a tool or change repository hook settings. Check
        # the effective workspace again immediately before any removal.
        for tool in repository_tools(workspace):
            verify_workspace(tool, home, record, workspace)
            if tool not in tools:
                print("{} live: {}".format(tool, live.run(tool, home)), flush=True)
        run(["--retire"], env)
    print("Migration complete. Review the uncommitted changes with git diff.")
