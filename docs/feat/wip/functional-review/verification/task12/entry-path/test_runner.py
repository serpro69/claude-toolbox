"""Offline controls for the bounded run set and probe-only prompt override."""
import hashlib
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import runner


class RunnerTests(unittest.TestCase):
    def test_declared_pairs_are_fresh_disjoint_and_isolated(self):
        snapshots = {side: Path("/tmp") / side for side in ("baseline", "candidate")}
        with patch.object(runner.driver.controller, "SNAPSHOTS", snapshots):
            jobs = runner.jobs_for(Path("freeze.json"))
        expected = {(case, side, repetition) for case in ("R3", "R5", "R9-recovery")
                    for side in ("baseline", "candidate") for repetition in (1, 2)}
        self.assertEqual({(j.case, j.side, j.repetition) for j in jobs}, expected)
        self.assertEqual(len(jobs), 12)
        self.assertEqual(len({j.workspace for j in jobs}), 12)
        self.assertEqual(len({j.evidence for j in jobs}), 12)
        self.assertTrue(all(j.mode == "isolated" and j.provider == "claude" and not j.binding
                            for j in jobs))

    def test_probe_prompt_is_bound_to_launch_and_preparation_receipts(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "launch.json").write_text(json.dumps({"prompt": "old", "side": "candidate"}))
            (root / "prepared.json").write_text(json.dumps({"patch_sha256": "unchanged"}))
            (root / "prompt.txt").write_text("old\n")
            with patch.object(runner.driver, "prepare_job"):
                runner.prepare(SimpleNamespace(binding=True, evidence=root))
            launch = json.loads((root / "launch.json").read_text())
            prepared = json.loads((root / "prepared.json").read_text())
            self.assertEqual(launch["prompt"], runner.BINDING_PROMPT)
            self.assertEqual((root / "prompt.txt").read_text(), launch["prompt"] + "\n")
            self.assertEqual(prepared["launch_sha256"], hashlib.sha256((root / "launch.json").read_bytes()).hexdigest())
            self.assertEqual(prepared["prompt_sha256"], hashlib.sha256((root / "prompt.txt").read_bytes()).hexdigest())
            self.assertEqual(prepared["patch_sha256"], "unchanged")
            self.assertEqual(launch["side"], "candidate")

    def test_measured_prompt_and_launch_bytes_remain_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            originals = {"launch.json": b'{"prompt":"ordinary request"}',
                         "prompt.txt": b"ordinary request\n", "prepared.json": b'{"frozen":"original"}'}
            for name, data in originals.items():
                (root / name).write_bytes(data)
            job = SimpleNamespace(binding=False, evidence=root)
            with patch.object(runner.driver, "prepare_job") as prepare:
                runner.prepare(job)
            prepare.assert_called_once_with(job)
            self.assertEqual({name: (root / name).read_bytes() for name in originals}, originals)


if __name__ == "__main__":
    unittest.main()
