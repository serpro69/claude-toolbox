"""Offline controls only: no actor, grader, registration or external service."""
import argparse
import copy
from contextlib import contextmanager
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import calibration
import inputs
import runner


class AdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adapter = runner.Adapter()

    def test_exact_matrix_order_and_sources(self):
        jobs = self.adapter.jobs()
        declared = inputs.read(inputs.PREPARATION / "matrix.json")["jobs"]
        self.assertEqual([j.evidence.name for j in jobs], [r["id"] for r in declared])
        self.assertEqual(len({j.evidence.name for j in jobs}), 64)
        for job, row in zip(jobs, declared):
            self.assertEqual(inputs.read(job.snapshot / "identity.json")["revision"], row["actor_revision"])

    def test_per_case_rubric_and_restoration(self):
        original = self.adapter.controller.RUBRIC
        for case in ("R6D", "R6M", "R5", "R9-recovery"):
            with self.adapter.case_context(case):
                self.assertEqual(self.adapter.controller.RUBRIC, self.adapter.rubric(case))
            self.assertEqual(self.adapter.controller.RUBRIC, original)
        with self.assertRaises(RuntimeError), self.adapter.case_context("R6D"):
            raise RuntimeError("grading export failed")
        self.assertEqual(self.adapter.controller.RUBRIC, original)

    def test_restored_fixture_tamper_fails(self):
        path = self.adapter.seed.fixture("R6D") / "test-files/after/config.py"
        original = path.read_bytes()
        try:
            path.write_bytes(b"tampered\n")
            with self.assertRaisesRegex(ValueError, "controller/fixture inputs differ"):
                inputs.verify_restored()
        finally:
            path.write_bytes(original)

    def test_input_restore_refuses_existing_destination(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(FileExistsError):
                inputs.restore(Path(root))

    def test_prepare_refuses_reuse_before_transport(self):
        with tempfile.TemporaryDirectory() as root:
            job = argparse.Namespace(workspace=Path(root), evidence=Path(root) / "new")
            with patch.object(self.adapter.prior, "prepare") as transport:
                with self.assertRaises(FileExistsError):
                    self.adapter.prepare(job)
                transport.assert_not_called()

    def test_capture_refuses_partial_attempt(self):
        with tempfile.TemporaryDirectory() as root:
            job = argparse.Namespace(evidence=Path(root))
            (job.evidence / "command.json").write_text("{}")
            with patch.object(self.adapter.prior, "capture") as transport:
                with self.assertRaises(FileExistsError):
                    self.adapter.capture(job, [None])
                transport.assert_not_called()

    def test_batch_checks_every_job_before_capture(self):
        with tempfile.TemporaryDirectory() as root:
            jobs = self.fake_jobs(Path(root))
            (jobs[-1].evidence / "prepared.json").unlink()
            with self.assertRaisesRegex(ValueError, "all 64"):
                runner.validate_batch(jobs)

    def test_batch_rejects_prior_completed_or_partial_attempt(self):
        with tempfile.TemporaryDirectory() as root:
            jobs = self.fake_jobs(Path(root))
            (jobs[7].evidence / "events.jsonl").write_text("{}")
            with self.assertRaises(FileExistsError):
                runner.validate_batch(jobs)

    def test_batch_rejects_subset(self):
        with self.assertRaisesRegex(ValueError, "complete declared batch"):
            runner.validate_batch([])

    def test_preflight_failure_prevents_capture(self):
        with patch.object(self.adapter, "preflight", side_effect=ValueError("missing binding")), \
                patch.object(self.adapter, "capture") as capture:
            with self.assertRaisesRegex(ValueError, "missing binding"):
                self.adapter.run(self.adapter.jobs())
            capture.assert_not_called()

    def test_runtime_failure_stops_after_first_attempt(self):
        self.check_stopped_batch(interrupt=False)

    def test_interruption_stops_after_first_attempt(self):
        self.check_stopped_batch(interrupt=True)

    def check_stopped_batch(self, interrupt):
        with tempfile.TemporaryDirectory() as root:
            jobs = self.fake_jobs(Path(root))
            calls = []
            def capture(job, request):
                calls.append(job.evidence.name)
                request[0] = 15 if interrupt else None
                inputs.write_new(job.evidence / "manifest.json", {})
                inputs.write_new(job.evidence / "completion.json", {
                    "exit_code": 0 if interrupt else 7, "interrupted_by": request[0]})
            with patch.object(self.adapter, "preflight"), patch.object(runner, "runtime_identity"), \
                    patch.object(self.adapter, "capture", side_effect=capture):
                self.assertEqual(self.adapter.run(jobs), 143 if interrupt else 7)
            self.assertEqual(calls, [jobs[0].evidence.name])

    @staticmethod
    def fake_jobs(root):
        jobs = []
        for number in range(64):
            directory = root / str(number)
            directory.mkdir()
            (directory / "prepared.json").write_text("{}")
            jobs.append(argparse.Namespace(evidence=directory))
        return jobs

    def test_execution_freeze_detects_dependency_and_calibration_drift(self):
        with tempfile.TemporaryDirectory() as root, patch.object(runner, "FROZEN", Path(root) / "freeze.json"):
            self.adapter.freeze()
            self.adapter.verify()
            data = inputs.read(runner.FROZEN)
            data["dependencies"]["runner.py"] = "0" * 64
            runner.FROZEN.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "Changed or unsafe"):
                self.adapter.verify()

    def test_offline_prepare_routes_both_provider_rubrics_without_actor_calls(self):
        with tempfile.TemporaryDirectory(prefix="fr-advisory-test-") as root, \
                patch.object(runner, "FROZEN", Path(root) / "freeze.json"), \
                patch.object(self.adapter.prior.matrix, "capture") as capture, \
                patch.object(self.adapter.prior.matrix, "admin") as admin:
            self.adapter.freeze()
            for provider, case in (("claude", "R6D"), ("claude", "R5"), ("codex", "R6M"), ("codex", "R9-recovery")):
                for side in ("baseline", "candidate"):
                    name = f"{provider}-{case}-{side}"
                    job = argparse.Namespace(provider=provider, case=case, side=side, mode="isolated",
                        repetition=1, workspace=Path(root) / ("actor-" + name),
                        evidence=Path(root) / ("evidence-" + name),
                        snapshot=self.adapter.controller.SNAPSHOTS[side], frozen=runner.FROZEN, binding=False)
                    self.adapter.prepare(job)
                    launch = inputs.read(job.evidence / "launch.json")
                    self.assertEqual(launch["rubric_sha256"], inputs.sha(self.adapter.rubric(case)))
                    self.assertEqual(launch["actor"], inputs.read(job.snapshot / "identity.json"))
                    self.assertFalse((job.evidence / "command.json").exists())
                    if provider == "claude":
                        self.assertNotIn("pal", inputs.read(job.workspace / ".runner/mcp-no-pal.json")["mcpServers"])
                    else:
                        self.assertIn('[mcp_servers.pal]\nenabled = false', (job.workspace / ".codex/config.toml").read_text())
            capture.assert_not_called()
            admin.assert_not_called()

    def test_checked_files_rejects_escape(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(ValueError):
                runner.checked_files(Path(root), {"../outside": "0" * 64})


class CalibrationTests(unittest.TestCase):
    def test_dispatch_configuration_and_linkage_are_required(self):
        planned = inputs.read(calibration.ROOT / "dispatch-plan.json")["disposition-01"]
        with tempfile.TemporaryDirectory() as root, patch.object(calibration, "HERE", Path(root)):
            (Path(root) / "execution-freeze.json").write_text("{}")
            record = {**copy.deepcopy(planned), "agent_id": "/root/" + planned["request"]["task_name"],
                      "response": {"task_name": "/root/" + planned["request"]["task_name"]},
                      "execution_freeze_sha256": inputs.sha(Path(root) / "execution-freeze.json")}
            calibration.validate_dispatch("disposition-01", record, planned)
            for key, value in (("workflow_mode", "component"), ("grader_sha256", "wrong"),
                               ("prompt_sha256", "wrong"), ("role_configuration", {}),
                               ("response", {"task_name": "/root/someone-else"})):
                changed = copy.deepcopy(record)
                changed[key] = value
                with self.subTest(key=key), self.assertRaises(ValueError):
                    calibration.validate_dispatch("disposition-01", changed, planned)
            changed = copy.deepcopy(record)
            changed["request"]["fork_turns"] = "all"
            with self.assertRaises(ValueError):
                calibration.validate_dispatch("disposition-01", changed, planned)

    def test_frozen_expectation_and_dependency_drift_cannot_certify(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            packets = root / "calibration"
            packets.mkdir()
            (root / "sentinel.py").write_text("value = 1\n")
            (packets / "expected-verdicts.json").write_text("{}")
            (packets / "grader.md").write_text("pinned methodology")
            inputs.write_new(root / "execution-freeze.json", {
                "preparation_sha256": inputs.PREPARATION_SHA,
                "dependencies": {"sentinel.py": inputs.sha(root / "sentinel.py")},
                "calibration_inputs": {"calibration/expected-verdicts.json": inputs.sha(packets / "expected-verdicts.json")},
                "grader_sha256": inputs.sha(packets / "grader.md")})
            with patch.object(calibration, "HERE", root), patch.object(calibration, "ROOT", packets):
                calibration.verify_frozen_inputs()
                (packets / "expected-verdicts.json").write_text('{"changed": true}')
                for operation in (calibration.reconcile, calibration.verify_results):
                    with self.assertRaisesRegex(ValueError, "Changed or unsafe"):
                        operation()
                (packets / "expected-verdicts.json").write_text("{}")
                (root / "sentinel.py").write_text("value = 2\n")
                with self.assertRaisesRegex(ValueError, "Changed or unsafe"):
                    calibration.verify_frozen_inputs()

    def test_every_packet_sealed_without_controller_answers(self):
        expected = inputs.read(calibration.ROOT / "expected-verdicts.json")
        plan = inputs.read(calibration.ROOT / "dispatch-plan.json")
        self.assertEqual(set(plan), set(expected))
        self.assertEqual(len(expected), 25)
        self.assertEqual(sum(len(r["verdicts"]) for r in expected.values()), 69)
        for name in expected:
            self.assertTrue(plan[name]["request"]["message"].startswith("## Plugin Root\n" + calibration.PLUGIN_ROOT + "\n"))
            manifest = calibration.validate_packet(calibration.ROOT / "inputs" / name)
            self.assertFalse(any("expected-verdicts" in r["path"] for r in manifest["files"]))

    def test_unlisted_evidence_is_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            target = Path(root) / "packet"
            shutil.copytree(calibration.ROOT / "inputs/disposition-01", target)
            (target / "unexpected.json").write_text("{}")
            with self.assertRaisesRegex(ValueError, "Unexpected or missing"):
                calibration.validate_packet(target)

    def test_duplicate_assertion_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            calibration.verdicts("| D.1 | PASS | evidence |\n| D.1 | PASS | again |")

    def test_trigger_is_observed_not_inferred(self):
        text = "| 22.6 | PASS | trigger=absent; report has no advisory |"
        self.assertEqual(calibration.trigger_values(text, {"22.6"}), {"22.6": "absent"})
        self.assertEqual(calibration.trigger_values("| 22.6 | PASS | no explicit value |", {"22.6"}), {})


if __name__ == "__main__":
    unittest.main()
