"""Local regression checks against the actual sealed bindings; no model calls."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import guarded_successor as guard
import successor


class ReceiptGuardTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="fr-receipt-guard-")
        self.addCleanup(self.temporary.cleanup)
        pin = Path(self.temporary.name) / "guard-freeze.json"
        patcher = patch.object(guard, "GUARD_FREEZE", pin)
        patcher.start()
        self.addCleanup(patcher.stop)
        guard.freeze_guard()
        self.adapter = guard.Adapter()

    def test_actual_complete_baseline_receipts_pass(self):
        guard.verify_guard()
        guard.verify_receipt(self.adapter, "baseline")

    def test_actual_candidate_missing_reads_cannot_reach_approval_gate(self):
        # Even a nominally successful original proof cannot authorize these reads.
        with patch.object(successor.Adapter, "preflight", return_value=None) as old_guard:
            with self.assertRaisesRegex(ValueError, "Incomplete Claude instructions"):
                self.adapter.preflight()
            old_guard.assert_not_called()

    def test_empty_or_failed_audit_rejected_despite_good_raw_baseline(self):
        original = successor.inputs.read
        audit = successor.HERE / "audits/binding-claude-baseline.json"
        for replacement in ({}, {"status": "FAIL"}):
            def read(path):
                return replacement if Path(path) == audit else original(path)
            with self.subTest(replacement=replacement), patch.object(successor.inputs, "read", side_effect=read):
                with self.assertRaisesRegex(ValueError, "Receipt audit differs"):
                    guard.verify_receipt(self.adapter, "baseline")

    def test_guard_dependency_drift_refused(self):
        data = successor.inputs.read(guard.GUARD_FREEZE)
        data["dependencies"]["guarded_successor.py"] = "0" * 64
        self.adapter.seed.write_json(guard.GUARD_FREEZE, data)
        with self.assertRaisesRegex(ValueError, "Changed or unsafe"):
            guard.verify_guard()

    def test_selected_cli_delegates_to_strict_adapter_and_restores_on_error(self):
        previous = successor.Adapter
        def delegated():
            self.assertIs(successor.Adapter, guard.Adapter)
            raise RuntimeError("operation failed")
        with patch.object(guard.sys, "argv", ["guarded_successor.py", "prepare"]), \
                patch.object(successor, "main", side_effect=delegated):
            with self.assertRaisesRegex(RuntimeError, "operation failed"):
                guard.main()
        self.assertIs(successor.Adapter, previous)


if __name__ == "__main__":
    unittest.main()
