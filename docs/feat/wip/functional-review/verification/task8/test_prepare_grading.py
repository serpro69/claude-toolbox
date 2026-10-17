"""Offline evidence-boundary regressions; these do not test model behavior."""

import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import prepare_grading as prepare


class EvidenceTests(unittest.TestCase):
    def test_seal_rejects_tampering_and_missing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            path = root / "evidence.txt"
            path.write_text("original")
            sha = prepare.digest(path)
            self.assertEqual(prepare.checked_file(root, path.name, sha), path)
            path.write_text("changed")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                prepare.checked_file(root, path.name, sha)
            path.unlink()
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                prepare.checked_file(root, path.name, sha)

    def test_manifest_paths_cannot_escape_through_links_or_traversal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            outside = root / "outside.txt"
            outside.write_text("not permitted")
            package = root / "package"
            package.mkdir()
            (package / "link").symlink_to(outside)
            for path in ("../outside.txt", str(outside), "link"):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    prepare.checked_file(package, path, prepare.digest(outside))

    def test_claude_preserves_returned_bytes_and_parent_edge_without_reasoning(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            records = [
                {"sequence": 1, "event": {"type": "system", "message": "host notice"}},
                {"sequence": 7, "event": {"type": "assistant", "session_id": "s",
                    "parent_tool_use_id": "dispatch-1", "message": {"content": [
                        {"type": "thinking", "thinking": "PRIVATE"},
                        {"type": "tool_use", "id": "read-1", "name": "Read", "input": {"path": "rules"}}]}}},
                {"sequence": 9, "event": {"type": "user", "session_id": "s",
                    "parent_tool_use_id": "dispatch-1", "message": {"content": [
                        {"type": "tool_result", "tool_use_id": "read-1", "content": "returned rules"}]}}},
            ]
            (root / "events.jsonl").write_text("\n".join(map(json.dumps, records)))
            events = prepare.observable_events(root, "claude", {"events.jsonl": prepare.digest(root / "events.jsonl")})
            self.assertEqual([e["id"] for e in events], ["e7.1", "e9.0"])
            self.assertEqual(events[1]["actor"], "child-of:dispatch-1")
            self.assertEqual(events[1]["block"]["content"], "returned rules")
            self.assertNotIn("PRIVATE", json.dumps(events))

    def test_trusted_root_can_live_below_a_platform_directory_alias(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            real = root / "real" / "evidence"
            real.mkdir(parents=True)
            (real / "file.txt").write_text("sealed")
            (root / "alias").symlink_to(real.parent, target_is_directory=True)
            via_alias = root / "alias/evidence"
            self.assertEqual(prepare.checked_file(via_alias, "file.txt", prepare.digest(real / "file.txt")), via_alias / "file.txt")

    def test_codex_preserves_failure_and_timing_without_private_items(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            records = [
                {"item": {"type": "reasoning", "id": "r", "text": "PRIVATE"}},
                {"item": {"type": "omitted_private_reasoning", "id": "r2"}},
                {"startedAtMs": 10, "completedAtMs": 20, "item": {
                    "id": "cmd1", "type": "commandExecution", "exitCode": 1,
                    "command": "cat rules", "aggregatedOutput": "permission denied"}},
            ]
            (root / "items-session1.json").write_text(json.dumps(records))
            (root / "items-unsealed.json").write_text(json.dumps([
                {"item": {"id": "invented", "type": "agentMessage", "text": "unsealed"}}]))
            events = prepare.observable_events(root, "codex", {"items-session1.json": prepare.digest(root / "items-session1.json")})
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["id"], "cmd1")
            self.assertEqual(events[0]["completedAtMs"], 20)
            self.assertEqual(events[0]["item"]["exitCode"], 1)
            self.assertNotIn("PRIVATE", json.dumps(events))
            self.assertNotIn("invented", json.dumps(events))

    def test_codex_requires_sealed_event_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "items-unsealed.json").write_text("[]")
            with self.assertRaisesRegex(ValueError, "No sealed"):
                prepare.observable_events(root, "codex", {})

    def test_existing_destination_is_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "existing"
            target.mkdir()
            (target / "owned.txt").write_text("preserve")
            with self.assertRaises(FileExistsError):
                prepare.prepare(target)
            self.assertEqual(list(target.iterdir()), [target / "owned.txt"])
            self.assertEqual((target / "owned.txt").read_text(), "preserve")

    def test_added_unfrozen_oracle_is_not_imported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            replica = root / "repo"
            for skill, name in prepare.CASES.values():
                relative = Path("klaude-plugin/skills") / skill / "evals" / name
                shutil.copytree(prepare.REPO / relative, replica / relative)
                (replica / relative / "oracle/unfrozen.txt").write_text("injected expected answer")
            agent = Path("klaude-plugin/agents/eval-grader.md")
            (replica / agent).parent.mkdir(parents=True)
            shutil.copyfile(prepare.REPO / agent, replica / agent)
            fresh = root / "sealed"
            with patch.object(prepare, "REPO", replica):
                # source_path is provenance only; keep original captures inside
                # the replica's declared repository boundary for this test.
                with patch.object(prepare, "VERIFICATION", replica / "verification"):
                    shutil.copytree(prepare.HERE.parent / "task2", replica / "verification/task2")
                    for name in ("task2-frozen.json", "task2-rubric.md"):
                        shutil.copyfile(prepare.HERE.parent / name, replica / "verification" / name)
                    prepare.prepare(fresh)
            self.assertEqual(len(list(fresh.glob("*/manifest.json"))), 16)
            self.assertEqual(list(fresh.rglob("expected-unfrozen.txt")), [])
            self.assertEqual(len(list(fresh.glob("*/expected-expected-results.json"))), 16)


if __name__ == "__main__":
    unittest.main()
