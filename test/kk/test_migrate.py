import io
import json
import os
from pathlib import Path
import shutil
import subprocess
from unittest.mock import patch

from test_install import InstallFixture, ROOT, cli


class Migration(InstallFixture):
    def setUp(self):
        super().setUp()
        self.repo = self.root / "project"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        tools = self.root / "migration-tools"
        tools.mkdir()
        for name, body in (("yq", 'test "$1" = --version && echo "yq (https://github.com/mikefarah/yq/) version v4"'),
                           ("curl", "exit 1")):
            path = tools / name
            path.write_text("#!/bin/sh\n" + body + "\n")
            path.chmod(0o755)
        self.env["PATH"] = str(tools) + os.pathsep + self.env["PATH"]
        self.guard = self.repo / ".codex/legacy"
        self.guard.parent.mkdir()
        self.guard.write_text("old")
        self.manifest = self.repo / cli.migrate.MANIFEST
        cli.state.write_json(self.manifest, {"upstream_repo": cli.payload.UPSTREAM})
        directory = self.env["CODEX_HOME"]
        self.saved = {"tools": {"codex": "ready"}, "codex_snapshot": {"directory": directory}}
        self.record = {"active": "v1.0.0", "installed_paths": [str(self.link)], "candidate": None,
                       "releases": {"v1.0.0": self.saved}, "codex_plugins": {directory: {"kk-guard": {"version": "1"}}}}
        self.addCleanup(os.chdir, Path.cwd())
        os.chdir(self.repo)
        self.enter_patch(patch.dict(os.environ, self.env))
        self.probe = self.enter_patch(patch.object(cli.live, "run", return_value="scratch denial"))
        self.trust = self.enter_patch(patch.object(cli.codex_trust, "check", return_value=("ready", [])))
        self.tag = "v1.2.3-rc.1"

    def enter_patch(self, patcher):
        self.addCleanup(patcher.stop)
        return patcher.start()

    def migrate(self, answers):
        with patch("sys.stdin", io.StringIO(answers)):
            cli.migrate.migrate(self.toolbox, self.record, self.tag)

    def test_fork_manifest_must_match_install_source(self):
        fork = "other/claude-toolbox"
        cli.state.write_json(self.manifest, {"upstream_repo": fork})
        with self.assertRaisesRegex(ValueError, "manifest names other/claude-toolbox"):
            self.migrate("yes\n")
        self.probe.assert_not_called()
        self.saved["source"] = {"repository": fork, "tag": self.tag}
        with patch.object(cli.migrate, "fetch_scripts", side_effect=OSError("fixture download")) as fetch:
            with self.assertRaisesRegex(OSError, "fixture download"):
                self.migrate("yes\n")
            self.assertEqual(fetch.call_args.args[1:], (fork, self.tag))

    def test_conflicting_legacy_git_mirror_stops_before_sync(self):
        old = "serpro69/claude-toolbox"
        cli.state.write_json(self.manifest, {"upstream_repo": old})
        env = {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "url.file:///other-repo.insteadOf",
               "GIT_CONFIG_VALUE_0": "https://github.com/" + old + ".git"}
        with patch.dict(os.environ, env), patch.object(cli.migrate, "fetch_scripts"):
            with self.assertRaisesRegex(ValueError, "conflicting Git URL rewrite"):
                self.migrate("yes\n")
        self.assertTrue(self.guard.is_file())

    def test_rc4_migration_from_old_manifest_preserves_exclusions(self):
        tag = cli.migrate.RETIREMENT_VERSION
        template = subprocess.run(["git", "show", tag + ":.github/template-state.example.json"],
                                  cwd=ROOT, capture_output=True)
        if template.returncode:
            self.skipTest("full retirement tag unavailable")
        search_path = os.pathsep.join(self.env["PATH"].split(os.pathsep)[1:])
        if not shutil.which("yq", path=search_path):
            self.skipTest("the released sync client needs Mike Farah yq")
        manifest = json.loads(template.stdout)
        manifest.update(upstream_repo="serpro69/claude-starter-kit", template_version=tag,
                        sync_exclusions=[".github/template-state.json", ".claude", ".codex/rules/default.rules"])
        cli.state.write_json(self.manifest, manifest)
        before = self.manifest.read_bytes()
        rules = self.repo / ".codex/rules/default.rules"
        rules.parent.mkdir()
        rules.write_text("# downstream rules\n")
        self.saved["source"] = {"repository": "serpro69/claude-toolbox", "tag": tag}

        def fetch(directory, repository, version):
            self.assertEqual((repository, version), ("serpro69/agentstakk", tag))
            for name in ("template-sync.sh", "semver-compare.sh"):
                blob = tag + ":.claude/toolbox/scripts/" + name
                (directory / name).write_bytes(subprocess.check_output(["git", "show", blob], cwd=ROOT))
            return directory / "template-sync.sh"

        # Only the canonical repository has a reachable mirror. An unredirected
        # old URL fails here, even if the script gets as far as its second fetch.
        # git clone ignores the adopter's repository-local URL configuration.
        subprocess.run(["git", "config", "url.file:///wrong-mirror.insteadOf",
                        "https://github.com/serpro69/agentstakk.git"], cwd=self.repo, check=True)
        env = dict(PATH=search_path, GIT_ALLOW_PROTOCOL="file", GIT_CONFIG_COUNT="1",
                   GIT_CONFIG_KEY_0="url.{}.insteadOf".format(ROOT.as_uri()),
                   GIT_CONFIG_VALUE_0="https://github.com/serpro69/agentstakk.git")
        with patch.dict(os.environ, env), patch.object(cli.migrate, "fetch_scripts", side_effect=fetch):
            self.tag = tag
            self.migrate("yes\nyes\nyes\n")
        self.assertEqual(self.manifest.read_bytes(), before)
        self.assertEqual(rules.read_text(), "# downstream rules\n")
        self.assertFalse((self.repo / ".claude").exists())

    def test_workspace_trust_and_live_refusals(self):
        self.trust.return_value = ("awaiting review", ["disabled; enable it in /hooks"])
        with self.assertRaisesRegex(ValueError, "disabled"):
            self.migrate("yes\n")
        self.assertEqual(self.trust.call_args.args[2], self.repo)
        self.probe.assert_not_called()
        self.saved["tools"]["codex"] = "unverified"
        self.trust.return_value = ("unverified", ["no hooks/list method"])
        self.probe.side_effect = ValueError("missing scratch guard denial")
        with self.assertRaisesRegex(ValueError, "missing scratch guard denial"):
            self.migrate("yes\n")
        self.assertTrue(self.trust.call_args.kwargs["acknowledged"])
        self.probe.assert_called_once_with("codex", self.toolbox)
        self.assertEqual(self.guard.read_text(), "old")

    def test_unmanaged_repository_tool_and_missing_yq(self):
        (self.repo / ".claude").mkdir()
        with self.assertRaisesRegex(ValueError, "uses claude"):
            self.migrate("yes\n")
        with patch.object(cli.migrate.shutil, "which", side_effect=lambda tool: None if tool == "yq" else "/bin/curl"):
            with self.assertRaisesRegex(ValueError, "Mike Farah's yq"):
                self.migrate("yes\n")
        self.probe.assert_not_called()

    def test_claude_legacy_project_plugin_and_effective_workspace_settings(self):
        self.guard.parent.rename(self.repo / ".claude")
        self.saved["tools"]["claude"] = "ready"
        plugin = self.toolbox / "releases/v1.0.0/klaude-plugin"
        rows = [{"id": cli.claude.PLUGIN_ID, "scope": "user", "enabled": True, "readFromFolder": str(plugin)},
                {"id": cli.claude.GIT_PLUGIN, "scope": "project", "enabled": True, "projectPath": str(self.repo)}]
        with patch.object(cli.claude, "vendor", return_value=rows), patch.object(cli.claude, "settings_report") as report:
            for settings in ({"disableAllHooks": True}, {"enabledPlugins": {cli.claude.PLUGIN_ID: False}}):
                report.return_value = (0, {"effective": settings})
                with self.assertRaisesRegex(ValueError, "settings disable"):
                    self.migrate("yes\n")
            self.probe.assert_not_called()
            report.return_value = (0, {"effective": {}})
            self.migrate("\n")
            self.probe.assert_called_once_with("claude", self.toolbox)
            self.assertEqual(report.call_args.args[1], self.repo)

    def test_confirmations_and_retry_through_tagged_script_interface(self):
        # Model the tagged script's public CLI. Task 13 exercises its actual
        # file comparisons and removals against local upstream repositories.
        commands = []
        source = """set -eu
case "$1" in
  --help) echo '  --retire  Retire the template'; exit ;;
esac
test "$TEMPLATE_SYNC_NO_HANDOFF" = 1
test "${@: -2:1}" = --version && test "${@: -1}" = v1.2.3-rc.1
case "$1" in
  --dry-run)
    test "$TEMPLATE_SYNC_MERGE_DENY" = 1
    if test "$(cat .codex/legacy)" = old; then echo has_changes=true; else echo has_changes=false; fi > "$GITHUB_OUTPUT" ;;
  --local) test "$TEMPLATE_SYNC_MERGE_DENY" = 1; echo synced > .codex/legacy ;;
  --retire)
    test -z "${TEMPLATE_SYNC_MERGE_DENY:-}"
    if test "$2" != --dry-run; then mv .codex/legacy retired; fi ;;
  *) exit 2 ;;
esac
"""
        real_run = subprocess.run

        def run(args, **kwargs):
            if args[0] == "curl":
                destination = Path(args[args.index("--output") + 1])
                self.assertEqual(args[-1], "https://raw.githubusercontent.com/serpro69/agentstakk/refs/tags/"
                                 + self.tag + "/.claude/toolbox/scripts/" + destination.name)
                destination.write_text(source if destination.name == "template-sync.sh" else "# helper")
                return subprocess.CompletedProcess(args, 0)
            if args[0] == "bash":
                self.assertTrue(Path(args[1]).with_name("semver-compare.sh").is_file())
                commands.append(tuple(args[2:-2]) if args[2] != "--help" else ("--help",))
            return real_run(args, **kwargs)

        with patch.object(cli.migrate.subprocess, "run", side_effect=run):
            self.migrate("\n")
            self.assertEqual(commands, [])
            self.migrate("yes\nno\n")
            self.assertEqual(self.guard.read_text(), "old")
            self.assertNotIn(("--local",), commands)
            self.migrate("yes\nyes\n\n")
            self.assertEqual(self.guard.read_text().strip(), "synced")
            self.assertEqual(commands[-1], ("--retire", "--dry-run"))
            self.trust.side_effect = [("ready", []), ("awaiting review", ["now disabled"])]
            with self.assertRaisesRegex(ValueError, "now disabled"):
                self.migrate("yes\nyes\n")
            self.assertTrue(self.guard.is_file())
            self.trust.side_effect = None
            commands.clear()
            self.migrate("yes\nyes\n")
            self.assertNotIn(("--local",), commands)
            self.assertEqual(commands[-1], ("--retire",))
            self.assertFalse(self.guard.exists())
            self.assertTrue((self.repo / "retired").is_file())
        self.assertEqual(subprocess.check_output(["git", "diff", "--cached", "--name-only"]), b"")

    def test_cli_refuses_disabled_repository_hook_even_with_recorded_ready(self):
        self.install()
        directory = Path(self.env["CODEX_HOME"])
        guard = next((directory / "plugins/cache/toolbox/kk-guard").iterdir())
        (directory / "fixture-reviewed").write_text(guard.name)
        record = self.state()
        record["releases"][record["active"]]["tools"]["codex"] = "ready"
        cli.state.write_json(self.state_file, record)
        (directory / "disabled-0").touch()
        run = subprocess.run([self.link, "migrate"], cwd=self.repo, env=self.env, input="yes\n",
                             capture_output=True, text=True, timeout=30)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("disabled; enable it in /hooks", run.stderr)
        self.assertEqual(self.guard.read_text(), "old")
