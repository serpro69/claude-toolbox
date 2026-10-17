"""Offline controls for explicit PAL exclusion with unchanged measured prompts."""
import hashlib
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import runner


class RunnerTests(unittest.TestCase):
    def test_exact_declared_pairs_use_disjoint_fresh_paths(self):
        with patch.object(runner.driver.controller, "SNAPSHOTS", {
                "baseline": Path("/tmp/base"), "candidate": Path("/tmp/candidate")}):
            jobs = runner.jobs_for(Path("freeze.json"))
        self.assertEqual({(j.case, j.side, j.repetition) for j in jobs}, {
            (case, side, repetition) for case in ("R3", "R5", "R9-recovery")
            for side in ("baseline", "candidate") for repetition in (1, 2)})
        self.assertEqual(len(jobs), 12)
        self.assertEqual(len({j.workspace for j in jobs}), 12)
        self.assertEqual(len({j.evidence for j in jobs}), 12)
        self.assertTrue(all(j.provider == "claude" and j.mode == "isolated" and not j.binding
                            for j in jobs))

    def check_preparation(self, binding):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace, evidence = root / "actor", root / "evidence"
            (workspace / ".runner").mkdir(parents=True)
            evidence.mkdir()
            capy = {"command": "capy", "args": ["serve"]}
            original = json.dumps({"mcpServers": {"capy": capy, "pal": {"command": "pal"}}}).encode()
            (workspace / ".runner/mcp.json").write_bytes(original)
            launch = {"prompt": "ordinary request", "models": {"claude": "pinned", "pal": "old"},
                      "mcp": {"capy": capy, "pal": {"command": "pal"}}}
            (evidence / "launch.json").write_text(json.dumps(launch))
            (evidence / "prompt.txt").write_text("ordinary request\n")
            original_hash = hashlib.sha256(original).hexdigest()
            (evidence / "prepared.json").write_text(json.dumps({
                "runtime_files": {".runner/mcp.json": original_hash}, "patch_sha256": "unchanged"}))
            with patch.object(runner.driver, "prepare_job"):
                runner.prepare(SimpleNamespace(binding=binding, workspace=workspace, evidence=evidence))
            selected = workspace / ".runner/mcp-no-pal.json"
            self.assertEqual(json.loads(selected.read_text()), {"mcpServers": {"capy": capy}})
            self.assertEqual((workspace / ".runner/mcp.json").read_bytes(), original)
            prepared = json.loads((evidence / "prepared.json").read_text())
            self.assertEqual(prepared["runtime_files"], {
                ".runner/mcp.json": original_hash,
                ".runner/mcp-no-pal.json": hashlib.sha256(selected.read_bytes()).hexdigest()})
            self.assertEqual(prepared["patch_sha256"], "unchanged")
            for key, name in [("launch_sha256", "launch.json"), ("prompt_sha256", "prompt.txt")]:
                self.assertEqual(prepared[key], hashlib.sha256((evidence / name).read_bytes()).hexdigest())
            actual = json.loads((evidence / "launch.json").read_text())
            self.assertEqual(actual["mcp"], {"capy": capy})
            self.assertEqual(actual["models"]["claude"], "pinned")
            expected = runner.BINDING_PROMPT if binding else "ordinary request"
            self.assertEqual(actual["prompt"], expected)
            self.assertEqual((evidence / "prompt.txt").read_text(), expected + "\n")

    def test_binding_excludes_pal_and_binds_actual_config(self):
        self.check_preparation(True)

    def test_measured_preparation_preserves_ordinary_prompt(self):
        self.check_preparation(False)

    def test_selected_config_is_only_command_change_and_restores_on_failure(self):
        original = runner.driver.capture.command_for
        before = original("ordinary request")
        def failed_capture(job, interruption):
            actual = runner.driver.capture.command_for("ordinary request")
            expected = list(before)
            expected[expected.index("--mcp-config") + 1] = ".runner/mcp-no-pal.json"
            self.assertEqual(actual, expected)
            raise RuntimeError("capture failed")
        with patch.object(runner.driver, "capture_job", side_effect=failed_capture):
            with self.assertRaisesRegex(RuntimeError, "capture failed"):
                runner.capture(SimpleNamespace(evidence=Path("example")), [None])
        self.assertIs(runner.driver.capture.command_for, original)


if __name__ == "__main__":
    unittest.main()
