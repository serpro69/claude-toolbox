import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from test_install import ROOT


class ReleaseGuardVersion(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name)
        self.env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
        self.git("init", "-qb", "main")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("commit", "--allow-empty", "-qm", "Before the guard plugin")
        self.git("tag", "v0.9.0")
        self.bundle = self.repo / "kodex-guard"
        self.manifest = self.bundle / ".codex-plugin/plugin.json"
        self.manifest.parent.mkdir(parents=True)
        self.manifest.write_bytes(b'{"name":"kk-guard", "version" : "0.1.0"}\n')
        self.adapter = self.bundle / "adapter.sh"
        self.adapter.write_text("exit 0\n")

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.repo, env=self.env, check=True, capture_output=True)

    def release(self, version, mode):
        return subprocess.check_output(
            ["bash", str(ROOT / ".github/scripts/release-guard-version.sh"), version, mode],
            cwd=self.repo, env=self.env, text=True,
        ).strip()

    def test_first_release_skills_only_and_rc_on_another_branch(self):
        original = self.manifest.read_bytes()
        self.assertEqual(self.release("1.0.0", "--preview"), "1.0.0")
        self.assertEqual(self.manifest.read_bytes(), original)
        self.assertEqual(self.release("1.0.0", "--apply"), "1.0.0")
        published = original.replace(b"0.1.0", b"1.0.0")
        self.assertEqual(self.manifest.read_bytes(), published)
        self.git("add", ".")
        self.git("commit", "-qm", "First guard")
        self.git("tag", "-am", "Stable", "v1.0.0")

        (self.repo / "skill.md").write_text("Skills only\n")
        self.git("add", "skill.md")
        self.git("commit", "-qm", "Skills only")
        self.assertEqual(self.release("1.0.1", "--preview"), "1.0.0")
        self.assertEqual(self.release("1.0.1", "--apply"), "1.0.0")
        self.assertEqual(self.manifest.read_bytes(), published)

        self.git("checkout", "-qb", "candidate")
        self.adapter.chmod(0o755)
        self.assertEqual(self.release("1.1.0-rc.1", "--preview"), "1.1.0-rc.1")
        self.assertEqual(self.manifest.read_bytes(), published)
        self.assertEqual(self.release("1.1.0-rc.1", "--apply"), "1.1.0-rc.1")
        self.git("add", "kodex-guard")
        self.git("commit", "-qm", "Executable adapter")
        self.git("tag", "v1.1.0-rc.1")

        self.git("checkout", "-q", "main")
        self.adapter.chmod(0o755)
        self.assertEqual(self.release("1.1.0", "--preview"), "1.1.0-rc.1")
        self.assertEqual(self.manifest.read_bytes(), published)
        self.assertEqual(self.release("1.1.0", "--apply"), "1.1.0-rc.1")
        self.assertEqual(json.loads(self.manifest.read_bytes())["version"], "1.1.0-rc.1")
