import contextlib
import io
import json
import os
from pathlib import Path
import pty
import select
import subprocess
import time
from unittest.mock import patch

from test_install import InstallFixture, cli


class LaunchNotice(InstallFixture):
    def test_explicit_upgrade_check_is_read_only(self):
        self.install()
        installed = self.state()
        installed["releases"][installed["active"]]["source"] = {"tag": "v1.0.0", "repository": "old/fork"}
        cli.state.write_json(self.state_file, installed)
        record = self.state_file.read_bytes()
        since = self.state_file.stat().st_mtime_ns
        with patch.dict(os.environ, self.env), patch("sys.argv", ["kk", "upgrade", "--check"]), \
                patch.object(cli.payload, "latest_tag", return_value="v77.0.0") as fetch, \
                contextlib.redirect_stdout(io.StringIO()) as output, cli.state.writer(self.toolbox):
            os.environ.pop("KK_REPOSITORY", None)
            self.assertEqual(cli.main(), 0)
            fetch.assert_called_once_with("serpro69/agentstakk")
            os.environ["KK_REPOSITORY"] = "new/fork"
            self.assertEqual(cli.main(), 0)
            fetch.assert_called_with("new/fork")
        self.assertIn("v77.0.0 is available", output.getvalue())
        self.assertEqual(self.state_file.read_bytes(), record)
        self.assertEqual(self.state_file.stat().st_mtime_ns, since)
        self.assertFalse((self.toolbox / "update-notice.json").exists())

    def test_check_is_daily_stable_only_and_silent_offline(self):
        self.toolbox.mkdir(parents=True)
        repo = "example/toolbox"
        stderr = io.StringIO()
        tag = "v2.0.0-rc.1"
        record = {"active": tag, "releases": {tag: {"source": {"tag": tag, "repository": repo}}}}
        with contextlib.redirect_stderr(stderr), patch.object(cli.notice.time, "time") as clock, patch.dict(os.environ, self.env):
            clock.return_value = 100
            with patch.object(cli.payload, "latest_tag", return_value="v2.0.0") as fetch:
                cli.notice.refresh(self.toolbox, repo)
                cli.notice.refresh(self.toolbox, repo)
                fetch.assert_called_once_with(repo)
            with patch.object(cli.payload, "latest_tag", return_value="v1.0.0") as fetch:
                cli.notice.refresh(self.toolbox, "other/fork")
                cli.notice.refresh(self.toolbox, repo)
                fetch.assert_called_once_with("other/fork")
            self.assertEqual(stderr.getvalue(), "")
            with patch("sys.stdin.isatty", return_value=True), patch.object(stderr, "isatty", return_value=True):
                with patch.object(cli.notice.subprocess, "run", side_effect=AssertionError("unexpected fetch")):
                    cli.notice.on_launch(self.toolbox, record)
                    cli.notice.on_launch(self.toolbox, record)
            self.assertEqual(len(stderr.getvalue().splitlines()), 1)
            self.assertIn("v2.0.0 is available", stderr.getvalue())
            clock.return_value += cli.notice.DAY
            with patch.object(cli.payload, "latest_tag", side_effect=OSError("offline")) as fetch:
                cli.notice.refresh(self.toolbox, repo)
                fetch.assert_called_once_with(repo)
            self.assertEqual(len(stderr.getvalue().splitlines()), 1)
        for latest, installed, expected in (("v1.10.0", "v1.9.0", True), ("v1.9.0", "v1.10.0", False),
                                             ("v2.0.0-rc.1", "v1.0.0", False), ("v1.0.0", "v1.0.0+abc", False)):
            self.assertEqual(cli.notice.newer(latest, installed), expected)

    def test_launch_from_old_upstream_reuses_daily_notice(self):
        self.toolbox.mkdir(parents=True)
        old = "serpro69/claude-toolbox"
        tag = "v1.0.0"
        source = {"repository": old, "tag": tag}
        record = {"active": tag, "releases": {tag: {"source": source}}}
        cli.state.write_json(self.toolbox / "update-notice.json",
                             {old: {"latest": "v1.1.0", "checked": time.time(), "shown": True}})
        with patch.dict(os.environ, self.env), patch("sys.stdin.isatty", return_value=True), \
                patch("sys.stderr.isatty", return_value=True), patch.object(cli.notice.subprocess, "run") as refresh:
            cli.notice.on_launch(self.toolbox, record)
            refresh.assert_not_called()
            self.assertEqual(cli.codex_plugins.activation_hint({"source": source}), "run kk upgrade --version v1.0.0")
            cli.state.write_json(self.toolbox / "update-notice.json", {})
            cli.notice.on_launch(self.toolbox, record)
            self.assertEqual(refresh.call_args.args[0][-1], "serpro69/agentstakk")

    def test_terminal_and_opt_out(self):
        self.install()
        record = self.state()
        with patch.dict(os.environ, self.env), patch.object(cli.notice.subprocess, "run") as spawn:
            with patch("sys.stdin.isatty", return_value=True), patch("sys.stderr.isatty", return_value=False):
                cli.notice.on_launch(self.toolbox, record)
            spawn.assert_not_called()
            with patch("sys.stdin.isatty", return_value=True), patch("sys.stderr.isatty", return_value=True):
                cli.state.write_json(cli.state.override_path(), {"launchNotice": False})
                cli.notice.on_launch(self.toolbox, record)
                spawn.assert_not_called()
                cli.state.write_json(cli.state.override_path(), {})
                cli.notice.on_launch(self.toolbox, record)
                self.assertTrue(spawn.call_args.kwargs["start_new_session"])
                self.assertEqual(spawn.call_args.kwargs["stderr"], subprocess.DEVNULL)

    def test_pending_notice_survives_expiry_and_offline_refresh(self):
        self.toolbox.mkdir(parents=True)
        repo, tag = "fixture/fork", "v1.0.0"
        record = {"active": tag, "releases": {tag: {"source": {"repository": repo, "tag": tag}}}}
        with patch.dict(os.environ, self.env), patch.object(cli.notice.time, "time") as clock:
            clock.return_value = 1
            with patch.object(cli.payload, "latest_tag", return_value="v2.0.0"):
                cli.notice.refresh(self.toolbox, repo)
            clock.return_value += 2 * cli.notice.DAY
            with patch.object(cli.payload, "latest_tag", side_effect=OSError("offline")):
                cli.notice.refresh(self.toolbox, repo)
            clock.return_value += 2 * cli.notice.DAY
            with contextlib.redirect_stderr(io.StringIO()) as out, patch("sys.stdin.isatty", return_value=True):
                with patch.object(out, "isatty", return_value=True), patch.object(cli.notice.subprocess, "run") as start:
                    cli.notice.on_launch(self.toolbox, record)
                    start.assert_called_once()
                    self.assertIn("v2.0.0 is available", out.getvalue())
            self.assertTrue(cli.notice.read_cache(self.toolbox)[repo]["shown"])

    def test_both_launchers_return_while_update_fetch_is_blocked(self):
        # A worker blocked on this pipe cannot finish until both launchers
        # have already exec'd and exited. No wall-clock benchmark is needed.
        pipe = self.root / "upstream"
        os.mkfifo(pipe)
        request = self.root / "request"
        with (self.checkout / "kk/lib/payload.py").open("a") as fixture:
            fixture.write("\ndef latest_tag(repo):\n    Path({!r}).touch()\n"
                          "    with open({!r}) as f:\n        return f.readline().strip()\n".format(str(request), str(pipe)))
        self.install()
        with pipe.open("r+b", buffering=0) as service:
            master, slave = pty.openpty()
            try:
                for tool in ("claude", "codex"):
                    result = subprocess.run([self.link, tool, "hello"], cwd=self.root, env=self.env, stdin=slave,
                                            stdout=subprocess.PIPE, stderr=slave, timeout=5)
                    self.assertEqual(result.returncode, 0)
                    self.assertIn(b"hello", result.stdout)
                deadline = time.monotonic() + 5
                while not request.exists() and time.monotonic() < deadline:
                    time.sleep(.02)
                self.assertTrue(request.exists())
                self.assertFalse(select.select([master], [], [], 0)[0])
                service.write(b"v1.0.0\n")
                cache = self.toolbox / "update-notice.json"
                deadline = time.monotonic() + 5
                while not cache.exists() and time.monotonic() < deadline:
                    time.sleep(.02)
                self.assertTrue(cache.is_file())
                subprocess.run([self.link, "codex", "hello"], cwd=self.root, env=self.env, stdin=slave,
                               stdout=slave, stderr=slave, timeout=5, check=True)
                output = os.read(master, 16384)
                self.assertLess(output.index(b"v1.0.0 is available"), output.index(b"hello"))
            finally:
                os.close(slave)
                os.close(master)


