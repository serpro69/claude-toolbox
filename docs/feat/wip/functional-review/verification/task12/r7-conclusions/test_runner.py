"""Offline controls for the Task 12.13 adapter; no model or service calls."""
import argparse
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import runner


class RunnerTests(unittest.TestCase):
    def test_selected_pairs_have_unique_fresh_locations(self):
        jobs = runner.jobs_for(Path("/tmp/frozen.json"))
        self.assertEqual(len(jobs), 48)
        self.assertEqual({job.case for job in jobs}, {"R3", "R5", "R7"})
        combinations = {(job.provider, job.side, job.case, job.mode, job.repetition) for job in jobs}
        self.assertEqual(len(combinations), 48)
        self.assertEqual(len({job.workspace for job in jobs}), 48)
        self.assertEqual(len({job.evidence for job in jobs}), 48)
        for job in jobs:
            self.assertEqual(job.workspace.parent, runner.WORKSPACES)
            self.assertEqual(job.evidence.parent, runner.HERE / "runs")

    def test_claude_preparation_binds_actual_mcp_without_pal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace, evidence = root / "subject", root / "evidence"
            (workspace / ".runner").mkdir(parents=True)
            evidence.mkdir()
            original = {"mcpServers": {"capy": {"command": "capy"}, "pal": {"command": "pal"}}}
            (workspace / ".runner/mcp.json").write_text(json.dumps(original))
            (evidence / "launch.json").write_text(json.dumps({"models": {"pal": "prior"}, "mcp": original["mcpServers"]}))
            (evidence / "prepared.json").write_text(json.dumps({"runtime_files": {}, "launch_sha256": "prior"}))
            job = argparse.Namespace(provider="claude", workspace=workspace, evidence=evidence)
            with mock.patch.object(runner.matrix, "prepare"):
                runner.prepare(job)
            actual = workspace / ".runner/mcp-no-pal.json"
            self.assertEqual(json.loads(actual.read_text()), {"mcpServers": {"capy": {"command": "capy"}}})
            self.assertEqual(json.loads((workspace / ".runner/mcp.json").read_text()), original)
            prepared = json.loads((evidence / "prepared.json").read_text())
            self.assertEqual(prepared["runtime_files"][".runner/mcp-no-pal.json"], runner.matrix.seed.sha(actual.read_bytes()))
            self.assertEqual(prepared["launch_sha256"], runner.matrix.seed.sha((evidence / "launch.json").read_bytes()))

    def test_launch_selects_no_pal_and_restores_after_failure(self):
        for failure in (False, True):
            with self.subTest(failure=failure):
                original = mock.Mock(return_value=["claude", "--mcp-config", ".runner/mcp.json", "--strict-mcp-config"])

                def invoke(job, interruption):
                    command = runner.matrix.driver.capture.command_for("ordinary prompt")
                    self.assertEqual(command, ["claude", "--mcp-config", ".runner/mcp-no-pal.json", "--strict-mcp-config"])
                    if failure:
                        raise RuntimeError("capture failed")
                    return 0

                with mock.patch.object(runner.matrix.driver.capture, "command_for", original), mock.patch.object(runner.matrix, "capture", side_effect=invoke):
                    job = argparse.Namespace(provider="claude")
                    if failure:
                        with self.assertRaisesRegex(RuntimeError, "capture failed"):
                            runner.capture(job, [0])
                    else:
                        self.assertEqual(runner.capture(job, [0]), 0)
                    self.assertIs(runner.matrix.driver.capture.command_for, original)

    def test_codex_keeps_inherited_configuration_and_transport(self):
        job = argparse.Namespace(provider="codex")
        with mock.patch.object(runner.matrix, "prepare") as prepare, mock.patch.object(runner.matrix, "capture", return_value=7) as capture:
            runner.prepare(job)
            self.assertEqual(runner.capture(job, [0]), 7)
        prepare.assert_called_once_with(job)
        capture.assert_called_once_with(job, [0])


if __name__ == "__main__":
    unittest.main()
