"""Offline matrix coverage and failed-capture cleanup regressions."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import matrix


class MatrixTests(unittest.TestCase):
    def test_all_declared_modes_have_independent_two_by_two_pairs(self):
        jobs = matrix.jobs_for(Path("freeze"))
        self.assertEqual(len(jobs), 192)
        self.assertEqual(len({job.workspace for job in jobs}), 192)
        self.assertEqual(len({job.evidence for job in jobs}), 192)
        for provider in ("claude", "codex"):
            self.assertEqual(sum(j.provider == provider for j in jobs), 96)
            for case, (_, _, modes) in matrix.controller.CASES.items():
                for mode in modes:
                    actual = {(j.side, j.repetition) for j in jobs
                              if (j.provider, j.case, j.mode) == (provider, case, mode)}
                    self.assertEqual(actual, {("baseline", 1), ("baseline", 2),
                                              ("candidate", 1), ("candidate", 2)})

    def test_replay_prompt_keeps_checkpoint_and_provider_invocation(self):
        for case in ("R8-zero", "R8-failure"):
            self.assertIn("/kk:review-code:isolated", matrix.seed.prompt_for(case, "replay", "claude"))
            self.assertIn("$kk:review-code isolated", matrix.seed.prompt_for(case, "replay", "codex"))
            self.assertIn("checkpoint.md", matrix.seed.prompt_for(case, "replay", "codex"))

    def test_codex_install_failure_restores_trust_and_seals_error(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evidence = root / "evidence"
            evidence.mkdir()
            config = root / ".codex/config.toml"
            config.parent.mkdir()
            config.write_text("")
            job = SimpleNamespace(evidence=evidence, workspace=root / "actor", side="baseline")
            operations = []
            def admin(operation, *args):
                operations.append(operation)
                if operation == "install":
                    raise RuntimeError("install failed")
            with patch.object(matrix, "validate_codex", return_value={}), \
                 patch.object(matrix, "codex_configure"), \
                 patch.object(matrix, "HERE", root), \
                 patch.object(Path, "home", return_value=root), \
                 patch.object(matrix.codex, "admin", side_effect=admin), \
                 patch.object(matrix, "restore_trust", side_effect=lambda *args: operations.append("untrust")), \
                 patch.object(matrix.codex, "secrets", return_value=[]), \
                 patch.object(matrix.seed, "subject_snapshot", return_value={}), \
                 patch.object(matrix.seed, "git", return_value=b""):
                with self.assertRaisesRegex(RuntimeError, "install failed"):
                    matrix.run_codex(job, [None])
            self.assertEqual(operations, ["trust", "install", "uninstall", "untrust"])
            self.assertEqual(json.loads((evidence / "completion.json").read_text())["exit_code"], 1)
            seal = json.loads((evidence / "manifest.json").read_text())
            self.assertIn("capture-error.json", seal)

    def test_cleanup_failure_does_not_prevent_remaining_finalizers_or_seal(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evidence = root / "evidence"
            evidence.mkdir()
            (root / ".codex").mkdir()
            (root / ".codex/config.toml").write_text("")
            job = SimpleNamespace(evidence=evidence, workspace=root / "actor", side="baseline")
            operations = []
            def admin(operation, *args):
                operations.append(operation)
                if operation in ("install", "uninstall"):
                    raise RuntimeError(operation + " failed")
            with patch.object(matrix, "validate_codex", return_value={}), \
                 patch.object(matrix, "codex_configure"), patch.object(matrix, "HERE", root), \
                 patch.object(Path, "home", return_value=root), \
                 patch.object(matrix.codex, "admin", side_effect=admin), \
                 patch.object(matrix, "restore_trust", side_effect=lambda *args: operations.append("untrust")), \
                 patch.object(matrix.codex, "secrets", return_value=[]), \
                 patch.object(matrix.seed, "subject_snapshot", return_value={}), \
                 patch.object(matrix.seed, "git", return_value=b""):
                with self.assertRaisesRegex(RuntimeError, "install failed") as caught:
                    matrix.run_codex(job, [None])
            self.assertEqual(operations[-1], "untrust")
            self.assertIn("uninstall failed", caught.exception.__notes__[0])
            self.assertTrue((evidence / "manifest.json").is_file())

    def test_successful_actor_with_failed_cleanup_is_sealed_runtime_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            job = SimpleNamespace(evidence=root, workspace=root / "actor")
            def broken():
                raise OSError("uninstall failed")
            with patch.object(matrix.seed, "subject_snapshot", return_value={}), \
                 patch.object(matrix.seed, "git", return_value=b""), \
                 patch.object(matrix.codex, "secrets", return_value=[]):
                result = matrix.finalize_capture(job, [None], True, None, [broken], None)
            self.assertIsInstance(result, OSError)
            self.assertEqual(matrix.runtime.completion_status(root), 1)
            completion = json.loads((root / "completion.json").read_text())
            self.assertTrue(completion["actor_completed"])
            seal = json.loads((root / "manifest.json").read_text())
            self.assertIn("finalization-errors.json", seal)

    def test_trust_mutation_then_admin_failure_still_restores_owned_entry(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "actor"
            evidence = root / "evidence"
            evidence.mkdir()
            config = root / ".codex/config.toml"
            config.parent.mkdir()
            config.write_text("")
            job = SimpleNamespace(evidence=evidence, workspace=workspace, side="baseline")
            operations = []
            def admin(operation, ws, target, record=None):
                operations.append(operation)
                if operation == "trust":
                    target.mkdir(parents=True)
                    matrix.seed.write_json(target / "previous-project-entry.json", {"path": str(ws), "previous": None})
                    config.write_text('[projects.' + json.dumps(str(ws)) + ']\ntrust_level = "trusted"\n')
                    raise RuntimeError("response lost after mutation")
                if operation == "untrust":
                    config.write_text("")
            with patch.object(matrix, "validate_codex", return_value={}), \
                 patch.object(matrix, "codex_configure"), patch.object(matrix, "HERE", root), \
                 patch.object(Path, "home", return_value=root), \
                 patch.object(matrix.codex, "admin", side_effect=admin), \
                 patch.object(matrix.codex, "secrets", return_value=[]), \
                 patch.object(matrix.seed, "subject_snapshot", return_value={}), \
                 patch.object(matrix.seed, "git", return_value=b""):
                with self.assertRaisesRegex(RuntimeError, "response lost"):
                    matrix.run_codex(job, [None])
            self.assertEqual(operations, ["trust", "untrust"])
            self.assertEqual(config.read_text(), "")
            self.assertEqual(matrix.runtime.completion_status(evidence), 1)


if __name__ == "__main__":
    unittest.main()
