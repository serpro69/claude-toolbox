"""Actual-capture and negative metadata controls; no actors or sealed-file edits."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import listing_audit as audit
import listing_guard as guard
import successor as s


class ListingAuditTests(unittest.TestCase):
    def setUp(self):
        self.adapter = s.Adapter()
        self.source = s.HERE / "binding-claude-candidate"
        self.snapshot = self.adapter.root / "candidate/retained/klaude-plugin"
        self.workspace = Path(s.inputs.read(self.source / "launch.json")["workspace"])
        self.bundle = self.workspace / "plugins/kk"
        self.rows = [json.loads(line) for line in (self.source / "events.jsonl").read_text().splitlines()]
        call = next(r for r in self.rows if r["sequence"] == 52)
        block = call["event"]["message"]["content"][0]
        self.call = {"event": 52, "actor": "main", "args": block["input"]}
        result = next(r for r in self.rows if r["sequence"] == 53)
        block = result["event"]["message"]["content"][0]
        self.result = {"event": 53, "error": False, "text": audit.original.content_text(block["content"]),
                       "meta": result["event"]["tool_use_result"]}

    def inspect(self, call=None, result=None):
        return audit.instruction_listing(call or self.call, result or self.result,
            self.workspace, self.bundle, self.snapshot)

    def test_actual_candidate_listing_and_required_reads_pass_without_capture_changes(self):
        before = s.inputs.sha(self.source / "events.jsonl")
        with self.assertRaisesRegex(ValueError, "unexpected binding tool"):
            audit.original.claude(self.source, self.snapshot, "candidate")
        result = audit.claude(self.source, self.snapshot, "candidate")
        self.assertEqual([len(r["paths"]) for r in result["instruction_listings"]], [6, 17])
        self.assertEqual(len([r for r in result["reads"] if r["path"].endswith("/DETECTION.md")]), 8)
        self.assertEqual(s.inputs.sha(self.source / "events.jsonl"), before)

    def test_actual_baseline_audit_is_unchanged(self):
        source = s.HERE / "binding-claude-baseline"
        snapshot = self.adapter.root / "baseline/retained/klaude-plugin"
        self.assertEqual(audit.claude(source, snapshot, "baseline"),
                         audit.original.claude(source, snapshot, "baseline"))

    def test_unexpected_bases_patterns_and_extra_arguments_fail(self):
        for update in ({"path": str(self.workspace)}, {"pattern": "**/*"},
                       {"pattern": "../*.md"}, {"pattern": "skills/review-code/evals/*.md"},
                       {"extra": "unrecognized"}):
            with self.subTest(update=update):
                call = copy.deepcopy(self.call)
                call["args"].update(update)
                with self.assertRaisesRegex(ValueError, "base/pattern"):
                    self.inspect(call=call)

    def test_failed_missing_truncated_and_inconsistent_results_fail(self):
        with self.assertRaisesRegex(ValueError, "Incomplete or failed"):
            audit.instruction_listing(self.call, None, self.workspace, self.bundle, self.snapshot)
        cases = [({"error": True}, {}), ({}, {"truncated": True}), ({}, {"countIsComplete": False}),
                 ({}, {"numFiles": 5}), ({}, {"totalMatches": 7}), ({"text": "partial"}, {}),
                 ({}, {"filenames": []})]
        for result_update, meta_update in cases:
            with self.subTest(result=result_update, metadata=meta_update):
                result = copy.deepcopy(self.result)
                result.update(result_update)
                result["meta"].update(meta_update)
                with self.assertRaises(ValueError):
                    self.inspect(result=result)

    def test_outside_traversal_subject_evaluator_and_absent_paths_fail(self):
        for name in ("/etc/config.md", "plugins/kk/agents/../agents/code-reviewer.md",
                     "plugins/kk/agents//code-reviewer.md", "app.py",
                     "plugins/kk/skills/review-code/evals/oracle.md", "plugins/kk/agents/absent.md"):
            with self.subTest(name=name):
                result = copy.deepcopy(self.result)
                result["meta"]["filenames"][0] = name
                result["text"] = "\n".join(result["meta"]["filenames"])
                with self.assertRaises(ValueError):
                    self.inspect(result=result)

    def test_absolute_and_relative_aliases_do_not_count_as_distinct_paths(self):
        result = copy.deepcopy(self.result)
        names = result["meta"]["filenames"]
        names[0] = str(self.workspace / names[1])
        result["text"] = "\n".join(names)
        with self.assertRaisesRegex(ValueError, "Duplicate normalized"):
            self.inspect(result=result)

    def test_listing_does_not_replace_missing_detection_read(self):
        rows = copy.deepcopy(self.rows)
        for row in rows:
            event = row["event"]
            message = event.get("message", {})
            blocks = message.get("content", []) if isinstance(message, dict) else []
            for block in blocks if isinstance(blocks, list) else []:
                if (block.get("type") == "tool_use" and block.get("name") == "Read"
                        and block["input"]["file_path"].endswith("profiles/python/DETECTION.md")):
                    # Remove the call rather than fabricating a successful byte receipt.
                    blocks.remove(block)
                    break
        with tempfile.TemporaryDirectory(prefix="fr-listing-missing-read-") as name:
            source = Path(name)
            shutil.copyfile(self.source / "launch.json", source / "launch.json")
            (source / "events.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
            with self.assertRaisesRegex(ValueError, "Incomplete Claude instructions"):
                audit.claude(source, self.snapshot, "candidate")

    def test_other_unexpected_tools_still_fail(self):
        rows = copy.deepcopy(self.rows)
        row = next(r for r in rows if r["sequence"] == 52)
        row["event"]["message"]["content"][0]["name"] = "Edit"
        with tempfile.TemporaryDirectory(prefix="fr-listing-unexpected-tool-") as name:
            source = Path(name)
            shutil.copyfile(self.source / "launch.json", source / "launch.json")
            (source / "events.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
            with self.assertRaisesRegex(ValueError, "unexpected binding tool"):
                audit.claude(source, self.snapshot, "candidate")


class ListingGuardTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="fr-listing-guard-")
        self.addCleanup(temporary.cleanup)
        patcher = patch.object(guard, "FREEZE", Path(temporary.name) / "verifier-freeze.json")
        patcher.start()
        self.addCleanup(patcher.stop)
        guard.freeze_verifier()
        self.adapter = guard.Adapter()

    def test_recomputed_receipt_must_match_retained_audit(self):
        expected = self.adapter.receipt("candidate")
        target = guard.HERE / "audits/binding-claude-candidate.json"
        original_read = s.inputs.read
        for actual in (expected, {}, {"status": "PASS"}):
            def read(path):
                return actual if Path(path) == target else original_read(path)
            with self.subTest(actual=bool(actual)), patch.object(s.inputs, "read", side_effect=read):
                if actual == expected:
                    self.adapter.verify_receipt("candidate")
                else:
                    with self.assertRaisesRegex(ValueError, "Receipt audit differs"):
                        self.adapter.verify_receipt("candidate")

    def test_dependency_drift_fails(self):
        data = s.inputs.read(guard.FREEZE)
        data["dependencies"]["listing_audit.py"] = "0" * 64
        guard.FREEZE.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "Changed or unsafe"):
            guard.verify_verifier()

    def test_preflight_requires_the_selected_verifier(self):
        original_read = s.inputs.read
        def read(path):
            return {"verifier_freeze_sha256": "0" * 64} if Path(path) == guard.HERE / "preflight.json" else original_read(path)
        with patch.object(s.inputs, "read", side_effect=read):
            with self.assertRaisesRegex(ValueError, "bind selected verifier"):
                self.adapter.preflight()

    def test_cli_selects_corrected_strict_adapter_and_restores_on_failure(self):
        previous = s.Adapter
        def fail():
            self.assertIs(s.Adapter, guard.Adapter)
            raise RuntimeError("operation failed")
        with patch.object(s, "main", side_effect=fail):
            with self.assertRaisesRegex(RuntimeError, "operation failed"):
                guard.main()
        self.assertIs(s.Adapter, previous)


if __name__ == "__main__":
    unittest.main()
