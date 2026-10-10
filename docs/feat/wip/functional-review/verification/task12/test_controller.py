"""Offline integrity tests for the Task 12 preparation boundary."""
import json
import argparse
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import controller


class FreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshots = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.snapshots.cleanup)
        snapshots = {}
        for side, revision in (("baseline", controller.BASELINE), ("candidate", controller.CANDIDATE)):
            destination = Path(cls.snapshots.name) / side
            controller.subprocess.run([controller.sys.executable, "-B",
                str(controller.VERIFICATION / "prepare-bundles.py"), "build",
                str(controller.ROOT), revision, str(destination)], check=True,
                stdout=controller.subprocess.PIPE)
            snapshots[side] = destination
        cls.snapshot_patch = patch.dict(controller.SNAPSHOTS, snapshots)
        cls.snapshot_patch.start()
        cls.addClassCleanup(cls.snapshot_patch.stop)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.frozen = Path(self.temp.name) / "frozen.json"
        with patch.object(controller.subprocess, "check_output", return_value="version\n"):
            controller.freeze(self.frozen)

    def test_complete_matrix_and_prompts(self):
        data = controller.verify_frozen(self.frozen)
        self.assertEqual(len(data["fixtures"]), 15)
        self.assertEqual(len(data["prompts"]), 48)
        self.assertIn("/kk:review-code:isolated", data["prompts"]["claude/R1/isolated"])
        self.assertIn("$kk:review-code isolated", data["prompts"]["codex/R3/isolated"])
        self.assertIn("checkpoint.md", data["prompts"]["claude/R8-zero/replay"])

    def test_refuses_overwrite(self):
        before = self.frozen.read_bytes()
        with patch.object(controller.subprocess, "check_output", return_value="version\n"):
            with self.assertRaises(FileExistsError):
                controller.freeze(self.frozen)
        self.assertEqual(before, self.frozen.read_bytes())

    def test_rejects_changed_fixture(self):
        with patch.object(controller.seed, "files", return_value={}):
            with self.assertRaisesRegex(ValueError, "Fixture changed"):
                controller.verify_frozen(self.frozen)

    def test_rejects_manifest_not_matching_source_identity(self):
        original = controller.seed.sha
        path = controller.SNAPSHOTS["baseline"] / "retained-manifest.json"
        content = path.read_bytes()
        with patch.object(controller.seed, "sha", side_effect=lambda data: "changed" if data == content else original(data)):
            with self.assertRaisesRegex(ValueError, "Frozen instruction snapshot changed"):
                controller.verify_frozen(self.frozen)

    def test_rejects_changed_frozen_prompt(self):
        with patch.object(controller.seed, "prompt_for", return_value="hinted prompt"):
            with self.assertRaisesRegex(ValueError, "Prompt changed"):
                controller.verify_frozen(self.frozen)

    def test_rejects_changed_controller(self):
        data = json.loads(self.frozen.read_bytes())
        data["controllers"]["task12/controller.py"] = "wrong"
        self.frozen.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "Controller changed"):
            controller.verify_frozen(self.frozen)

    def prepare(self):
        args = argparse.Namespace(provider="claude", side="baseline", case="R1", mode="standard",
                                  snapshot=controller.SNAPSHOTS["baseline"],
                                  workspace=Path(self.temp.name) / "actor",
                                  evidence=Path(self.temp.name) / "evidence",
                                  frozen=self.frozen, binding=False)
        controller.prepare(args)
        return args

    def test_rejects_nested_evidence_before_mutation(self):
        args = argparse.Namespace(provider="claude", side="baseline", case="R1", mode="standard",
                                  snapshot=controller.SNAPSHOTS["baseline"],
                                  workspace=Path(self.temp.name) / "actor",
                                  evidence=Path(self.temp.name) / "actor/evidence",
                                  frozen=self.frozen, binding=False)
        with self.assertRaisesRegex(ValueError, "disjoint"):
            controller.prepare(args)
        self.assertFalse(args.workspace.exists())

    def test_accepts_fresh_launch(self):
        args = self.prepare()
        controller.validate_launch(args.evidence, self.frozen)

    def test_rejects_changed_bundle(self):
        args = self.prepare()
        (args.workspace / "plugins/kk/skills/review-code/SKILL.md").write_text("changed")
        with self.assertRaises(controller.subprocess.CalledProcessError):
            controller.validate_launch(args.evidence, self.frozen)

    def test_rejects_changed_subject(self):
        args = self.prepare()
        (args.workspace / "cleanup.py").write_text("changed")
        with self.assertRaisesRegex(ValueError, "Subject files changed"):
            controller.validate_launch(args.evidence, self.frozen)

    def test_rejects_changed_prompt(self):
        args = self.prepare()
        (args.evidence / "prompt.txt").write_text("changed")
        with self.assertRaisesRegex(ValueError, "Prepared prompt changed"):
            controller.validate_launch(args.evidence, self.frozen)

    def test_rejects_inherited_state(self):
        args = self.prepare()
        (args.workspace / ".runner/knowledge.db").write_text("stale")
        with self.assertRaisesRegex(ValueError, "inherited runtime/knowledge state"):
            controller.validate_launch(args.evidence, self.frozen)


if __name__ == "__main__":
    unittest.main()
