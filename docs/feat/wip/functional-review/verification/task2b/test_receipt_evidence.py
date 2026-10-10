"""Supplement integrity and local metadata-only collection checks."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import merge_receipts
import receipt_supplement


class ReceiptEvidenceTests(unittest.TestCase):
    def test_local_collection_emits_only_allowlisted_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            line = "2026-10-10 14:36:24,728 - utils.conversation_memory - DEBUG - File embedded in conversation history: /tmp/owned-source.py (80 tokens)"
            (root / "observed-lines.txt").write_text("2:" + line + "\n")
            log = root / "runtime.log"
            log.write_text("unrelated private text\n" + line + "\nnot selected\n")
            with patch.object(receipt_supplement, "RECEIPTS", root), patch.object(receipt_supplement, "LOG", log):
                selected, origin = receipt_supplement.load_allowed_lines()
            self.assertEqual(set(selected), {2})
            self.assertNotIn("private", json.dumps(selected))
            self.assertFalse(origin["raw_log_copied"])
            self.assertEqual(origin["through_line"], 2)
            expected = ("unrelated private text\n" + line + "\n").encode()
            self.assertEqual(origin["prefix_sha256"], hashlib.sha256(expected).hexdigest())

    def test_unrelated_line_cannot_be_selected_for_export(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "observed-lines.txt").write_text("1:some prompt or credential\n")
            with patch.object(receipt_supplement, "RECEIPTS", root):
                with self.assertRaisesRegex(ValueError, "Non-allowlisted"):
                    receipt_supplement.load_allowed_lines()

    def test_curated_line_must_match_actual_local_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            line = "2026-10-10 14:36:24,728 - utils.conversation_memory - DEBUG - File embedded in conversation history: /tmp/owned-source.py (80 tokens)"
            (root / "observed-lines.txt").write_text("1:" + line + "\n")
            log = root / "runtime.log"
            log.write_text("different private line\n")
            with patch.object(receipt_supplement, "RECEIPTS", root), patch.object(receipt_supplement, "LOG", log):
                with self.assertRaisesRegex(ValueError, "metadata line 1") as raised:
                    receipt_supplement.load_allowed_lines()
            self.assertNotIn("private", str(raised.exception))

    def package(self, root, run, supplemental=False):
        root.mkdir()
        payload = root / "payload.txt"
        payload.write_text("receipt" if supplemental else "original evidence")
        manifest = {"run": run if supplemental else {"id": run}, "files": [
            {"path": "payload.txt", "sha256": hashlib.sha256(payload.read_bytes()).hexdigest()}]}
        (root / "manifest.json").write_text(json.dumps(manifest))

    def test_merge_rejects_another_run_before_creating_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.package(root / "original", "a")
            self.package(root / "supplement", "b", True)
            with self.assertRaisesRegex(ValueError, "another run"):
                merge_receipts.merge(root / "original", root / "supplement", root / "output")
            self.assertFalse((root / "output").exists())

    def test_merge_rejects_tampered_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.package(root / "original", "a")
            self.package(root / "supplement", "a", True)
            (root / "supplement/payload.txt").write_text("tampered")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                merge_receipts.merge(root / "original", root / "supplement", root / "output")
            self.assertFalse((root / "output").exists())

    def test_merge_keeps_original_and_supplement_separate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.package(root / "original", "a")
            self.package(root / "supplement", "a", True)
            original = (root / "original/manifest.json").read_bytes()
            merge_receipts.merge(root / "original", root / "supplement", root / "output")
            self.assertEqual((root / "original/manifest.json").read_bytes(), original)
            self.assertEqual((root / "output/payload.txt").read_text(), "original evidence")
            self.assertEqual((root / "output/receipt-supplement/payload.txt").read_text(), "receipt")
            self.assertEqual((root / "output/prior-grading-manifest.json").read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
