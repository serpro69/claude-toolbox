"""Offline evidence-validity controls; no actor or external service calls."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

import runner

ROOT = runner.controller.ROOT
EVALS = ROOT / "klaude-plugin/skills/review-code/evals"


def client(case, side):
    path = EVALS / runner.CASES[case][1] / "test-files" / side / "client.py"
    spec = importlib.util.spec_from_file_location("fixture_" + case + "_" + side, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DocumentedProvider:
    """Controller-only executable model of protocol.md, never a deployed source."""
    def __init__(self, version):
        self.version = version
        self.label = "Old label"

    def put(self, path, body):
        if path != "/settings" or set(body) != {"display_name"}:
            raise ValueError("unexpected request shape")
        value = body["display_name"]
        if value is None:
            if self.version == 1:
                raise ValueError("HTTP 422")
            self.label = None
        else:
            self.label = value.strip()
        return {"ok": True}


class DiagnosticTests(unittest.TestCase):
    def setUp(self):
        runner.configure()

    def test_four_standard_current_source_jobs_only(self):
        jobs = runner.jobs_for(Path("/tmp/unused-freeze.json"))
        self.assertEqual(len(jobs), 4)
        self.assertEqual({(j.case, j.repetition) for j in jobs},
                         {("R7M", 1), ("R7M", 2), ("R7B", 1), ("R7B", 2)})
        self.assertEqual({j.provider for j in jobs}, {"claude"})
        self.assertEqual({j.mode for j in jobs}, {"standard"})
        self.assertEqual({j.side for j in jobs}, {"candidate"})
        self.assertEqual(len({j.workspace for j in jobs}), 4)
        self.assertEqual(len({j.evidence for j in jobs}), 4)
        for job in jobs:
            self.assertEqual(job.snapshot, runner.HERE / "source-inputs")
            self.assertFalse(any((p / "SKILL.md").exists() for p in job.workspace.parents))

    def test_complete_metadata_distinct_ids_and_shared_natural_prompt(self):
        prompts, identifiers, protocols = set(), set(), set()
        for case, (_, name, _) in runner.CASES.items():
            root = EVALS / name
            data = json.loads((root / "eval.json").read_text())
            actual = {str(p.relative_to(root)) for p in (root / "test-files").rglob("*") if p.is_file()}
            self.assertEqual(set(data["files"]), actual)
            self.assertTrue(all(p.startswith("test-files/") for p in data["files"]))
            self.assertEqual(len(data["assertions"]), 6)
            self.assertEqual([a["id"] for a in data["assertions"]],
                             [str(data["id"]) + "." + str(i) for i in range(1, 7)])
            self.assertTrue((root / "oracle/expected-results.json").is_file())
            for side in ("before", "after"):
                subject = root / "test-files" / side
                self.assertFalse((subject / "oracle").exists())
                self.assertFalse((subject / "eval.json").exists())
                protocols.add((subject / "protocol.md").read_text())
            prompts.add(data["prompt"])
            identifiers.add(data["id"])
        self.assertEqual(identifiers, {19, 20})
        self.assertEqual(len(prompts), 1)
        self.assertEqual(len(protocols), 1)

    def test_material_capability_difference_and_preserved_save(self):
        before, after = client("R7M", "before"), client("R7M", "after")
        self.assertFalse(hasattr(before, "clear_name"))
        for version in (1, 2):
            for value in ("Ada", "", "  Ada  ", "Ada Lovelace", " \t"):
                old, new = DocumentedProvider(version), DocumentedProvider(version)
                self.assertEqual(before.save(old, value), after.save(new, value))
                self.assertEqual(old.label, new.label)
        old_provider = DocumentedProvider(1)
        with self.assertRaisesRegex(ValueError, "^HTTP 422$"):
            after.clear_name(old_provider)
        self.assertEqual(old_provider.label, "Old label")
        new_provider = DocumentedProvider(2)
        self.assertEqual(after.clear_name(new_provider), {"ok": True})
        self.assertIsNone(new_provider.label)
        empty_provider = DocumentedProvider(2)
        after.save(empty_provider, "")
        self.assertEqual(empty_provider.label, "")

    def test_benign_equivalence_for_boundaries_and_unicode(self):
        before, after = client("R7B", "before"), client("R7B", "after")
        values = ("", "Ada", "Ada Lovelace", " \t\n", "\u00a0Ada\u3000",
                  "\u200bAda\u200b", "\x1cAda\x1f", " A\tB ")
        for version in (1, 2):
            for value in values:
                with self.subTest(version=version, value=value):
                    old, new = DocumentedProvider(version), DocumentedProvider(version)
                    self.assertEqual(before.save(old, value), after.save(new, value))
                    self.assertEqual(old.label, new.label)

    def test_all_supplied_snapshot_suites_execute(self):
        for case, (_, name, _) in runner.CASES.items():
            for side in ("before", "after"):
                with self.subTest(case=case, side=side):
                    result = subprocess.run(
                        [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"],
                        cwd=EVALS / name / "test-files" / side,
                        text=True, capture_output=True, check=True)
                    self.assertIn("Ran ", result.stderr)
                    self.assertNotIn("Ran 0 tests", result.stderr)

if __name__ == "__main__":
    unittest.main()
