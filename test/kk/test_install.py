import ast
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("kk_loader", ROOT / "kk/lib/run.py")
loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loader)
cli = loader.load_cli(ROOT / "kk/lib", "_kk_tests")


class InstallFixture(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.home = self.root / "user home"
        self.home.mkdir()
        self.toolbox = self.home / "data" / "kk"
        self.env = dict(os.environ, HOME=str(self.home), KK_HOME=str(self.toolbox),
                        CODEX_HOME=str(self.home / ".codex"), XDG_CONFIG_HOME=str(self.home / ".config"),
                        PATH=str(ROOT / "test/kk") + os.pathsep + os.environ["PATH"])
        self.link = self.home / ".local/bin/kk"
        self.state_file = self.toolbox / "state.json"
        self.checkout = self.root / "checkout"
        self.standalone = self.root / "install.sh"
        shutil.copy2(ROOT / "install.sh", self.standalone)
        # Keep the real guard and registration. Trim unrelated skill content
        # in negative cases; the success case also installs the full checkout.
        for name in ("kk", "klaude-plugin/scripts/guard", "klaude-plugin/.claude-plugin",
                     "klaude-plugin/hooks", "klaude-plugin/instructions", "kodex-plugin/.codex-plugin", "kodex-guard"):
            shutil.copytree(ROOT / name, self.checkout / name)

    def invoke(self, *args, ok=True, env=None):
        result = subprocess.run(list(map(str, args)), cwd=self.root, env=env or self.env,
                                stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=45)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result

    def install(self, *args, ok=True):
        return self.invoke(ROOT / "install.sh", "--local", self.checkout, *args, ok=ok)

    def state(self):
        return json.loads(self.state_file.read_text())


class FirstInstall(InstallFixture):
    def test_first_install_full_checkout_and_dispatch(self):
        self.invoke(ROOT / "install.sh", "--local", ROOT)
        state = self.state()
        release = self.toolbox / "releases" / state["active"]
        self.assertTrue((release / "klaude-plugin/skills/implement/shared-change-context.md").is_symlink())
        self.assertEqual(self.link.resolve(), self.toolbox / "bin/kk")
        self.assertIn(str(self.link), state["installed_paths"])
        self.assertIsNone(state["candidate"])
        self.assertIn("claude: ready", self.invoke(self.link, "status").stdout)
        shell_env = self.env.copy()
        del shell_env["KK_HOME"]
        self.assertIn(state["active"], self.invoke(self.link, "status", env=shell_env).stdout)
        self.invoke(ROOT / "install.sh", "--local", ROOT)
        self.assertEqual(self.state(), state)

    def test_resume_after_vendor_commits_install(self):
        (self.home / "interrupt").touch()
        self.install(ok=False)
        pending = self.state()
        self.assertIsNone(pending["active"])
        self.assertEqual(pending["candidate"]["phase"], "activating")
        self.assertFalse(self.link.exists())
        (self.home / "interrupt").unlink()
        self.invoke(self.standalone)  # No adjacent bootstrap, network or source arguments.
        self.assertEqual(self.state()["active"], pending["candidate"]["version"])
        calls = [json.loads(row) for row in (self.home / "calls").read_text().splitlines()]
        self.assertEqual(sum(args[:2] == ["plugin", "install"] for args in calls), 1)

    def test_rebuild_missing_pending_candidate(self):
        (self.home / "interrupt").touch()
        self.install(ok=False)
        old = self.state()["candidate"]["version"]
        # The stable dispatcher may already have been published before promotion.
        entry = self.toolbox / "bin/kk"
        entry.parent.mkdir()
        shutil.copy2(ROOT / "kk/bin/kk", entry)
        shutil.rmtree(self.toolbox / "releases" / old)
        (self.home / "interrupt").unlink()
        self.invoke(self.standalone)
        self.assertNotEqual(self.state()["active"], old)
        self.assertIn("claude: ready", self.invoke(self.link, "status").stdout)

    def test_broken_engine_and_registered_command_fail_before_state_change(self):
        self.toolbox.mkdir(parents=True)
        original = cli.state.load(self.toolbox)
        original["extension"] = {"kept": True}
        cli.state.write_json(self.state_file, original)
        before = self.state_file.read_bytes()
        engine = self.checkout / "klaude-plugin/scripts/guard/guard.py"
        engine.write_text("invalid python !\n")
        self.assertIn("self-test", self.install(ok=False).stderr)
        self.assertEqual(self.state_file.read_bytes(), before)
        shutil.copy2(ROOT / "klaude-plugin/scripts/guard/guard.py", engine)
        hooks = self.checkout / "klaude-plugin/hooks/hooks.json"
        config = json.loads(hooks.read_text())
        config["hooks"]["PreToolUse"][0]["hooks"][0]["command"] = 'bash "${CLAUDE_PLUGIN_ROOT}/missing"'
        hooks.write_text(json.dumps(config))
        self.assertIn("self-test", self.install(ok=False).stderr)
        self.assertEqual(self.state_file.read_bytes(), before)
        self.assertFalse((self.home / "market").exists())

    def test_broken_candidate_cli_and_dispatcher_fail_before_activating(self):
        for name, invalid in (("lib/cli.py", "bad syntax !"), ("bin/kk", "if true; then"),
                              ("bin/kk", "#!/bin/sh\nexit 0\n")):
            with self.subTest(name=name):
                path = self.checkout / "kk" / name
                path.write_text(invalid)
                self.install(ok=False)
                self.assertFalse(self.state_file.exists())
                self.assertFalse((self.home / "market").exists())
                shutil.copy2(ROOT / "kk" / name, path)

    def test_modified_pending_payload_rebuilt_before_first_promotion(self):
        (self.home / "interrupt").touch()
        self.install(ok=False)
        previous = self.state()["candidate"]["version"]
        release = self.toolbox / "releases" / previous
        (release / "kk/lib/cli.py").write_text("raise RuntimeError('broken candidate CLI')")
        os.mkfifo(release / "unexpected-special-file")
        (self.home / "interrupt").unlink()
        self.invoke(self.standalone)
        self.assertNotEqual(self.state()["active"], previous)

    def test_explicit_checkout_replaces_pending_first_install(self):
        (self.home / "interrupt").touch()
        self.install(ok=False)
        previous = self.state()["candidate"]["version"]
        replacement = self.root / "fixed checkout"
        shutil.copytree(self.checkout, replacement)
        (self.home / "interrupt").unlink()
        self.invoke(self.standalone, "--local", replacement)
        self.assertNotEqual(self.state()["active"], previous)
        self.assertTrue((self.toolbox / "releases" / previous).is_dir())

    def test_wrong_or_missing_vendor_path_blocks_promotion(self):
        override = self.home / "list-override"
        for value in (None, str(self.root)):
            override.write_text(json.dumps({"readFromFolder": value}))
            self.assertIn("readFromFolder", self.install(ok=False).stderr)
            self.assertIsNone(self.state()["active"])
        override.unlink()
        self.install()

    def test_payload_requires_all_directories_and_matching_versions(self):
        guard = self.checkout / "kodex-guard"
        guard.rename(self.root / "held-guard")
        self.assertIn("missing payload directory", self.install(ok=False).stderr)
        (self.root / "held-guard").rename(guard)
        guard_manifest = guard / ".codex-plugin/plugin.json"
        original = guard_manifest.read_bytes()
        guard_manifest.write_text("[]")
        self.assertIn("invalid Codex guard manifest", self.install(ok=False).stderr)
        guard_manifest.write_bytes(original)
        manifest = self.checkout / "kodex-plugin/.codex-plugin/plugin.json"
        plugin = json.loads(manifest.read_text())
        plugin["version"] = "0.0.0"
        manifest.write_text(json.dumps(plugin))
        self.assertIn("versions disagree", self.install(ok=False).stderr)
        shutil.rmtree(self.checkout / "kodex-plugin")
        self.assertIn("missing payload directory", self.install(ok=False).stderr)
        self.assertFalse(self.state_file.exists())
        self.assertFalse((self.home / "calls").exists())

    def test_non_object_journal_is_preserved(self):
        self.toolbox.mkdir(parents=True)
        self.state_file.write_text("[]")
        self.assertIn("kk: unsupported kk state format", self.install(ok=False).stderr)
        self.assertEqual(self.state_file.read_text(), "[]")

    def test_external_link_collision_and_marketplace_collision(self):
        self.link.parent.mkdir(parents=True)
        self.link.symlink_to(self.root / "absent")
        self.assertIn("already exists", self.install(ok=False).stderr)
        self.assertTrue(self.link.is_symlink())
        self.assertFalse(self.state_file.exists())
        self.assertFalse((self.home / "calls").exists())
        self.link.unlink()
        market = self.home / "market"
        other = json.dumps({"name": cli.claude.MARKETPLACE, "installLocation": str(self.root)})
        market.write_text(other)
        self.assertIn("another source", self.install(ok=False).stderr)
        self.assertEqual(market.read_text(), other)
        self.assertFalse(self.link.exists())

    def test_second_writer_and_state_format(self):
        with cli.state.writer(self.toolbox):
            held = (self.toolbox / "lock").read_bytes()
            self.assertIn("another kk writer", self.install(ok=False).stderr)
            self.assertEqual((self.toolbox / "lock").read_bytes(), held)
            self.assertFalse(self.state_file.exists())
        original = cli.state.load(self.toolbox)
        original["format_version"] += 1
        cli.state.write_json(self.state_file, original)
        before = self.state_file.read_bytes()
        self.assertIn("unsupported kk state", self.install(ok=False).stderr)
        self.assertEqual(self.state_file.read_bytes(), before)
        self.assertFalse((self.home / "calls").exists())

    def test_atomic_state_and_extensions(self):
        record = cli.state.load(self.toolbox)
        record["extension"] = ["keep"]
        cli.state.write_json(self.state_file, record)
        with patch.object(cli.state.os, "replace", side_effect=OSError("rename failed")):
            with self.assertRaisesRegex(OSError, "rename failed"):
                cli.state.write_json(self.state_file, {})
        self.assertEqual(self.state(), record)
        self.install()
        self.assertEqual(self.state()["extension"], ["keep"])

    def test_rollback_target_and_dispatch(self):
        record = cli.state.load(self.toolbox)
        for version in ("v1.0.0", "v2.0.0"):
            cli.state.promote(record, version)
        previous = "v1.0.0"
        current = "v2.0.0"
        self.assertIsNotNone(record["releases"][previous]["superseded_at"])
        pending = copy.deepcopy(record)
        pending["releases"][current]["tools"]["codex"] = "awaiting review"
        cli.state.promote(pending, "v3.0.0")
        self.assertEqual(pending["rollback_target"], previous)
        pending["releases"][previous]["tools"]["codex"] = "awaiting review"
        pending["releases"]["v3.0.0"]["tools"]["codex"] = "awaiting review"
        cli.state.promote(pending, "v4.0.0")
        self.assertEqual(pending["rollback_target"], "v3.0.0")
        for version in (previous, current):
            runner = self.toolbox / "releases" / version / "kk/lib/run.py"
            runner.parent.mkdir(parents=True)
            runner.write_text("import sys\nassert sys.flags.isolated\nprint(" + repr(version) + ")\n")
        cli.state.write_json(self.state_file, record)
        self.assertEqual(self.invoke(ROOT / "kk/bin/kk", "rollback").stdout.strip(), previous)
        record["candidate"] = {"phase": "activating", "version": "v3.0.0"}
        cli.state.write_json(self.state_file, record)
        self.assertEqual(self.invoke(ROOT / "kk/bin/kk", "rollback").stdout.strip(), current)

    def test_path_shadow_warning(self):
        shadow = self.root / "kk"
        shadow.write_text("#!/bin/sh\nexit 1\n")
        shadow.chmod(0o755)
        env = dict(self.env, PATH=str(self.root) + os.pathsep + self.env["PATH"])
        result = self.invoke(ROOT / "install.sh", "--local", self.checkout, env=env)
        self.assertIn(str(shadow), result.stderr)

    def test_floor_syntax(self):
        # The entry points report the floor, so they must load on interpreters below it,
        # down to a distribution's 3.6. ast cannot see future features, so check that too.
        # Python 3.13+ documents (3, 7) as its lowest grammar version; the 3.9 CI job checks 3.6.
        entry = (3, 6) if sys.version_info < (3, 13) else (3, 7)
        for path in (ROOT / "kk/lib").glob("*.py"):
            with self.subTest(path=path):
                version = entry if path.name == "run.py" else (3, 9)
                ast.parse(path.read_text(), filename=str(path), feature_version=version)
        installer = (ROOT / "install.sh").read_text()
        bootstrap = installer.split("<<'PY'\n", 1)[1].rsplit("\nPY\n", 1)[0]
        ast.parse(bootstrap, filename="install.sh", feature_version=entry)
        for name, source in (("run.py", (ROOT / "kk/lib/run.py").read_text()), ("install.sh", bootstrap)):
            with self.subTest(entry_point=name):
                self.assertFalse([node for node in ast.walk(ast.parse(source))
                                  if isinstance(node, ast.ImportFrom) and node.module == "__future__"])

    def test_entry_point_refuses_python_below_the_floor(self):
        run = runpy.run_path(str(ROOT / "kk/lib/run.py"))
        with patch.object(sys, "version_info", (3, 8, 20, "final", 0)):
            with self.assertRaises(SystemExit) as raised:
                run["require_python"]()
        self.assertEqual(str(raised.exception), "kk: Python 3.9 or newer is required; 3.8.20 found")

    def test_archive_round_trip_and_tag_validation(self):
        archive = self.root / "release.tar"
        symlink = self.checkout / "kk/selftest/alias"
        symlink.symlink_to("guard-cases.json")
        with tarfile.open(archive, "w") as tar:
            tar.add(self.checkout, "release")
            tar.add(__file__, "release/irrelevant")
        version = json.loads((self.checkout / "klaude-plugin/.claude-plugin/plugin.json").read_text())["version"]
        with patch.dict(os.environ, self.env), patch.object(sys, "argv", ["kk", "upgrade", "--version", "v" + version]):
            with patch.object(cli.payload, "urlopen", return_value=archive.open("rb")) as download:
                self.assertEqual(cli.main(), 0)
            download.assert_called_once_with(cli.payload.api_root(self.env.get("KK_REPOSITORY", "serpro69/agentstakk"))
                                             + "/tarball/v" + version, timeout=60)
        installed = self.toolbox / "releases" / self.state()["active"]
        self.assertTrue((installed / "kk/selftest/alias").is_symlink())
        self.assertFalse((installed / "irrelevant").exists())
        identity = [sys.executable, "-I", "-B", str(installed / "kk/lib/guard_identity.py")]
        self.assertEqual(self.invoke(*identity, self.checkout / "kodex-guard").stdout,
                         self.invoke(*identity, installed / "kodex-guard").stdout)

    def standalone_downloads(self):
        # The actual standalone installer owns argument parsing, extraction and
        # locking. Substitute only the two GitHub HTTP responses before it runs.
        archive = self.root / "source.tar.gz"
        version = "v" + json.loads((self.checkout / "klaude-plugin/.claude-plugin/plugin.json").read_text())["version"]
        with tarfile.open(archive, "w:gz") as tar:
            tar.add(self.checkout, "repo-commit")
        journal = self.root / "urls"
        python = self.root / "python3"
        python.write_text("#!" + sys.executable + " -I\n" + """
import io, json, os, sys
from pathlib import Path
from unittest.mock import patch
if sys.argv[1:4] != ["-I", "-B", "-"]:
    os.execv(sys.executable, [sys.executable] + sys.argv[1:])
def download(url, timeout):
    with Path(os.environ["KK_TEST_URLS"]).open("a") as log:
        print(url, file=log)
    if url.endswith("/releases/latest"):
        return io.BytesIO(json.dumps({"tag_name": os.environ["KK_TEST_TAG"]}).encode())
    return Path(os.environ["KK_TEST_ARCHIVE"]).open("rb")
sys.dont_write_bytecode = True  # Match the real interpreter's -B during bootstrap.
sys.argv = sys.argv[3:]
with patch("urllib.request.urlopen", download):
    exec(compile(sys.stdin.read(), "install.sh", "exec"), {"__name__": "__main__"})
""")
        python.chmod(0o755)
        env = dict(self.env, PATH=str(self.root) + os.pathsep + self.env["PATH"],
                   KK_TEST_URLS=str(journal), KK_TEST_TAG=version, KK_TEST_ARCHIVE=str(archive))
        return env, version, journal

    def test_standalone_latest_and_recovery_from_original_fork(self):
        env, version, journal = self.standalone_downloads()
        env["KK_REPOSITORY"] = "example/fork"
        (self.home / "interrupt").touch()
        self.invoke(self.standalone, env=env, ok=False)
        self.assertEqual(self.state()["candidate"]["source"], {"tag": version, "repository": "example/fork"})
        before = self.state_file.read_bytes()
        other = dict(env, KK_REPOSITORY="other/fork")
        self.assertIn("retained release", self.invoke(self.standalone, "--version", version, env=other, ok=False).stderr)
        self.assertEqual(self.state_file.read_bytes(), before)
        shutil.rmtree(self.toolbox / "releases" / version)
        del env["KK_REPOSITORY"]
        (self.home / "interrupt").unlink()
        self.invoke(self.standalone, env=env)
        api = "https://api.github.com/repos/example/fork/"
        self.assertEqual(journal.read_text().splitlines(), [
            api + "releases/latest", api + "tarball/" + version,
            "https://api.github.com/repos/other/fork/tarball/" + version, api + "tarball/" + version])
        self.assertEqual(self.state()["active"], version)

    def test_standalone_default_and_old_canonical_source(self):
        env, version, urls = self.standalone_downloads()
        env.pop("KK_REPOSITORY", None)
        (self.home / "interrupt").touch()
        self.invoke(self.standalone, env=env, ok=False)
        api = "https://api.github.com/repos/serpro69/agentstakk/"
        self.assertEqual(urls.read_text().splitlines(), [api + "releases/latest", api + "tarball/" + version])
        record = self.state()
        self.assertEqual(record["candidate"]["source"]["repository"], "serpro69/agentstakk")
        record["candidate"]["source"]["repository"] = "serpro69/claude-toolbox"
        cli.state.write_json(self.state_file, record)
        (self.home / "interrupt").unlink()
        self.invoke(self.standalone, "--version", version, env=env)
        self.assertIn("Already active", self.invoke(self.link, "upgrade", "--version", version, env=env).stdout)
        self.assertEqual(urls.read_text().splitlines(), [api + "releases/latest", api + "tarball/" + version])

    def test_archive_rejects_out_of_bounds_names_and_links(self):
        for name, link in (("/absolute", None), ("release/kk/../other", None),
                           ("release/kk/link", "../../outside"), ("release/kk/link", "/outside")):
            with self.subTest(name=name, link=link), tempfile.TemporaryDirectory() as destination:
                buffer = io.BytesIO()
                with tarfile.open(fileobj=buffer, mode="w") as tar:
                    info = tarfile.TarInfo(name)
                    if link:
                        info.type = tarfile.SYMTYPE
                        info.linkname = link
                    tar.addfile(info)
                buffer.seek(0)
                with self.assertRaisesRegex(ValueError, "unsafe archive|absolute link|escaping payload"):
                    cli.payload.extract(buffer, Path(destination), ["kk"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
