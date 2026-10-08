"""Offline rejection controls for the Task 1 instruction packaging boundary."""

from pathlib import Path
import os
import runpy
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from probe_state import workspace_at


BUNDLE = runpy.run_path(str(Path(__file__).with_name("prepare-bundles.py")))


class BundleBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "bundle"
        self.root.mkdir()

    def test_preserves_hidden_files_executable_mode_and_local_link(self):
        target = self.root / ".instruction"
        target.write_bytes(b"unaltered\n")
        target.chmod(0o755)
        (self.root / "shared.md").symlink_to(".instruction")
        records = BUNDLE["manifest"](self.root)
        self.assertEqual([r["path"] for r in records], [".instruction", "shared.md"])
        self.assertEqual(records[0]["mode"], "0o755")
        self.assertEqual(records[1]["target"], ".instruction")
        self.assertEqual(records[0]["sha256"], records[1]["sha256"])

    def test_rejects_evaluator_material_at_any_depth(self):
        for path in ("skills/x/evals/case/eval.json", "oracle/answer.md", "grading-fixtures/run.json",
                     "verification/trace.json", "results/run.json", "reports/review.md",
                     "eval.json", "gold-claims.json", "expected-verdicts.json"):
            with self.subTest(path=path):
                self.assertTrue(BUNDLE["excluded"](path))
        (self.root / "eval.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "Evaluator material"):
            BUNDLE["manifest"](self.root)

    def test_rejects_link_back_to_controller(self):
        (self.root.parent / "oracle.md").write_text("private grading material")
        (self.root / "shared.md").symlink_to("../oracle.md")
        with self.assertRaisesRegex(ValueError, "Escaping link"):
            BUNDLE["manifest"](self.root)

    def test_rejects_absolute_link_even_inside_bundle(self):
        (self.root / "source.md").write_text("source")
        (self.root / "shared.md").symlink_to(self.root / "source.md")
        with self.assertRaisesRegex(ValueError, "Escaping link"):
            BUNDLE["manifest"](self.root)

    def test_rejects_dangling_or_directory_link(self):
        link = self.root / "shared.md"
        link.symlink_to("absent.md")
        with self.assertRaises(FileNotFoundError):
            BUNDLE["manifest"](self.root)
        link.unlink()
        (self.root / "directory").mkdir()
        link.symlink_to("directory")
        with self.assertRaisesRegex(ValueError, "Only file links"):
            BUNDLE["manifest"](self.root)

    def test_detects_changed_bytes_and_extra_cache_files(self):
        source = self.root / "SKILL.md"
        source.write_text("baseline")
        initial = BUNDLE["manifest"](self.root)
        source.write_text("stale candidate")
        self.assertNotEqual(initial, BUNDLE["manifest"](self.root))
        source.write_text("baseline")
        (self.root / ".unexpected").write_text("inherited state")
        self.assertNotEqual(initial, BUNDLE["manifest"](self.root))

    def test_archive_attributes_cannot_change_baseline_silently(self):
        for attribute, message in (("export-ignore", "omitted committed"),
                                   ("export-subst", "differs from Git blob")):
            with self.subTest(attribute=attribute), tempfile.TemporaryDirectory() as tmp:
                repo = workspace_at(Path(tmp) / "source")
                for tree in BUNDLE["TREES"]:
                    (repo / tree).mkdir(parents=True)
                    (repo / tree / "instruction.md").write_text("$Format:%H$\n")
                (repo / ".gitattributes").write_text("klaude-plugin/instruction.md " + attribute + "\n")
                env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
                env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
                git = ["git", "-C", str(repo), "-c", "core.hooksPath=" + os.devnull]
                subprocess.run([*git, "add", "-f", "."], env=env, check=True)
                subprocess.run([*git, "-c", "user.name=Probe", "-c", "user.email=probe@example.invalid",
                                "-c", "commit.gpgsign=false", "commit", "-qm", "Attribute control"],
                               env=env, check=True)
                with self.assertRaisesRegex(ValueError, message):
                    BUNDLE["build"](repo, "HEAD", Path(tmp) / "bundle")

    def test_fresh_workspace_ignores_git_environment_and_hooks(self):
        hooks = self.root / "hooks"
        hooks.mkdir()
        hook = hooks / "pre-commit"
        hook.write_text("#!/bin/sh\necho corrupted > README.md\nexit 1\n")
        hook.chmod(0o755)
        config = self.root / "global.gitconfig"
        config.write_text('[core]\nhooksPath = "' + str(hooks) + '"\n')
        with patch.dict(os.environ, {"GIT_CONFIG_GLOBAL": str(config),
                                     "GIT_DIR": str(self.root / "wrong.git"),
                                     "GIT_WORK_TREE": str(self.root),
                                     "GIT_TEMPLATE_DIR": str(hooks)}):
            workspace = workspace_at(self.root / "fresh")
        self.assertEqual((workspace / "README.md").read_text(), "# Disposable instruction-loading probe\n")
        self.assertTrue((workspace / ".git/HEAD").exists())
        self.assertFalse((self.root / "wrong.git").exists())


if __name__ == "__main__":
    unittest.main()
