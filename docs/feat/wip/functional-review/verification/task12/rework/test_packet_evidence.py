"""The unchanged evidence adapter preserves successful packet Read results."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

VERIFICATION = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("previous_grading", VERIFICATION / "task8/prepare_grading.py")
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class PacketEvidenceTests(unittest.TestCase):
    def test_read_bytes_survive_and_unread_manifest_entry_is_not_invented(self):
        packet = "Instruction packet: part 1/2\nBEGIN SOURCE /plugin/profiles/python/DETECTION.md\noriginal instruction bytes\nEND PACKET PART 1/2\n"
        events = [
            {"sequence": 1, "event": {"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "read1", "name": "Read", "input": {"file_path": "/tmp/packet/part-01.md"}}]}}},
            {"sequence": 2, "event": {"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "read1", "content": packet}]}}},
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "events.jsonl"
            path.write_text("\n".join(json.dumps(e) for e in events) + "\n")
            seal = {"events.jsonl": hashlib.sha256(path.read_bytes()).hexdigest()}
            observed = adapter.observable_events(root, "claude", seal)
        self.assertEqual(len(observed), 2)
        self.assertEqual(observed[1]["block"]["content"], packet)
        self.assertEqual(observed[1]["block"]["tool_use_id"], "read1")
        self.assertEqual([e["source_sequence"] for e in observed], [1, 2])


if __name__ == "__main__":
    unittest.main()
