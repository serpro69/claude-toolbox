from argparse import Namespace
import json
import os
from pathlib import Path
import pty
import shutil
import subprocess
import sys
import tarfile
import unittest
from unittest.mock import patch

from test_install import InstallFixture, cli


class CodexActivation(InstallFixture):
    def setUp(self):
        super().setUp()
        self.directory = Path(self.env["CODEX_HOME"])

    def guard_version(self):
        return next((self.directory / "plugins/cache/toolbox/kk-guard").iterdir()).name

    def confirm_upgrade(self, *, ok=True):
        master, slave = pty.openpty()
        try:
            os.write(master, b"yes\n")
            result = subprocess.run([self.link, "upgrade"], env=self.env, cwd=self.root, stdin=slave,
                                    capture_output=True, text=True, timeout=45)
        finally:
            os.close(slave)
            os.close(master)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result

    def change_guard(self):
        with (self.checkout / "kodex-guard/scripts/pretooluse-bash.sh").open("a") as f:
            f.write("\n# fixture release B\n")

    def test_guard_identity_confirmation_and_mixed_rollback_target(self):
        self.install()
        first = self.state()["active"]
        reviewed = self.guard_version()
        self.assertRegex(reviewed, r"\+kk\.[0-9a-f]{12}$")
        (self.directory / "fixture-reviewed").write_text(reviewed)
        self.change_guard()
        declined = self.invoke(self.link, "upgrade", "--local", self.checkout, ok=False)
        self.assertIn("guard change declined", declined.stderr)
        self.assertEqual(self.state()["candidate"]["phase"], "staged")
        self.assertEqual(self.guard_version(), reviewed)
        self.assertIn("awaiting review", self.confirm_upgrade().stdout)
        second = self.state()["active"]
        changed = self.guard_version()
        self.assertNotEqual(changed, reviewed)
        for folder, manifest in (("klaude-plugin", ".claude-plugin"), ("kodex-plugin", ".codex-plugin")):
            path = self.checkout / folder / manifest / "plugin.json"
            data = json.loads(path.read_text())
            data["version"] = "1.2.3"
            path.write_text(json.dumps(data))
        adds = self.directory / "fixture-adds"
        before = adds.read_text()
        self.invoke(self.link, "upgrade", "--local", self.checkout)
        self.assertEqual(adds.read_text(), before + "kk 1.2.3\n")
        self.assertEqual(self.state()["rollback_target"], first)
        recovery = self.invoke(self.link, "rollback")
        self.assertIn("Continuing offline recovery", recovery.stderr)
        self.assertIn("codex: ready", recovery.stdout)
        self.assertEqual(self.guard_version(), reviewed)
        self.assertTrue((self.toolbox / "releases" / second).is_dir())

    def test_unreviewed_fallback_and_interrupted_vendor_commit(self):
        self.install()
        first = self.state()["active"]
        self.change_guard()
        self.invoke(self.link, "upgrade", "--local", self.checkout, ok=False)
        interrupt = self.directory / "interrupt-add-kk-guard"
        interrupt.touch()
        self.confirm_upgrade(ok=False)
        self.assertEqual(self.state()["candidate"]["step"], "codex-add-kk-guard")
        count = (self.directory / "fixture-adds").read_text()
        interrupt.unlink()
        self.invoke(self.link, "upgrade")
        self.assertEqual((self.directory / "fixture-adds").read_text(), count)
        self.assertEqual(self.state()["rollback_target"], first)
        result = self.invoke(self.link, "rollback")
        self.assertIn("codex previously awaiting review", result.stdout)
        self.assertIn("codex: awaiting review", result.stdout)

    def test_workspace_and_later_disablement_override_machine_readiness(self):
        self.install()
        (self.directory / "fixture-reviewed").write_text(self.guard_version())
        self.invoke(self.link, "apply")
        self.assertIn("codex: ready", self.invoke(self.link, "status").stdout)
        sub = self.root / "other"
        sub.mkdir()
        (sub / "fixture-guard-off").touch()
        self.assertIn("absent", self.invoke(self.link, "codex", "exec", "-Cother", "hello", ok=False).stderr)
        self.assertIn("absent", self.invoke(self.link, "codex", "-cfeatures.hooks=false", "review", ok=False).stderr)
        self.invoke(self.link, "codex", "exec", "hello")
        (self.directory / "disabled-1").touch()
        self.assertIn("disabled", self.invoke(self.link, "codex", "exec", "hello", ok=False).stderr)
        self.assertIn("awaiting review", self.invoke(self.link, "status").stdout)
        self.assertIn("cannot verify", self.invoke(self.link, "codex", "-pother", "exec", ok=False).stderr)
        self.assertIn("cannot verify", self.invoke(self.link, "codex", "exec", "resume", ok=False).stderr)
        with (self.directory / "kk.config.toml").open("a") as profile:
            profile.write("\n[features]\nhooks = false\n")
        self.assertIn("managed Codex profile", self.invoke(self.link, "codex", "-pkk", "exec", ok=False).stderr)

    def test_tag_collision_and_same_identity_across_local_and_tagged_versions(self):
        self.install()
        guard = self.checkout / "kodex-guard"
        version = self.guard_version()
        actual = next((self.directory / "plugins/cache/toolbox/kk-guard").iterdir())
        verified = cli.codex_plugins.verify_tree("kk-guard", guard, self.directory, version, actual)
        self.assertEqual(verified["version"], version)
        manifest = guard / ".codex-plugin/plugin.json"
        manifest.write_bytes(cli.codex_plugins.with_version(manifest.read_bytes(), version))
        self.change_guard()
        with self.assertRaisesRegex(ValueError, "changed under installed version"):
            cli.codex_plugins.stage_guard(self.checkout, self.state(), self.directory, False)

    def tagged_archive(self):
        archive = self.root / "release.tar"
        with tarfile.open(archive, "w") as stream:
            stream.add(self.checkout, "release")
        tag = "v" + json.loads((self.checkout / "kodex-plugin/.codex-plugin/plugin.json").read_text())["version"]
        return tag, archive

    @unittest.skipUnless(shutil.which("codex"), "installed Codex CLI required")
    def test_real_codex_same_version_skills_edit_and_tag_after_local(self):
        real_bin = self.root / "real-bin"
        real_bin.mkdir()
        (real_bin / "codex").symlink_to(shutil.which("codex"))
        self.env["PATH"] = str(real_bin) + os.pathsep + self.env["PATH"]
        skills = self.checkout / "kodex-plugin/skills"
        skills.mkdir()
        note = skills / "fixture.txt"
        note.write_text("first")
        self.install()
        first = self.state()["active"]
        guard = next((self.directory / "plugins/cache/toolbox/kk-guard").iterdir())
        with (guard / ".codex-plugin/plugin.json").open("rb") as held:
            note.write_text("second")
            tag, archive = self.tagged_archive()
            active = cli.load_cli(self.toolbox / "releases" / first / "kk/lib", "_local_to_tag")
            with patch.dict(os.environ, self.env), patch.object(sys, "argv", ["kk", "upgrade", "--version", tag]):
                with archive.open("rb") as stream, patch.object(active.payload, "urlopen", return_value=stream):
                    self.assertEqual(active.main(), 0)
            self.assertTrue(os.path.samestat(os.fstat(held.fileno()), (guard / ".codex-plugin/plugin.json").stat()))
        cache = self.directory / "plugins/cache/toolbox/kk" / tag[1:]
        self.assertEqual((cache / "skills/fixture.txt").read_text(), "second")
        self.assertEqual(self.state()["active"], tag)
        self.invoke(self.link, "rollback")
        self.assertEqual((cache / "skills/fixture.txt").read_text(), "first")

    def test_adding_codex_to_an_already_active_tag(self):
        tag, archive = self.tagged_archive()
        claude_only = self.root / "claude-only"
        claude_only.mkdir()
        (claude_only / "claude").symlink_to(Path(__file__).with_name("claude"))
        env = dict(self.env, PATH=str(claude_only) + os.pathsep + os.defpath, KK_REPOSITORY="fixture/fork")
        self.assertIsNone(shutil.which("codex", path=env["PATH"]))
        with patch.dict(os.environ, env), cli.state.writer(self.toolbox):
            cli.install_locked(self.toolbox, Namespace(command="install", local=None, version=tag), archive_file=archive)
        self.assertNotIn("codex", self.state()["releases"][tag]["tools"])
        hint = "KK_REPOSITORY=fixture/fork kk upgrade --version " + tag
        self.assertIn(hint, self.invoke(self.link, "status").stdout)
        self.assertIn(hint, self.invoke(self.link, "codex", "exec", ok=False).stderr)
        self.directory.mkdir(exist_ok=True)
        interrupted = self.directory / "interrupt-add-kk-guard"
        interrupted.touch()
        self.invoke(self.link, "upgrade", "--version", tag, env=dict(self.env, KK_REPOSITORY="fixture/fork"), ok=False)
        self.assertIn("kk status for recovery options", self.invoke(self.link, "upgrade", "--local", self.checkout, ok=False).stderr)
        self.assertIn("Resume offline with kk upgrade", self.invoke(self.link, "rollback", ok=False).stderr)
        self.assertEqual(self.state()["candidate"]["operation"], "add-codex")
        interrupted.unlink()
        self.invoke(self.link, "upgrade")
        self.assertIsNone(self.state()["candidate"])
        self.assertEqual(self.state()["active"], tag)
        self.assertIn("untrusted", self.invoke(self.link, "status").stdout)
        self.assertTrue(self.guard_version())

    def test_relative_vendor_path_and_previously_reviewed_rollback_target(self):
        self.install()
        (self.directory / "fixture-reviewed").write_text(self.guard_version())
        self.invoke(self.link, "upgrade", "--local", self.checkout)
        second = self.state()["active"]
        bin_dir = self.root / "relative-bin"
        bin_dir.mkdir()
        (bin_dir / "codex").symlink_to(Path(__file__).with_name("codex"))
        workspace = self.root / "different-workspace"
        workspace.mkdir()
        env = dict(self.env, PATH="relative-bin:/usr/bin:/bin")
        self.invoke(self.link, "codex", "-C", workspace, "exec", "hello", env=env)
        (self.directory / "disabled-1").touch()
        self.invoke(self.link, "upgrade", "--local", self.checkout)
        self.assertEqual(self.state()["rollback_target"], second)
        self.assertIn("disabled", self.invoke(self.link, "rollback").stdout)

    def test_broken_vendor_leaves_changed_plugins_pending_after_file_restore(self):
        self.install()
        agent = "kk-eval-grader.toml"
        first = self.state()["active"]
        (self.checkout / "kk/baseline/codex/agents/eval-grader.toml").unlink()
        self.change_guard()
        self.invoke(self.link, "upgrade", "--local", self.checkout, ok=False)
        self.confirm_upgrade()
        self.assertFalse((self.directory / "agents" / agent).exists())
        vendor_bin = self.root / "broken-vendor"
        vendor_bin.mkdir()
        (vendor_bin / "codex").symlink_to(shutil.which("false"))
        env = dict(self.env, PATH=str(vendor_bin) + os.pathsep + self.env["PATH"])
        result = self.invoke(self.link, "rollback", env=env, ok=False)
        self.assertIn("Codex plugin recovery is pending", result.stderr)
        self.assertTrue((self.directory / "agents" / agent).is_file())
        self.assertEqual(self.state()["candidate"]["step"], "codex-restore-plugins")
        self.invoke(self.link, "rollback")
        self.assertEqual(self.state()["active"], first)

    def test_registered_adapter_is_exercised_before_activation(self):
        path = self.checkout / "kodex-guard/hooks/hooks.json"
        hooks = json.loads(path.read_text())
        hooks["hooks"]["PreToolUse"][1]["hooks"][0]["command"] = "true"
        path.write_text(json.dumps(hooks))
        self.assertIn("guard self-test expected secrets for apply_patch", self.install(ok=False).stderr)
        self.assertFalse((self.toolbox / ".agents").exists())

    def test_managed_is_not_trusted_and_method_absence_requires_acknowledgement(self):
        env = patch.dict(os.environ, self.env)
        env.start()
        self.addCleanup(env.stop)
        groups = json.loads((self.checkout / "kodex-guard/hooks/hooks.json").read_text())["hooks"]["PreToolUse"]
        hooks = [dict(group["hooks"][0], key="kk-guard@toolbox:hooks/hooks.json:pre_tool_use:{}:0".format(i),
                      pluginId="kk-guard@toolbox", source="plugin", matcher=group["matcher"],
                      enabled=True, trustStatus="managed") for i, group in enumerate(groups)]
        trust = cli.codex_trust
        with patch.object(trust, "hooks", return_value=hooks):
            phase, messages = trust.check(self.checkout, self.directory, self.root)
            self.assertEqual(phase, "awaiting review")
            self.assertEqual(len(messages), len(groups))
        with patch.object(trust, "hooks", side_effect=trust.NoTrustMethod), patch.object(trust.mixed, "inspect", return_value=([], [])):
            self.assertEqual(trust.check(self.checkout, self.directory, self.root)[0], "awaiting review")
            with patch("sys.stdin.isatty", return_value=True), patch("sys.stdin.readline", return_value="yes\n"):
                self.assertEqual(trust.check(self.checkout, self.directory, self.root, prompt=True)[0], "unverified")
