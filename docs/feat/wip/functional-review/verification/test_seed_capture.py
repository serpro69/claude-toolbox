"""Evidence integrity checks for Task 2, independent of model behavior."""

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("capture_seeds", Path(__file__).with_name("capture-seeds.py"))
capture = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(capture)


class CaptureTests(unittest.TestCase):
    def test_failed_capture_is_sealed_after_output_stream_closes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            original_seal = capture.seal

            def fail(destination):
                (destination / "command.json").write_text("{}")
                with (destination / "stderr.txt").open("w") as stream:
                    stream.write("test-secret-value")
                    raise RuntimeError("capture failed")

            with patch.object(capture, "_run_claude", side_effect=fail), patch.object(
                    capture, "seal", side_effect=lambda p: original_seal(p, ["test-secret-value"])):
                with self.assertRaisesRegex(RuntimeError, "capture failed"):
                    capture.run_claude(root)
            self.assertEqual((root / "stderr.txt").read_text(), "[credential redacted]")
            self.assertTrue((root / "manifest.json").exists())

    def test_package_seal_redacts_every_artifact_and_hashes_sanitized_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("report.md", "stderr.txt", "events.jsonl", "payloads/blob", "final/source.py"):
                path = root / name
                path.parent.mkdir(exist_ok=True)
                path.write_text("test-secret-value")
            capture.seal(root, ["test-secret-value"])
            for name in ("report.md", "stderr.txt", "events.jsonl", "payloads/blob", "final/source.py"):
                self.assertEqual((root / name).read_text(), "[credential redacted]")
            import json
            manifest = json.loads((root / "manifest.json").read_text())
            self.assertNotIn("manifest.json", manifest)
            self.assertEqual(manifest["report.md"], capture.sha(b"[credential redacted]"))
            self.assertEqual(len(json.loads((root / "credential-redactions.json").read_text())["redactions"]), 5)

    def test_refused_retry_leaves_all_artifacts_unchanged(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "command.json").write_text("original command identity")
            before = capture.files(root)
            with self.assertRaises(FileExistsError):
                capture.run_claude(root)
            self.assertEqual(before, capture.files(root))

    def test_private_reasoning_removed_while_call_arguments_survive(self):
        event = {"type": "assistant", "parent_tool_use_id": "dispatch-1", "message": {"content": [
            {"type": "thinking", "thinking": "private"},
            {"type": "redacted_thinking", "data": "private"},
            {"type": "tool_use", "id": "read-1", "name": "Read", "input": {"file_path": "/tmp/source.py"}}]}}
        retained = capture.sanitize_claude(event)
        self.assertEqual(retained["parent_tool_use_id"], "dispatch-1")
        self.assertEqual(retained["message"]["content"], event["message"]["content"][2:])
        self.assertEqual(len(event["message"]["content"]), 3)

    def test_non_message_notices_do_not_crash_or_become_tool_results(self):
        self.assertIsNone(capture.sanitize_claude({"type": "user", "message": "notice"}))
        self.assertEqual(capture.sanitize_claude({"type": "system", "message": "notice"}),
                         {"type": "system", "message": "notice"})

    def test_dispatch_snapshot_survives_actor_deleting_payload(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            work = root / "actor"
            evidence = root / "controller"
            work.mkdir()
            evidence.mkdir()
            source = work / "client.py"
            source.write_text("public source\n")
            capture.capture_payloads({"relevant_files": [str(source)]}, work, evidence, 42)
            source.unlink()
            self.assertEqual((evidence / "payloads" / capture.sha(b"public source\n")).read_bytes(), b"public source\n")
            self.assertIn('"event_sequence": 42', (evidence / "payload-events.jsonl").read_text())

    def test_runner_credentials_and_controller_paths_are_not_payload_inputs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            work = root / "actor"
            evidence = root / "controller"
            (work / ".runner").mkdir(parents=True)
            evidence.mkdir()
            secret = work / ".runner/config.json"
            secret.write_text("credential")
            oracle = evidence / "oracle.json"
            oracle.write_text("expected answer")
            capture.capture_payloads({"paths": [str(secret), str(oracle)]}, work, evidence, 1)
            self.assertFalse((evidence / "payloads").exists())


if __name__ == "__main__":
    unittest.main()
