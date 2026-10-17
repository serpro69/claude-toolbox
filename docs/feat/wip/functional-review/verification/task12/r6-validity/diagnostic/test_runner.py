"""Offline controller gates; no model, registration or network operations."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import runner


class RunnerTests(unittest.TestCase):
    def setUp(self):
        runner.configure()

    def test_exact_eight_jobs_and_same_instruction_source(self):
        jobs = runner.jobs_for(Path("/tmp/unused-r6-freeze.json"))
        self.assertEqual(len(jobs), 8)
        self.assertEqual({(j.provider, j.case, j.repetition) for j in jobs},
                         {(p, c, r) for p in ("claude", "codex")
                          for c in ("R6M", "R6D") for r in (1, 2)})
        self.assertEqual({j.mode for j in jobs}, {"standard"})
        self.assertEqual({j.side for j in jobs}, {"candidate"})
        self.assertEqual(len({j.workspace for j in jobs}), 8)
        self.assertEqual(len({j.evidence for j in jobs}), 8)
        self.assertEqual({j.snapshot for j in jobs}, {runner.HERE / "source-inputs"})
        self.assertEqual(runner.controller.BASELINE, runner.controller.CANDIDATE)

    def test_missing_any_preparation_blocks_even_selected_run(self):
        jobs = runner.jobs_for(Path("/tmp/unused-r6-freeze.json"))
        with tempfile.TemporaryDirectory() as temp:
            for i, job in enumerate(jobs):
                job.evidence = Path(temp) / str(i)
                job.evidence.mkdir()
                if i != 7:
                    (job.evidence / "prepared.json").write_text("{}")
            with self.assertRaisesRegex(ValueError, "all eight"):
                runner.validate_batch(jobs[:1], jobs)
            (jobs[-1].evidence / "prepared.json").write_text("{}")
            runner.validate_batch(jobs[:1], jobs)

    def test_partial_attempt_is_not_silently_retried(self):
        for marker in ("manifest.json", "command.json", "events.jsonl", "protocol.jsonl"):
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as temp:
                jobs = runner.jobs_for(Path("/tmp/unused-r6-freeze.json"))
                for i, job in enumerate(jobs):
                    job.evidence = Path(temp) / str(i)
                    job.evidence.mkdir()
                    (job.evidence / "prepared.json").write_text("{}")
                (jobs[0].evidence / marker).write_text("{}")
                with self.assertRaises(FileExistsError):
                    runner.validate_batch(jobs[:1], jobs)

    def test_calibration_controls_are_sealed_and_expected_answers_excluded(self):
        import calibration
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "calibration"
            calibration.build(destination)
            expected = json.loads((destination / "expected-verdicts.json").read_text())
            self.assertEqual(len(expected), 8)
            self.assertEqual(sum(len(c["verdicts"]) for c in expected.values()), 28)
            for name, answers in expected.items():
                root = destination / "inputs" / name
                manifest = json.loads((root / "manifest.json").read_text())
                for entry in manifest["files"]:
                    self.assertNotIn("expected-verdicts", entry["path"])
                    self.assertEqual(runner.seed.sha((root / entry["path"]).read_bytes()), entry["sha256"])
                assertions = json.loads((root / "assertions.json").read_text())
                self.assertEqual(set(answers["verdicts"]), {a["id"] for a in assertions})
            self.assertEqual(expected["dormant-missing-child"]["verdicts"]["22.3"], "PARTIAL")
            self.assertEqual(expected["dormant-absent"]["triggers"]["22.6"], "absent")

    def test_calibration_mismatch_blocks_freeze(self):
        expected = json.loads((runner.HERE / "calibration/expected-verdicts.json").read_text())
        results = json.loads((runner.HERE / "calibration/results.json").read_text())
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "calibration").mkdir()
            (root / "calibration/expected-verdicts.json").write_text(json.dumps(expected))
            result_path = root / "calibration/results.json"
            result_path.write_text(json.dumps(results))
            with patch.object(runner, "HERE", root):
                runner.verify_calibration()
                results["semantic"]["material-supported"]["verdicts"]["21.3"] = "FAIL"
                result_path.write_text(json.dumps(results))
                with self.assertRaisesRegex(ValueError, "Calibration verdict mismatch"):
                    runner.verify_calibration()

    def test_missing_preflight_blocks_measurement(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(runner, "HERE", Path(temp)):
            with self.assertRaises(FileNotFoundError):
                runner.verify_preflight(Path(temp) / "freeze.json")


if __name__ == "__main__":
    unittest.main(verbosity=2)
