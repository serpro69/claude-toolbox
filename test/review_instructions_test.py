"""Instruction packaging tests; predicates remain owned by profile prose."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "klaude-plugin/skills/review-code/scripts/prepare_instructions.py"
spec = importlib.util.spec_from_file_location("prepare_instructions", SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class PacketTests(unittest.TestCase):
    def packet(self, phase, profiles=(), selected=(), skipped=()):
        sources, outcomes = helper.select_sources(helper.ROOT, phase, profiles, selected, skipped)
        result = helper.write_packet(helper.ROOT, phase, sources, outcomes)
        if result["parts"]:
            destination = Path(result["parts"][0]["path"]).parent
            self.addCleanup(shutil.rmtree, destination)
        text = b""
        for entry in result["parts"]:
            path = Path(entry["path"])
            content = path.read_bytes()
            self.assertEqual(hashlib.sha256(content).hexdigest(), entry["sha256"])
            self.assertLessEqual(len(content), helper.PART_BYTES + 200)
            # Strip framing on each part before reconstructing original bytes.
            text += content.split(b"\n\n", 1)[1].rsplit(b"\nEND PACKET PART", 1)[0]
        for source, content in sources:
            self.assertIn(content, text)
        self.assertIn("NOT ESTABLISHED", result["gate"])
        return result

    def test_bootstrap_contains_every_common_source_and_known_detection(self):
        packet = self.packet("bootstrap")
        paths = {entry["source"] for entry in packet["sources"]}
        expected = set(helper.COMMON) | {f"profiles/{p}/DETECTION.md" for p in helper.known_profiles(helper.ROOT)}
        self.assertEqual(paths, {str(helper.ROOT / p) for p in expected})
        self.assertEqual(packet["routing_outcomes"], [])

    def test_profiles_then_all_python_checklists(self):
        indexes = self.packet("profiles", ["python"])
        self.assertEqual(len(indexes["sources"]), 1)
        selected = ["python/" + name for name in helper.checklist_entries(helper.ROOT, "python")]
        packet = self.packet("checklists", ["python"], selected)
        self.assertEqual(len(packet["sources"]), 4)

    def test_missing_decision_and_skipped_always_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Every active-profile"):
            helper.select_sources(helper.ROOT, "checklists", ["python"], ["python/code-quality-checklist.md"])
        entries = list(helper.checklist_entries(helper.ROOT, "python"))
        with self.assertRaisesRegex(ValueError, "always-load"):
            helper.select_sources(helper.ROOT, "checklists", ["python"],
                ["python/" + n for n in entries[1:]], ["python/" + entries[0] + "=small diff"])

    def test_false_conditional_is_retained_without_loading(self):
        entries = helper.checklist_entries(helper.ROOT, "skill-md")
        load = ["skill-md/" + n for n, required in entries.items() if required]
        skip = ["skill-md/" + n + "=standalone skill outside provider/plugin tree" for n, required in entries.items() if not required]
        result = self.packet("checklists", ["skill-md"], load, skip)
        self.assertEqual(len(result["sources"]), 1)
        self.assertEqual(len(result["routing_outcomes"]), 2)

    def test_no_profile_means_no_invented_checklist(self):
        sources, outcomes = helper.select_sources(helper.ROOT, "checklists")
        self.assertEqual((sources, outcomes), ([], []))

    def test_unknown_profile_and_unlisted_checklist_rejected(self):
        for args in [("profiles", ["../python"], [], []),
                     ("checklists", ["python"], ["python/../../oracle/gold.md"], [])]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                helper.select_sources(helper.ROOT, *args)

    def test_external_symlink_cannot_enter_instruction_packet(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "plugin"
            root.mkdir()
            (root / "instruction.md").symlink_to(SCRIPT)
            with self.assertRaisesRegex(ValueError, "boundary"):
                helper.read_instruction(root, "instruction.md")

    def test_evaluator_paths_are_rejected_even_inside_plugin(self):
        with self.assertRaisesRegex(ValueError, "boundary"):
            helper.read_instruction(helper.ROOT, "skills/review-code/evals/test.md")

    def test_internal_link_to_evaluator_material_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "evals").mkdir()
            (root / "evals/answer.md").write_text("grader-only")
            (root / "instruction.md").symlink_to("evals/answer.md")
            with self.assertRaisesRegex(ValueError, "boundary"):
                helper.read_instruction(root, "instruction.md")


if __name__ == "__main__":
    unittest.main(verbosity=2)
