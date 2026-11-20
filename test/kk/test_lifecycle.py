import json
import os
from pathlib import Path
import shlex
import shutil
import sys
import tarfile
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from test_install import InstallFixture, cli


class ClaudeLifecycle(InstallFixture):
    def setUp(self):
        super().setUp()
        self.trace = self.home / "trace"
        self.stop = self.home / "stop-at"
        self.second = self.root / "second"
        shutil.copytree(self.checkout, self.second)
        for source, label in ((self.checkout, "A"), (self.second, "B")):
            self.instrument(source, label)
        self.install()
        self.first_id = self.state()["active"]

    def instrument(self, source, label):
        # Only fixture releases have these wrappers. Abrupt exit leaves the
        # real on-disk journal and vendor side effects for another process.
        modules = {"state": ("checkpoint", "write_json"), "payload": ("stage",),
                   "validation": ("validate",), "cli": ("finish_install", "status", "rollback_locked", "complete_publication")}
        for module, functions in modules.items():
            with (source / "kk/lib" / (module + ".py")).open("a") as stream:
                stream.write("""
import os
from pathlib import Path
def traced(fn):
    def call(*args, **kwargs):
        real_home = Path(os.environ["HOME"])
        with (real_home / "trace").open("a") as log:
            print(%r, fn.__name__, file=log)
        stop = real_home / "stop-at"
        marker = stop.read_text() if stop.exists() else None
        if marker == "publish-dispatcher" and fn.__name__ == "complete_publication":
            os._exit(79)
        if (marker == "published-dispatcher" and fn.__name__ == "write_json"
                and "pending_entry" not in args[1] and args[0].exists()
                and "pending_entry" in json.loads(args[0].read_bytes())):
            os._exit(79)
        result = fn(*args, **kwargs)
        if fn.__name__ == "checkpoint" and stop.exists() and stop.read_text() == args[2]:
            os._exit(79)
        return result
    return call
""" % label)
                for name in functions:
                    stream.write("{0} = traced({0})\n".format(name))
        with (source / "kk/bin/kk").open("a") as stream:
            stream.write("\n# fixture release {}\n".format(label))

    def release(self, version):
        return self.toolbox / "releases" / version

    def upgrade(self, ok=True):
        return self.invoke(self.link, "upgrade", "--local", self.second, ok=ok)

    def check_active(self, version, label):
        record = self.state()
        self.assertEqual(record["active"], version)
        self.assertIsNone(record["candidate"])
        manifest = json.loads((self.toolbox / ".claude-plugin/marketplace.json").read_text())
        self.assertEqual(self.toolbox / manifest["plugins"][0]["source"], self.release(version) / "klaude-plugin")
        self.assertIn("# fixture release " + label, self.link.read_text())

    def test_interrupt_each_activation_step_and_recover(self):
        snapshot = self.root / "snapshot"
        shutil.copytree(self.home, snapshot, symlinks=True)
        for step in ("place", "marketplace", "register", "install-plugin", "verify", "entry-point", "entry-link", "promote"):
            for recovery in ("upgrade", "rollback"):
                with self.subTest(step=step, recovery=recovery):
                    shutil.rmtree(self.home)
                    shutil.copytree(snapshot, self.home, symlinks=True)
                    self.trace.write_text("")
                    if step == "register":
                        (self.home / "market").unlink()
                    if step == "install-plugin":
                        (self.home / "plugin").unlink()
                    self.stop.write_text(step)
                    self.assertEqual(self.upgrade(ok=False).returncode, 79)
                    journal = self.state()["candidate"]
                    self.assertIn("# fixture release A", self.link.read_text())
                    second_id = journal["version"]
                    self.assertEqual((journal["phase"], journal["step"]), ("activating", step))
                    status = self.invoke(self.link, "status").stdout
                    for expected in ("Mixed installation", self.first_id, second_id, "kk upgrade", "kk rollback"):
                        self.assertIn(expected, status)
                    self.assertIn("A stage", self.trace.read_text())
                    self.assertIn("A validate", self.trace.read_text())
                    self.assertIn("A status", self.trace.read_text())
                    self.stop.unlink()
                    self.trace.write_text("")
                    self.invoke(self.link, recovery)
                    trace = self.trace.read_text()
                    self.assertNotIn(" stage", trace)
                    if recovery == "upgrade":
                        self.check_active(second_id, "B")
                        self.assertEqual(self.state()["rollback_target"], self.first_id)
                        self.assertIn("A validate", trace)
                        self.assertIn("B finish_install", trace)
                    else:
                        self.check_active(self.first_id, "A")
                        self.assertIn("A rollback_locked", trace)
                        self.assertNotIn("B ", trace)
                        if step != "place":
                            self.assertIsNotNone(self.state()["releases"][second_id]["superseded_at"])

    def test_dispatcher_publication_interruption_after_promotion(self):
        snapshot = self.root / "snapshot"
        shutil.copytree(self.home, snapshot, symlinks=True)
        for point, label in (("publish-dispatcher", "A"), ("published-dispatcher", "B")):
            for recovery in ("upgrade", "rollback"):
                with self.subTest(point=point, recovery=recovery):
                    shutil.rmtree(self.home)
                    shutil.copytree(snapshot, self.home, symlinks=True)
                    self.stop.write_text(point)
                    self.assertEqual(self.upgrade(ok=False).returncode, 79)
                    record = self.state()
                    target = record["active"]
                    self.assertEqual(record["pending_entry"], target)
                    self.assertEqual(record["rollback_target"], self.first_id)
                    self.assertIsNone(record["candidate"])
                    self.assertIn("# fixture release " + label, self.link.read_text())
                    self.assertIn("publication pending", self.invoke(self.link, "status").stdout)
                    self.stop.unlink()
                    if recovery == "rollback":
                        (self.release(target) / "kk/lib").rename(self.release(target) / "unavailable")
                    else:
                        (self.release(target) / "kk/bin/kk").write_text("#!/bin/sh\nexit 67\n")
                    self.invoke(self.link, recovery, env=dict(self.env, KK_REPOSITORY="offline"))
                    self.assertNotIn("pending_entry", self.state())
                    if recovery == "upgrade":
                        self.check_active(target, "B")
                    else:
                        self.check_active(self.first_id, "A")

    def test_offline_rollback_survives_broken_active_code_and_dispatcher(self):
        for break_entry in (None, "script", "symlink"):
            with self.subTest(break_entry=break_entry):
                result = self.upgrade()
                command = shlex.split(result.stdout.split("Recovery command: ")[1].strip())
                self.assertEqual(command, [str(self.release(self.first_id) / "kk/bin/kk"), "rollback"])
                active = self.release(self.state()["active"])
                (active / "kk/lib").rename(active / "kk/unavailable")
                if break_entry == "script":
                    (self.toolbox / "bin/kk").write_text("#!/bin/sh\nexit 63\n")
                if break_entry == "symlink":
                    foreign = self.root / "foreign"
                    foreign.write_text("outside toolbox")
                    (self.toolbox / "bin/kk").unlink()
                    (self.toolbox / "bin/kk").symlink_to(foreign)
                self.trace.write_text("")
                self.stop.write_text("verify")
                entry = command if break_entry else [self.link, "rollback"]
                self.assertEqual(self.invoke(*entry, ok=False).returncode, 79)
                self.assertEqual(self.state()["candidate"]["operation"], "rollback")
                self.stop.unlink()
                self.invoke(*entry)
                self.check_active(self.first_id, "A")
                if break_entry == "symlink":
                    self.assertEqual(foreign.read_text(), "outside toolbox")
                self.assertNotIn("B ", self.trace.read_text())
                self.assertIn("A rollback_locked", self.trace.read_text())

    def test_tagged_candidate_survives_rollback_and_offline_retry(self):
        archive = self.root / "release.tar"
        with tarfile.open(archive, "w") as stream:
            stream.add(self.second, "source")
        tag = "v" + json.loads((self.second / "klaude-plugin/.claude-plugin/plugin.json").read_text())["version"]
        active = cli.load_cli(self.release(self.first_id) / "kk/lib", "_active_tag_test")
        override = self.home / "list-override"
        override.write_text(json.dumps({"readFromFolder": None}))
        with patch.dict(os.environ, self.env), patch.object(sys, "argv", ["kk", "upgrade", "--version", tag]):
            with patch.object(active.payload, "urlopen", return_value=archive.open("rb")):
                self.assertEqual(active.main(), 1)
        held = self.release(tag).stat().st_ino
        pending = self.state()["candidate"]
        override.unlink()
        self.stop.write_text("promote")
        self.invoke(self.link, "rollback", ok=False)
        self.stop.unlink()
        self.invoke(self.link, "rollback")
        retired = self.state()["releases"][tag]
        for field in ("source", "digest", "digest_format"):
            self.assertEqual(retired[field], pending[field])
        with patch.dict(os.environ, self.env), patch.object(sys, "argv", ["kk", "upgrade", "--version", tag]):
            with patch.object(active.payload, "urlopen", side_effect=AssertionError("unexpected network request")):
                self.assertEqual(active.main(), 0)
        self.check_active(tag, "B")
        self.assertEqual(self.release(tag).stat().st_ino, held)

    def test_fingerprint_tolerates_concurrent_atomic_cache_publication(self):
        release = self.release(self.first_id)
        expected = cli.payload.fingerprint(release)
        cache = release / cli.payload.GUARD_CACHE
        cache.mkdir(exist_ok=True)
        staged = cache / "guard.cpython-311.pyc.12345"
        published = cache / "guard.cpython-311.pyc"
        original = Path.rglob
        def walk(path, pattern):
            staged.write_bytes(b"temporary")
            yield from original(path, pattern)
            staged.replace(published)
            yield published
        with patch.object(Path, "rglob", walk):
            self.assertEqual(cli.payload.fingerprint(release), expected)

    def test_retention_uses_supersession_time_and_preserves_exclusions(self):
        old = datetime.now(timezone.utc) - timedelta(days=35)
        os.utime(self.release(self.first_id), (old.timestamp(), old.timestamp()))
        orphan = "local-" + "a" * 32
        self.release(orphan).mkdir()
        os.utime(self.release(orphan), (old.timestamp(), old.timestamp()))
        self.upgrade()
        second_id = self.state()["active"]
        self.upgrade()
        record = self.state()
        self.assertEqual(record["rollback_target"], second_id)
        for version in (self.first_id, orphan):
            self.assertTrue(self.release(version).is_dir())
            self.assertGreater(datetime.fromisoformat(record["releases"][version]["superseded_at"]), old)
        now = datetime.now(timezone.utc)
        record["releases"][orphan]["superseded_at"] = (now - timedelta(days=14)).isoformat()
        record["releases"][self.first_id]["superseded_at"] = old.isoformat()
        for version in (record["active"], second_id):
            record["releases"][version]["superseded_at"] = old.isoformat()
        cli.state.prune(self.toolbox, record, now)
        self.assertFalse(self.release(self.first_id).exists())
        self.assertNotIn(self.first_id, self.state()["releases"])
        self.assertTrue(self.release(orphan).exists())
        cli.state.prune(self.toolbox, record, now + timedelta(seconds=1))
        self.assertFalse(self.release(orphan).exists())
        for version in (record["active"], second_id):
            self.assertTrue(self.release(version).is_dir())

    def test_cache_churn_resumes_but_changed_source_requires_rollback(self):
        self.stop.write_text("verify")
        self.upgrade(ok=False)
        self.stop.unlink()
        candidate = self.release(self.state()["candidate"]["version"])
        cache = candidate / "klaude-plugin/scripts/guard/__pycache__/guard.cpython-999.pyc"
        cache.parent.mkdir(exist_ok=True)
        cache.write_bytes(b"transient interpreter output")
        self.invoke(self.link, "upgrade")
        self.assertFalse(cache.exists())
        self.assertEqual(self.state()["active"], candidate.name)
        self.stop.write_text("verify")
        self.upgrade(ok=False)
        self.stop.unlink()
        pending = self.release(self.state()["candidate"]["version"])
        (pending / "klaude-plugin/scripts/guard/guard.py").write_text("changed\n")
        self.assertIn("run kk rollback", self.invoke(self.link, "upgrade", ok=False).stderr)
        self.assertEqual(self.state()["candidate"]["version"], pending.name)
        self.invoke(self.link, "rollback")
        self.check_active(candidate.name, "B")
