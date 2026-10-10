"""Offline capture-integrity checks; never actor inputs."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import controller


class CaptureIntegrityTests(unittest.TestCase):
    def test_public_sanitization_removes_private_reasoning_and_credentials(self):
        value = {"item": {"type": "reasoning", "text": "private"},
                 "arguments": {"path": "source.py", "key": "fake-secret"},
                 "encrypted_content": "ciphertext"}
        result = controller.sanitized(value, ["fake-secret"])
        self.assertEqual(result["item"], {"type": "omitted_private_reasoning"})
        self.assertEqual(result["arguments"], {"path": "source.py", "key": "[credential redacted]"})
        self.assertNotIn("encrypted_content", result)

    def test_retries_cannot_overwrite_existing_capture(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "command.json").write_text("original")
            before = controller.seed.files(root)
            with self.assertRaises(FileExistsError):
                controller.run(root, root)
            self.assertEqual(controller.seed.files(root), before)

    def test_startup_failure_still_seals_and_redacts_final_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evidence, workspace = root / "evidence", root / "workspace"
            evidence.mkdir()
            workspace.mkdir()
            (evidence / "launch.json").write_text('{"prompt": "probe"}')
            with patch.object(controller, "secrets", return_value=["fake-secret"]), \
                 patch.object(controller, "Server", side_effect=RuntimeError("fake-secret startup failed")), \
                 patch.object(controller.seed, "subject_snapshot", return_value={}), \
                 patch.object(controller.seed, "git", return_value=b""):
                with self.assertRaisesRegex(RuntimeError, "startup failed"):
                    controller.run(workspace, evidence, binding=True)
            self.assertTrue((evidence / "manifest.json").is_file())
            self.assertNotIn("fake-secret", (evidence / "capture-error.json").read_text())
            self.assertIn("[credential redacted]", (evidence / "capture-error.json").read_text())

    def test_child_discovery_retains_activity_link_when_wait_is_empty(self):
        self.assertEqual(controller.child_ids({"type": "collabAgentToolCall", "receiverThreadIds": []}), set())
        self.assertEqual(controller.child_ids({"type": "subAgentActivity", "agentThreadId": "actual-child"}), {"actual-child"})

    def test_payload_snapshot_excludes_runner_and_keeps_actual_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            work, evidence = root / "work", root / "evidence"
            (work / ".runner").mkdir(parents=True)
            evidence.mkdir()
            source = work / "source.py"
            secret = work / ".runner/credentials.json"
            source.write_text("source bytes\n")
            secret.write_text("private")
            controller.snapshot_payloads({"paths": [str(source), str(secret)]}, work, evidence, 3)
            rows = [json.loads(line) for line in (evidence / "payload-events.jsonl").read_text().splitlines()]
            self.assertEqual([entry["path"] for entry in rows[0]["files"]], [str(source)])
            source.unlink()
            artifact = evidence / rows[0]["files"][0]["artifact"]
            self.assertEqual(artifact.read_text(), "source bytes\n")

    def test_unmatched_catalog_fails_before_reading_other_plugin_files(self):
        class FakeServer:
            credentials = []

            def call(self, method, params):
                return {"data": [{"skills": [{"name": "kk:implement", "enabled": True,
                       "pluginId": "kk@unfiltered", "path": "/unfiltered/skills/implement/SKILL.md"}]}]}

        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "mixed"):
                controller.verify_catalog(FakeServer(), Path(temporary), Path(temporary))

    def test_prepare_restores_retained_validator_after_failure(self):
        original = controller.seed.verify_frozen
        with patch.object(controller.seed, "prepare", side_effect=RuntimeError("staging failure")):
            with self.assertRaisesRegex(RuntimeError, "staging failure"):
                controller.prepare("R3", Path("/tmp/unused-actor"), Path("/tmp/unused-evidence"))
        self.assertIs(controller.seed.verify_frozen, original)

    def test_v2_validator_rejects_wrong_rubric(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "freeze.json"
            path.write_text('{"revision": 2, "rubric_sha256": "wrong"}')
            with self.assertRaisesRegex(ValueError, "rubric mismatch"):
                controller.verify_v2(path)

    def test_mismatched_launch_freeze_cannot_start_or_create_command(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "launch.json").write_text('{"prompt": "ordinary", "fixture_manifest_sha256": "wrong"}')
            with patch.object(controller, "verify_v2", return_value={}):
                with self.assertRaisesRegex(ValueError, "different freeze"):
                    controller.run(root, root)
            self.assertFalse((root / "command.json").exists())


if __name__ == "__main__":
    unittest.main()