class InstallationStatus(InstallFixture):
    def test_claude_readiness_requires_source_and_effective_settings(self):
        self.install()
        cli.state.write_json(self.home / "list-override", {"readFromFolder": str(self.root)})
        self.assertIn("claude: awaiting review", self.invoke(self.link, "status").stdout)
        (self.home / "list-override").unlink()
        cli.state.write_json(self.home / "effective-settings", {"disableAllHooks": True})
        self.assertIn("settings disable the managed guard", self.invoke(self.link, "status").stdout)
        (self.home / "effective-settings").unlink()
        self.assertIn("claude: ready", self.invoke(self.link, "status").stdout)

    def test_project_setting_can_enable_old_id_without_an_inventory_row(self):
        self.install()
        for plugin in ("kk@claude-toolbox", "kk@toolbox", "kk@agentstakk"):
            with self.subTest(plugin=plugin):
                cli.state.write_json(self.home / "effective-settings", {"enabledPlugins": {plugin: True}})
                status = self.invoke(self.link, "status").stdout
                self.assertIn("claude: awaiting review", status)
                self.assertIn("settings also enable " + plugin, status)

    def test_mixed_scope_confirmation_and_readiness(self):
        codex = Path(self.env["CODEX_HOME"])
        codex.mkdir()
        current = "kk@claude-toolbox"
        project = {"id": current, "scope": "project", "projectPath": str(self.root), "enabled": True}
        user = {"id": current, "scope": "user", "enabled": True}
        unrelated = {"id": "other@claude-toolbox", "scope": "user", "enabled": True}
        claude_path = self.home / "claude-git"
        cli.state.write_json(claude_path, [user, project, unrelated])
        codex_path = codex / "codex-git"
        cli.state.write_json(codex_path, [{"pluginId": current, "enabled": True},
                                          {"pluginId": "kk-guard@claude-toolbox", "enabled": True}])
        self.install()
        record = self.state()
        self.assertEqual(record["releases"][record["active"]]["tools"], {"claude": "awaiting review", "codex": "awaiting review"})
        guard = next((codex / "plugins/cache/agentstakk-local/kk-guard").iterdir())
        (codex / "fixture-reviewed").write_text(guard.name)
        before = self.state_file.read_bytes()
        status = self.invoke(self.link, "status").stdout
        self.assertIn("claude: awaiting review", status)
        self.assertIn("codex: awaiting review", status)
        self.assertIn("--remove-mixed", status)
        self.assertEqual(self.state_file.read_bytes(), before)
        self.assertIn("confirmation", self.invoke(self.link, "status", "--remove-mixed", ok=False).stderr)
        with patch.dict(os.environ, self.env), patch("sys.stdin.isatty", return_value=True):
            (codex / "fixture-reviewed").unlink()
            with patch("sys.stdin.readline", return_value="\n"):
                with contextlib.redirect_stderr(io.StringIO()) as preview:
                    cli.remove_mixed(self.toolbox)
            self.assertIn("Bash: untrusted", preview.getvalue())
            self.assertIn("can leave Codex sessions unguarded", preview.getvalue())
            (codex / "fixture-reviewed").write_text(guard.name)
            self.assertEqual(len(json.loads(claude_path.read_text())), 3)
            with patch("sys.stdin.readline", return_value="yes\n"):
                cli.remove_mixed(self.toolbox)
        self.assertEqual(json.loads(claude_path.read_text()), [project, unrelated])
        self.assertEqual(json.loads(codex_path.read_text()), [])
        after = self.invoke(self.link, "status").stdout
        self.assertIn("claude: awaiting review", after)
        self.assertIn("codex: ready", after)
        cli.state.write_json(claude_path, [dict(project, enabled=False)])
        cli.state.write_json(codex_path, [{"pluginId": current, "enabled": True}])
        after = self.invoke(self.link, "status").stdout
        self.assertIn("claude: ready", after)
        self.assertIn("codex: ready", after)
        self.assertIn(current, after)

    def test_rollback_skips_release_with_never_verified_claude_guard(self):
        record = cli.state.load(self.toolbox)
        cli.state.promote(record, "v1.0.0")
        cli.state.promote(record, "v2.0.0", "awaiting review")
        cli.state.promote(record, "v3.0.0")
        self.assertEqual(record["rollback_target"], "v1.0.0")

    def test_live_requires_tool_evidence_from_each_scratch_workspace(self):
        samples = []
        def run(args, *, cwd, **kwargs):
            if args[0] == "git":
                return subprocess.CompletedProcess(args, 0)
            canary, = cwd.glob("kk-live-*.txt")
            samples.append(canary)
            name = canary.name
            self.assertEqual(json.loads((cwd / ".claude/kk-guard.json").read_text())["secrets"], ["./**/" + name])
            reason = "kk guard: secrets — Read of {} matches ./**/{}. Way through: fixture".format(name, name)
            result = subprocess.CompletedProcess(args, 0, "", "")
            if args[1] == "claude":
                use = {"type": "tool_use", "id": "id1", "name": "Read", "input": {"file_path": str(canary)}}
                error = {"type": "tool_result", "tool_use_id": "id1", "is_error": True, "content": reason}
                events = (("assistant", use), ("user", error)) if good else (("assistant", use), ("assistant", error))
                result.stdout = "\n".join(json.dumps({"type": role, "message": {"content": [block]}}) for role, block in events)
            else:
                result.stderr = ("codex_core::tools::router: error=Command blocked by PreToolUse hook: " + reason
                                 if good else "sandbox permission denied")
                result.stdout = json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": reason}})
            return result
        with patch.object(cli.mixed, "inspect", return_value=([], [])), patch.object(cli.live.subprocess, "run", side_effect=run):
            for tool in ("claude", "codex"):
                good = True
                self.assertIn("kk guard: secrets", cli.live.run(tool, self.toolbox))
                good = False
                with self.assertRaisesRegex(ValueError, "did not report"):
                    cli.live.run(tool, self.toolbox)
        self.assertEqual(len({p.parent for p in samples}), 4)
        self.assertTrue(all(not p.parent.exists() for p in samples))

    def test_live_command_tries_both_tools_and_fails_on_missing_evidence(self):
        self.install()
        record = self.state()
        guard = next((Path(self.env["CODEX_HOME"]) / "plugins/cache/agentstakk-local/kk-guard").iterdir())
        (Path(self.env["CODEX_HOME"]) / "fixture-reviewed").write_text(guard.name)
        run = self.invoke(self.link, "status", "--live", ok=False)
        self.assertIn("codex live: failed", run.stdout)
        self.assertIn("claude live: failed", run.stdout)
        self.assertEqual(self.state(), record)

    def test_unmanaged_vendor_is_reported_but_is_not_a_required_live_check(self):
        self.install()
        record = self.state()
        del record["releases"][record["active"]]["tools"]["codex"]
        record.pop("codex_plugins")
        cli.state.write_json(self.state_file, record)
        with patch.dict(os.environ, self.env), patch.object(cli.live, "run", return_value="confirmed") as probe:
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(cli.status(self.toolbox, True), 0)
        probe.assert_called_once_with("claude", self.toolbox)
        self.assertIn("codex live: skipped", output.getvalue())
