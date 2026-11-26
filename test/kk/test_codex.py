import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import unittest
from unittest.mock import patch

from test_install import InstallFixture, ROOT, cli


class CodexFiles(InstallFixture):
    def setUp(self):
        super().setUp()
        self.codex = Path(self.env["CODEX_HOME"])
        self.profile = self.codex / "kk.config.toml"
        self.config = Path(self.env["XDG_CONFIG_HOME"]) / "kk/config.json"

    def configure(self, settings):
        cli.state.write_json(self.config, {"codex": settings})

    def flags(self):
        """The applied settings, as the configuration flags of an interactive launch."""
        argv = json.loads(self.invoke(self.link, "codex", "hello").stdout)
        if argv[0] == "--no-daemon":  # Precedes kk's flags whenever there are any.
            del argv[0]
        self.assertEqual(argv[:-1:2], ["-c"] * (len(argv) // 2))
        return argv[1::2]

    def test_collision_stops_before_activation(self):
        agent = self.codex / "agents/kk-code-reviewer.toml"
        agent.parent.mkdir(parents=True)
        agent.write_text("existing")
        self.assertIn("already exists", self.install(ok=False).stderr)
        self.assertEqual(agent.read_text(), "existing")
        self.assertFalse((self.home / "market").exists())
        self.assertNotIn(str(agent), self.state()["installed_paths"])

    def test_apply_drift_opt_ins_and_pruning(self):
        self.install()
        self.assertFalse(self.profile.exists())
        self.assertNotIn(str(self.profile), self.state()["installed_paths"])
        original = self.flags()
        self.assertFalse([flag for flag in original if flag.startswith(("approval_policy=", "sandbox_mode="))])
        self.assertEqual((self.codex / "agents/kk-code-reviewer.toml").read_bytes(),
                         (ROOT / "kk/baseline/codex/agents/code-reviewer.toml").read_bytes())
        personal = self.codex / "agents/kk-notes.toml"
        personal.touch()
        self.configure({"optIn": {"approval_policy": True, "sandbox_mode": True, "nativeForbids": True},
                        "settings": {"agents": {"max_concurrent_threads_per_session": 3}, "my_new_preference": "new"}})
        self.assertIn("kk apply", self.invoke(self.link, "status").stderr)
        before = self.state_file.read_bytes()
        launch = self.invoke(self.link, "codex", "-p", "personal", "hello")
        self.assertIn("kk apply", launch.stderr)
        self.assertEqual(json.loads(launch.stdout), ["-p", "personal", "hello"])
        self.assertEqual(self.state_file.read_bytes(), before)
        # A launch uses the settings kk apply saved, not the edited file.
        self.assertEqual(self.flags(), original)
        calls = (self.home / "calls").read_bytes()
        self.assertIn("every Codex session", self.invoke(self.link, "apply").stdout)
        self.assertTrue((self.codex / "rules/kk.rules").is_file())
        self.assertEqual((self.home / "calls").read_bytes(), calls)
        self.assertNotIn("kk apply", self.invoke(self.link, "status").stderr)
        applied = self.flags()
        for flag in ('approval_policy="on-request"', 'sandbox_mode="read-only"', 'my_new_preference="new"',
                     'agents={ "max_depth" = 1, "max_concurrent_threads_per_session" = 3 }'):
            self.assertIn(flag, applied)
        self.assertFalse(self.profile.exists())
        self.assertTrue(personal.is_file())
        self.config.unlink()
        self.assertIn("kk apply", self.invoke(self.link, "status").stderr)
        self.invoke(self.link, "apply")
        self.assertFalse((self.codex / "rules/kk.rules").exists())
        self.assertEqual(self.flags(), original)

    def test_refusals_and_ready_states(self):
        self.install()
        record = self.state()
        phases = record["releases"][record["active"]]["tools"]
        for args in (["exec", "hello"], ["-m", "model", "e", "hello"], ["review"]):
            self.assertIn("awaiting review", self.invoke(self.link, "codex", *args, ok=False).stderr)
        phases["codex"] = "unverified"
        cli.state.write_json(self.state_file, record)
        no_method = self.codex / "fixture-no-method"
        no_method.touch()
        self.assertIn("unverified", self.invoke(self.link, "codex", "exec", "hello").stderr)
        no_method.unlink()
        phases["codex"] = "ready"
        cli.state.write_json(self.state_file, record)
        version = next((self.codex / "plugins/cache/agentstakk-local/kk-guard").iterdir()).name
        (self.codex / "fixture-reviewed").write_text(version)
        launch = self.invoke(self.link, "codex", "exec", "hello")
        argv = json.loads(launch.stdout)
        self.assertEqual(argv[-2:], ["exec", "hello"])
        self.assertNotIn("--profile", argv)
        self.assertTrue(argv[-3].startswith("developer_instructions="))
        self.assertNotIn("unverified", launch.stderr)
        record["candidate"] = {"phase": "activating"}
        cli.state.write_json(self.state_file, record)
        self.assertIn("changing", self.invoke(self.link, "codex", "--profile=personal", ok=False).stderr)
        self.assertNotEqual(self.invoke(self.link, "apply", ok=False).returncode, 0)

    def test_reserved_enablement_settings(self):
        self.install()
        original = self.state_file.read_bytes()
        for settings in ({"features": {"hooks": False}}, {"features": {"plugins": True}},
                         {"plugins": {"example@local": {"enabled": False}}}, {"hooks": {"state": {}}},
                         {"mcp_servers": {}}, {"model_providers": {}}, {"shell_environment_policy": {}},
                         {"otel": {"exporter": {"otlp-http": {"headers": {"x-api-key": "secret"}}}}}):
            self.configure({"settings": settings})
            self.assertIn("native Codex", self.invoke(self.link, "apply", ok=False).stderr)
            self.assertEqual(self.state_file.read_bytes(), original)
        # As a launch flag, Codex would split this key and switch hooks off.
        self.configure({"settings": {"features.hooks": False}})
        self.assertIn("not a plain name", self.invoke(self.link, "apply", ok=False).stderr)
        self.assertEqual(self.state_file.read_bytes(), original)

    def test_upgrade_prunes_recorded_agent_and_rollback_restores_it(self):
        self.install()
        personal = self.codex / "agents/kk-notes.toml"
        personal.write_text("adopter owned")
        removed = self.codex / "agents/kk-eval-grader.toml"
        (self.checkout / "kk/baseline/codex/agents/eval-grader.toml").unlink()
        self.invoke(self.link, "upgrade", "--local", self.checkout)
        self.assertFalse(removed.exists())
        self.assertNotIn(str(removed), self.state()["installed_paths"])
        self.assertEqual(personal.read_text(), "adopter owned")
        self.invoke(self.link, "rollback")
        self.assertTrue(removed.is_file())
        self.assertIn(str(removed), self.state()["installed_paths"])
        self.assertEqual(personal.read_text(), "adopter owned")

    def test_partial_apply_blocks_launch_and_can_be_retried(self):
        self.install()
        self.configure({"settings": {"model": "replacement"}})
        record = self.state()
        release = self.toolbox / "releases" / record["active"]
        write = cli.state.atomic_write
        def interrupted(path, *args, **kwargs):
            if path.name == "codex-instructions.md":
                raise OSError("interrupted")
            return write(path, *args, **kwargs)
        with patch.dict(os.environ, self.env):
            plan = cli.codex_profile.prepare(release, record)
            with patch.object(cli.state, "atomic_write", interrupted), self.assertRaisesRegex(OSError, "interrupted"):
                cli.codex_profile.publish(self.toolbox, record, record["active"], plan)
        self.assertTrue(self.state()["codex_write_pending"])
        self.assertIn("changing", self.invoke(self.link, "codex", "hello", ok=False).stderr)
        with cli.state.writer(self.toolbox):
            self.assertIn("another kk writer", self.invoke(self.link, "apply", ok=False).stderr)
        self.invoke(self.link, "apply")
        self.assertNotIn("codex_write_pending", self.state())
        self.assertIn('model="replacement"', self.flags())

    def test_staged_collision_preserves_apply_and_rollback_ignores_invalid_draft(self):
        self.configure({"settings": {"model": "first"}})
        self.install()
        collision = self.codex / "agents/kk-new.toml"
        collision.write_text("personal")
        (self.checkout / "kk/baseline/codex/agents/new.toml").write_text('name = "new"\n')
        self.assertIn("already exists", self.invoke(self.link, "upgrade", "--local", self.checkout, ok=False).stderr)
        self.assertEqual(self.state()["candidate"]["phase"], "staged")
        self.configure({"settings": {"model": "first-applied"}})
        self.invoke(self.link, "apply")
        self.assertIn('model="first-applied"', self.flags())
        self.assertEqual(collision.read_text(), "personal")
        collision.rename(collision.with_suffix(".saved"))
        self.configure({"settings": {"model": "second"}})
        self.invoke(self.link, "upgrade")
        self.config.write_text("{invalid")
        broken = self.root / "bin/codex"
        broken.parent.mkdir()
        broken.write_text("#!/bin/sh\nexit 17\n")
        broken.chmod(0o755)
        self.invoke(self.link, "rollback", env=dict(self.env, PATH=str(broken.parent) + os.pathsep + self.env["PATH"]))
        self.assertIn('model="first-applied"', self.flags())
        self.assertIn("kk apply", self.invoke(self.link, "status").stderr)

    def test_interrupted_reservation_recognizes_only_its_own_file(self):
        self.install()
        destination = self.codex / "agents/kk-extra.toml"
        for linked, foreign in ((False, True), (True, False)):
            with self.subTest(linked=linked):
                record = self.state()
                with patch.object(cli.codex_profile, "reconcile_claim", return_value=None):
                    if linked:
                        cli.codex_profile.publish_new(self.toolbox, record, destination, b"toolbox")
                    else:
                        with patch("os.link", side_effect=OSError("interrupted")), self.assertRaises(OSError):
                            cli.codex_profile.publish_new(self.toolbox, record, destination, b"toolbox")
                if foreign:
                    destination.write_bytes(b"adopter")
                record = self.state()
                self.assertIn(str(destination), record["installed_paths"])
                cli.codex_profile.reconcile_claim(self.toolbox, record)
                self.assertEqual(str(destination) in self.state()["installed_paths"], linked)
                self.assertEqual(destination.read_bytes(), b"toolbox" if linked else b"adopter")
                destination.unlink()

    def test_claim_evidence_survives_interruption_after_journal_rename(self):
        self.install()
        record = self.state()
        destination = self.codex / "agents/kk-interrupted.toml"
        original = cli.state.write_json
        def interrupt(path, value):
            original(path, value)
            raise KeyboardInterrupt
        with patch.object(cli.state, "write_json", interrupt), self.assertRaises(KeyboardInterrupt):
            cli.codex_profile.publish_new(self.toolbox, record, destination, b"new")
        destination.write_bytes(b"adopter")
        cli.codex_profile.reconcile_claim(self.toolbox, self.state())
        self.assertEqual(destination.read_bytes(), b"adopter")
        self.assertNotIn(str(destination), self.state()["installed_paths"])

    def test_unreadable_override_does_not_hide_status_or_stop_launcher(self):
        self.install()
        self.config.parent.mkdir(parents=True)
        self.config.symlink_to("missing-target")
        self.assertIn("cannot check override", self.invoke(self.link, "status").stderr)
        self.assertIn("cannot check override", self.invoke(self.link, "codex", "hello").stderr)
        self.invoke(self.link, "apply", ok=False)

    def test_interactive_launch_needs_the_applied_codex_home_and_instructions(self):
        self.install()
        other = self.root / "other"
        other.mkdir()
        result = self.invoke(self.link, "codex", "hello", env=dict(self.env, CODEX_HOME=str(other)), ok=False)
        self.assertIn("different CODEX_HOME: " + json.dumps(str(self.codex)), result.stderr)
        self.assertIn("kk upgrade --local", result.stderr)
        named = self.invoke(self.link, "codex", "-p", "personal", "hello", env=dict(self.env, CODEX_HOME=str(other)))
        self.assertEqual(json.loads(named.stdout), ["-p", "personal", "hello"])
        (self.toolbox / "codex-instructions.md").unlink()
        self.assertIn("run kk apply", self.invoke(self.link, "codex", "hello", ok=False).stderr)

    def test_apply_stops_when_codex_reports_a_value_under_another_name(self):
        self.install()
        original = self.state_file.read_bytes()
        marker = "KK-SYNTHETIC-MARKER"
        self.configure({"settings": {"agents": {"max_threads": 3}, "note": marker}})
        (self.codex / "fixture-aliases.json").write_text(
            json.dumps({"agents.max_threads": "agents.max_concurrent_threads_per_session"}))
        env = dict(self.env, KK_TEST_CODEX_FIXTURES=str(self.codex))
        renamed = self.invoke(self.link, "apply", ok=False, env=env).stderr
        # kk's own default has the name Codex reports, so only the aliased key passed alone reveals it.
        self.assertIn("does not report agents.max_threads under the name kk passes; it reported "
                      "agents.max_concurrent_threads_per_session instead.", renamed)
        (self.codex / "fixture-rejects-settings").touch()
        rejected = self.invoke(self.link, "apply", ok=False, env=env).stderr
        self.assertEqual(rejected, "kk: Codex rejected debug prompt-input: error: invalid configuration\n")
        # Settings travel as arguments; an error repeats what Codex said, never the arguments.
        self.assertNotIn(marker, renamed + rejected)
        # Codex quotes a rejected value, which may read like the flag below without being about it.
        quoted = 'Error: invalid type: string "--no-daemon", expected usize'
        (self.codex / "fixture-rejects-settings").write_text(quoted)
        self.assertEqual(self.invoke(self.link, "apply", ok=False, env=env).stderr,
                         "kk: Codex rejected debug prompt-input: {}\n".format(quoted))
        # Interactive launches pass --no-daemon, so a Codex without the flag is found out here.
        (self.codex / "fixture-rejects-settings").unlink()
        self.configure({})
        (self.codex / "fixture-no-daemon-unknown").touch()
        self.assertEqual(self.invoke(self.link, "apply", ok=False, env=env).stderr,
                         "kk: kk codex passes --no-daemon to its sessions, and this Codex CLI refused it; update Codex. "
                         "Codex rejected debug prompt-input: error: unexpected argument '--no-daemon' found\n")
        self.assertEqual(self.state_file.read_bytes(), original)

    def test_apply_needs_codex_to_answer_config_read(self):
        self.install()
        original = self.state_file.read_bytes()
        (self.codex / "fixture-no-config-read").touch()
        refused = self.invoke(self.link, "apply", ok=False, env=dict(self.env, KK_TEST_CODEX_FIXTURES=str(self.codex)))
        self.assertIn("config/read, which failed: Codex has no config/read method. Run the command again; "
                      "if this Codex CLI has no config/read, update Codex", refused.stderr)
        self.assertEqual(self.state_file.read_bytes(), original)

    def test_apply_accepts_a_value_an_administrator_pins(self):
        self.install()
        # Codex reports a pinned value under the same name, with the managed layer as its origin.
        (self.codex / "fixture-managed.json").write_text(
            json.dumps({"project_doc_max_bytes": 12345, "approval_policy": "never"}))
        self.configure({"optIn": {"approval_policy": True}})
        self.invoke(self.link, "apply", env=dict(self.env, KK_TEST_CODEX_FIXTURES=str(self.codex)))
        applied = [flag.partition("=")[0] for flag in self.flags()]
        # At launch the default yields to the pin; the opt-in is passed and Codex keeps the pinned value.
        self.assertNotIn("project_doc_max_bytes", applied)
        self.assertIn("approval_policy", applied)

    def test_apply_accepts_empty_values_codex_reports_no_origin_for(self):
        self.install()
        self.configure({"settings": {"tui": {"status_line": []}, "notes": {}}})
        self.invoke(self.link, "apply")
        applied = self.flags()
        self.assertIn("notes={  }", applied)
        self.assertIn('"status_line" = []', next(flag for flag in applied if flag.startswith("tui=")))

    def test_apply_removes_the_profile_an_earlier_release_owned(self):
        self.install()
        self.profile.write_text('model = "saved by Codex"\n')
        record = self.state()
        record["installed_paths"].append(str(self.profile))
        record["codex_paths"].append(str(self.profile))
        cli.state.write_json(self.state_file, record)
        notice = "removed the managed Codex profile " + str(self.profile)
        self.assertEqual(self.invoke(self.link, "apply").stdout.count(notice), 1)
        self.assertFalse(self.profile.exists())
        record = self.state()
        self.assertNotIn(str(self.profile), record["installed_paths"] + record["codex_paths"])
        self.assertNotIn(notice, self.invoke(self.link, "apply").stdout)

    def test_workspace_path_preserves_trailing_newline(self):
        repo = self.root / "repo\n"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        self.assertEqual(cli.codex_launch.workspace_root(repo), repo)
        sub = repo / "nested" / "work"
        sub.mkdir(parents=True)
        with patch.dict(os.environ, GIT_CEILING_DIRECTORIES=str(sub.parent)):
            self.assertEqual(cli.codex_launch.workspace_root(sub), repo)

    def test_size_cap_uses_serialized_utf8_and_keeps_later_imports(self):
        self.install()
        (self.root / "AGENTS.md").write_text("@large\n@small\n")
        (self.root / "large").write_text('"' * 65000)
        (self.root / "small").write_text("small file")
        decision = cli.codex_launch.import_record(self.toolbox, self.root)
        cli.state.write_json(decision, {"paths": ["large", "small"], "approved": True})
        run = self.invoke(self.link, "codex", "hello")
        args = json.loads(run.stdout)
        self.assertIn("exceeds the import argument limit", run.stderr)
        self.assertEqual(args[-3], "-c")
        self.assertTrue(args[-2].startswith("developer_instructions="))
        self.assertNotIn("# large", args[-2])
        self.assertIn("# small", args[-2])
        self.assertLessEqual(len(args[-2].encode()), cli.codex_launch.ARG_LIMIT)

    def test_consent_follows_selected_repository_and_list(self):
        self.install()
        repo = self.root / "repo-b"
        sub = repo / "sub"
        sub.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        agents = repo / "AGENTS.md"
        agents.write_text("@notes.md\n```text\n@fenced\n```\n@../outside\n@escape\n@missing\n")
        (self.root / "outside").write_text("private outside file")
        (repo / "escape").symlink_to(self.root / "outside")
        (repo / "notes.md").write_text('quoted "text"\n@nested\n')
        (repo / "nested").write_text("nested content")
        (repo / "fenced").touch()
        with patch.dict(os.environ, self.env), patch("sys.stdin", io.StringIO("yes\n")):
            messages = io.StringIO()
            with contextlib.redirect_stderr(messages):
                flags = cli.codex_launch.import_argument(self.toolbox, repo, True)
        self.assertIn("replaces any repository", messages.getvalue())
        self.assertIn('skipped import "escape"', messages.getvalue())
        self.assertIn('skipped import "missing"', messages.getvalue())
        argument = flags[1]
        self.assertIn('# notes.md', argument)
        self.assertNotIn("nested content", argument)
        self.assertNotIn("# fenced", argument)
        self.assertNotIn("private outside file", argument)
        launch = self.invoke(self.link, "codex", "--cd=repo-b/sub", "hello")
        self.assertEqual(json.loads(launch.stdout)[-4:-2], flags)
        remote = self.invoke(self.link, "codex", "--cd=repo-b/sub", "--remote", "ws://example.invalid")
        self.assertNotIn("# notes.md", remote.stdout)
        status = subprocess.run([str(self.link), "status"], env=self.env, cwd=sub, capture_output=True, text=True)
        self.assertIn("imports: approved", status.stdout)
        with agents.open("a") as stream:
            stream.write("@second\n")
        (repo / "second").touch()
        changed = self.invoke(self.link, "codex", "-Crepo-b", "hello")
        self.assertNotIn("# notes.md", changed.stdout)
        self.assertIn("no stored approval", changed.stderr)
        with patch.dict(os.environ, self.env), patch("sys.stdin", io.StringIO("\n")):
            self.assertEqual(cli.codex_launch.import_argument(self.toolbox, repo, True), [])
        with patch.dict(os.environ, self.env), patch("sys.stdin.readline", side_effect=AssertionError("re-prompt")):
            self.assertEqual(cli.codex_launch.import_argument(self.toolbox, repo, True), [])

    @unittest.skipUnless(shutil.which("codex"), "installed Codex CLI required")
    def test_installed_codex_loads_launch_flags_and_independent_forbids(self):
        actual = shutil.which("codex")
        bin_dir = self.root / "vendor"
        bin_dir.mkdir()
        (bin_dir / "codex").symlink_to(actual)
        self.env["PATH"] = str(bin_dir) + os.pathsep + self.env["PATH"]
        self.configure({"optIn": {"nativeForbids": True, "approval_policy": True, "approvals_reviewer": True,
                                  "sandbox_mode": True}})
        # Installing checks that this Codex reports every shipped value under the name kk passes.
        self.assertIn("every Codex session", self.install().stdout)
        rules = self.codex / "rules/kk.rules"
        rendered = self.invoke(self.link, "codex", "debug", "prompt-input")
        self.assertNotIn("kk:", rendered.stderr)
        messages = json.loads(rendered.stdout)
        self.assertTrue(any(m.get("role") == "developer" and
                            "Protected files:" in str(m.get("content")) and "Tool-Name Mapping" in str(m.get("content"))
                            for m in messages))
        selected = self.root / "dir=choice"
        selected.mkdir()
        (selected / "AGENTS.md").write_text("KK_SELECTED_WORKSPACE_MARKER")
        probe = self.invoke(actual, "-Cdir=choice", "debug", "prompt-input")
        self.assertIn("KK_SELECTED_WORKSPACE_MARKER", probe.stdout)
        with patch("pathlib.Path.cwd", return_value=self.root):
            self.assertEqual(cli.codex_launch.launch_options(["-Cdir=choice", "debug"])[0], selected)
        before = self.state_file.read_bytes()
        extra = rules.with_name("personal.rules")
        extra.write_text("this is not a rules file!\n")
        rejected = self.invoke(self.link, "apply", ok=False)
        self.assertIn("personal.rules", rejected.stderr)
        self.assertEqual(self.state_file.read_bytes(), before)
        extra.unlink()
        self.configure({"settings": {"agents": {"max_concurrent_threads_per_session": "six"}}})
        self.assertIn("Codex rejected debug prompt-input", self.invoke(self.link, "apply", ok=False).stderr)
        self.configure({"settings": {"agents": {"max_threads": 3}}})
        self.assertIn("does not report agents.max_threads under the name kk passes; it reported "
                      "agents.max_concurrent_threads_per_session instead.",
                      self.invoke(self.link, "apply", ok=False).stderr)
        self.assertEqual(self.state_file.read_bytes(), before)
        self.assertTrue(rules.is_file())
        self.configure({})
        self.invoke(self.link, "apply")
        self.assertFalse(rules.exists())
        self.assertNotIn(str(rules), self.state()["installed_paths"])
        extra.write_text('prefix_rule(pattern=["sudo"], decision="forbidden")\n')
        baseline = self.toolbox / "releases" / self.state()["active"] / "kk/baseline/codex/kk.rules"
        baseline.write_text(baseline.read_text().replace('pattern = ["sudo"]', 'pattern = ["other"]')
                            .replace('"sudo rm -rf /","sudo apt install x"', '"other"'))
        self.configure({"optIn": {"nativeForbids": True}})
        self.assertIn("does not forbid sudo", self.invoke(self.link, "apply", ok=False).stderr)
        self.assertFalse(rules.exists())
        self.assertTrue(extra.is_file())

    def test_toml_round_trip(self):
        try:
            import tomllib
        except ImportError:
            self.skipTest("tomllib unavailable")
        baseline, explicit, instructions, native = cli.codex_profile.compose(ROOT, {})
        settings = cli.codex_profile.merge([*baseline, (("developer_instructions",), instructions)])
        values = tomllib.loads("\n".join(cli.codex_profile.config_flags(settings)[1::2]))
        self.assertEqual(values.pop("developer_instructions"), instructions)
        self.assertEqual(values, json.loads((ROOT / "kk/baseline/codex.json").read_text())["profile"])
        self.assertEqual((explicit, native), ([], False))
        data = {"key.with.dots": [{"quoted": '😀\n"\\\x7f'}]}
        self.assertEqual(tomllib.loads("sample = " + cli.codex_profile.toml_value(data))["sample"], data)
