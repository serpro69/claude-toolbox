"""Offline prompt-boundary and retained-evidence regressions; no actor calls."""
import argparse
from contextlib import contextmanager
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import successor


class BootstrapTests(unittest.TestCase):
    @contextmanager
    def adapter(self):
        with tempfile.TemporaryDirectory(prefix="fr-bootstrap-test-") as name:
            root = Path(name)
            for filename in successor.host.DEPENDENCIES:
                shutil.copyfile(successor.HERE / filename, root / filename)
            with patch.object(successor.host, "HERE", root), \
                    patch.object(successor.host, "FROZEN", root / "execution-freeze.json"), \
                    patch.object(successor.host, "WORKSPACES", root / "actors"):
                adapter = successor.Adapter()
                adapter.freeze()
                yield adapter, root

    def job(self, adapter, root, side="candidate", binding=True):
        name = side + ("-binding" if binding else "-measured")
        return argparse.Namespace(provider="claude", side=side, case="R6M",
            mode="standard", repetition=0, snapshot=adapter.controller.SNAPSHOTS[side],
            workspace=root / "actors" / name, evidence=root / name,
            frozen=successor.host.FROZEN, binding=binding)

    def test_freeze_pins_prompt_and_historical_sources_without_overwriting(self):
        old = successor.inputs.sha(successor.HOST / "execution-freeze.json")
        with self.adapter() as (adapter, root):
            adapter.verify()
            frozen = successor.inputs.read(successor.host.FROZEN)
            self.assertIn("binding-prompt.txt", frozen["dependencies"])
            self.assertIn("high-effort-host/guarded_successor.py", frozen["inherited_evidence"])
            self.assertEqual(successor.inputs.sha(successor.HOST / "execution-freeze.json"), old)
            with self.assertRaises(FileExistsError):
                adapter.freeze()
            (root / "binding-prompt.txt").write_text("changed")
            with self.assertRaisesRegex(ValueError, "Changed or unsafe"):
                adapter.verify()

    def test_real_preparation_preserves_measured_prompt_and_validates_bindings(self):
        with self.adapter() as (adapter, root):
            for side in ("baseline", "candidate"):
                for binding in (True, False):
                    with self.subTest(side=side, binding=binding):
                        job = self.job(adapter, root, side, binding)
                        adapter.prepare(job)
                        adapter.controller.validate_launch(job.evidence, job.frozen)
                        launch = successor.inputs.read(job.evidence / "launch.json")
                        expected = (successor.binding_prompt() if binding else
                            adapter.verify()["prompts"]["claude/R6M/standard"])
                        self.assertEqual(launch["prompt"], expected)
                        self.assertEqual(launch["claude_effort_environment"], successor.host.EFFORT_ENV)
                        self.assertNotIn("pal", launch["mcp"])
                        with self.assertRaises(FileExistsError):
                            adapter.prepare(job)

    def test_changed_historical_evidence_cannot_be_refrozen_or_verified(self):
        with self.adapter() as (adapter, root):
            changed = successor.host.Adapter.inherited_evidence(adapter)
            changed["preflight.json"] = "0" * 64
            with patch.object(successor.host.Adapter, "inherited_evidence", return_value=changed):
                with self.assertRaisesRegex(ValueError, "Reviewed historical evidence changed"):
                    adapter.verify()
                with patch.object(successor.host, "FROZEN", root / "another-freeze.json"):
                    with self.assertRaisesRegex(ValueError, "Reviewed historical evidence changed"):
                        adapter.freeze()
                    self.assertFalse(successor.host.FROZEN.exists())

    def test_resealed_wrong_binding_prompt_fails_before_transport(self):
        with self.adapter() as (adapter, root):
            job = self.job(adapter, root)
            adapter.prepare(job)
            launch_path = job.evidence / "launch.json"
            launch = successor.inputs.read(launch_path)
            launch["prompt"] = "Stop before loading detection instructions."
            adapter.seed.write_json(launch_path, launch)
            (job.evidence / "prompt.txt").write_text(launch["prompt"] + "\n")
            prepared = successor.inputs.read(job.evidence / "prepared.json")
            prepared["launch_sha256"] = successor.inputs.sha(launch_path)
            prepared["prompt_sha256"] = successor.inputs.sha(job.evidence / "prompt.txt")
            adapter.seed.write_json(job.evidence / "prepared.json", prepared)
            with patch.object(adapter.prior, "capture") as transport:
                with self.assertRaisesRegex(ValueError, "Binding prompt differs"):
                    adapter.capture(job, [None])
                transport.assert_not_called()

    def test_successful_raw_baseline_and_failed_candidate_remain_distinct(self):
        adapter = successor.Adapter()
        # Old captures belong to their old freeze/prompt. Exercise only the carried
        # receipt recomputation here, bypassing the new identity/prompt comparison.
        with patch.object(successor.host, "HERE", successor.HOST), \
                patch.object(adapter, "check_binding"):
            adapter.verify_receipt("baseline")
            with self.assertRaisesRegex(ValueError, "Incomplete Claude instructions"):
                adapter.verify_receipt("candidate")

    def test_empty_retained_audit_cannot_replace_successful_raw_evidence(self):
        adapter = successor.Adapter()
        original = successor.inputs.read
        audit = successor.HOST / "audits/binding-claude-baseline.json"
        def read(path):
            return {} if Path(path) == audit else original(path)
        with patch.object(successor.host, "HERE", successor.HOST), \
                patch.object(adapter, "check_binding"), \
                patch.object(successor.inputs, "read", side_effect=read):
            with self.assertRaisesRegex(ValueError, "Receipt audit differs"):
                adapter.verify_receipt("baseline")

    def test_receipt_failure_prevents_original_approval_gate(self):
        with self.adapter() as (adapter, root), \
                patch.object(adapter, "verify_receipt", side_effect=ValueError("missing receipt")), \
                patch.object(successor.host.Adapter, "preflight") as approval:
            with self.assertRaisesRegex(ValueError, "missing receipt"):
                adapter.preflight()
            approval.assert_not_called()

    def test_cli_selects_strict_adapter_and_restores_on_failure(self):
        previous = successor.host.Adapter
        def fail():
            self.assertIs(successor.host.Adapter, successor.Adapter)
            raise RuntimeError("selected operation failed")
        with patch.object(successor.host, "main", side_effect=fail):
            with self.assertRaisesRegex(RuntimeError, "selected operation failed"):
                successor.main()
        self.assertIs(successor.host.Adapter, previous)


if __name__ == "__main__":
    unittest.main()
