"""Offline effort, provenance and routing regressions; never launch an actor."""
import argparse
from contextlib import contextmanager
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import successor


class SuccessorTests(unittest.TestCase):
    @contextmanager
    def adapter(self):
        with tempfile.TemporaryDirectory(prefix="fr-effort-test-") as root:
            root = Path(root)
            for name in successor.DEPENDENCIES:
                shutil.copyfile(successor.HERE / name, root / name)
            with patch.object(successor, "HERE", root), \
                    patch.object(successor, "FROZEN", root / "execution-freeze.json"), \
                    patch.object(successor, "WORKSPACES", root / "actors"):
                adapter = successor.Adapter()
                adapter.freeze()
                yield adapter, root

    def test_freeze_preserves_original_and_detects_source_drift(self):
        original = successor.inputs.sha(successor.runner.FROZEN)
        with self.adapter() as (adapter, root):
            adapter.verify()
            self.assertEqual(original, successor.PREDECESSOR_SHA)
            self.assertEqual(successor.inputs.sha(successor.runner.FROZEN), original)
            with self.assertRaises(FileExistsError):
                adapter.freeze()
            (root / "successor.py").write_text("changed")
            with self.assertRaisesRegex(ValueError, "Changed or unsafe"):
                adapter.verify()

    def test_same_matrix_new_destinations_and_case_rubrics(self):
        with self.adapter() as (adapter, root):
            jobs = adapter.jobs()
            self.assertEqual(len(jobs), 64)
            for job in jobs:
                self.assertEqual(job.evidence.parent, root / "runs")
                self.assertEqual(job.workspace.parent, root / "actors")
                self.assertEqual(job.frozen, successor.FROZEN)
                with adapter.case_context(job.case):
                    self.assertEqual(adapter.verify()["rubric_sha256"], successor.inputs.sha(adapter.rubric(job.case)))

    def test_real_launch_environment_and_record_override_ambient_effort(self):
        adapter = successor.Adapter()
        transport = adapter.prior.matrix.driver.capture
        previous = transport.MODEL_ENV
        with tempfile.TemporaryDirectory(prefix="fr-effort-transport-") as root:
            root = Path(root)
            (root / ".codex").mkdir()
            (root / ".codex/config.toml").write_text("[mcp_servers.pal.env]\n")
            evidence = root / "evidence"
            evidence.mkdir()
            successor.inputs.write_new(evidence / "launch.json", {"workspace": str(root), "prompt": "binding"})
            seen = []
            def capture(command, workspace, environment, *unused):
                seen.append(environment.copy())
                self.assertEqual(environment["CLAUDE_CODE_EFFORT_LEVEL"], "high")
                self.assertEqual(environment["CLAUDE_CODE_SUBAGENT_MODEL"], "claude-opus-5-5")
                return {"exit_code": 0, "interrupted_by": None}
            with patch.object(Path, "home", return_value=root), \
                    patch.object(transport.seed, "run_environment", return_value={"CLAUDE_CODE_EFFORT_LEVEL": "xhigh"}), \
                    patch.object(transport.seed, "subject_snapshot", return_value={}), \
                    patch.object(transport.seed, "git", return_value=b""), \
                    patch.object(transport, "capture_stream", side_effect=capture), \
                    successor.effort_override(transport):
                transport.run_claude(evidence, [None])
            self.assertEqual(len(seen), 1)
            self.assertEqual(successor.effort_receipt(evidence)["selected_environment"], successor.EFFORT_ENV)
            self.assertIs(transport.MODEL_ENV, previous)
            self.assertNotIn("CLAUDE_CODE_EFFORT_LEVEL", previous)
            command = successor.inputs.read(evidence / "command.json")
            command["model_environment"].pop("CLAUDE_CODE_EFFORT_LEVEL")
            (evidence / "command.json").write_text(json.dumps(command))
            with self.assertRaisesRegex(ValueError, "effort launch receipt"):
                successor.effort_receipt(evidence)

    def test_binding_and_measured_capture_restore_override_on_failure(self):
        adapter = successor.Adapter()
        transport = adapter.prior.matrix.driver.capture
        previous = transport.MODEL_ENV
        for binding in (True, False):
            with self.subTest(binding=binding), tempfile.TemporaryDirectory() as root:
                evidence = Path(root)
                successor.inputs.write_new(evidence / "launch.json", {
                    "claude_effort_environment": successor.EFFORT_ENV,
                    "models": {"claude_subagent_effort": "high"}})
                job = argparse.Namespace(provider="claude", case="R6M", evidence=evidence, binding=binding)
                def fail(*unused):
                    self.assertEqual(transport.MODEL_ENV["CLAUDE_CODE_EFFORT_LEVEL"], "high")
                    raise RuntimeError("capture failed")
                with patch.object(adapter.prior, "capture", side_effect=fail):
                    with self.assertRaisesRegex(RuntimeError, "capture failed"):
                        adapter.capture(job, [None])
                self.assertIs(transport.MODEL_ENV, previous)
                (evidence / "command.json").write_text("{}")
                with patch.object(adapter.prior, "capture") as capture:
                    with self.assertRaises(FileExistsError):
                        adapter.capture(job, [None])
                    capture.assert_not_called()
                self.assertIs(transport.MODEL_ENV, previous)

    def test_codex_transport_has_no_effort_override(self):
        adapter = successor.Adapter()
        transport = adapter.prior.matrix.driver.capture
        previous = transport.MODEL_ENV
        with tempfile.TemporaryDirectory() as root:
            job = argparse.Namespace(provider="codex", case="R5", evidence=Path(root))
            with patch.object(adapter.prior, "capture") as capture:
                adapter.capture(job, [None])
                capture.assert_called_once_with(job, [None])
                self.assertIs(transport.MODEL_ENV, previous)

    def test_offline_preparation_binds_both_sides_and_modes(self):
        with self.adapter() as (adapter, root):
            with patch.object(adapter.prior, "capture") as capture:
                for side in ("baseline", "candidate"):
                    for binding in (True, False):
                        name = f"{side}-{binding}"
                        job = argparse.Namespace(provider="claude", case="R6M", side=side,
                            mode="standard" if binding else "isolated", repetition=0 if binding else 1,
                            workspace=root / ("actor-" + name), evidence=root / name,
                            snapshot=adapter.controller.SNAPSHOTS[side], frozen=successor.FROZEN, binding=binding)
                        adapter.prepare(job)
                        launch = successor.inputs.read(job.evidence / "launch.json")
                        self.assertEqual(launch["claude_effort_environment"], successor.EFFORT_ENV)
                        self.assertEqual(launch["fixture_manifest_sha256"], successor.inputs.sha(successor.FROZEN))
                        prepared = successor.inputs.read(job.evidence / "prepared.json")
                        self.assertEqual(prepared["launch_sha256"], successor.inputs.sha(job.evidence / "launch.json"))
                        self.assertNotIn("pal", successor.inputs.read(job.workspace / ".runner/mcp-no-pal.json")["mcpServers"])
                        adapter.controller.validate_launch(job.evidence, successor.FROZEN)
                        with self.assertRaises(FileExistsError):
                            adapter.prepare(job)
                capture.assert_not_called()

    def test_retain_only_declared_runtime_files_and_refuse_secret(self):
        for secret_present in (False, True):
            with self.subTest(secret_present=secret_present), self.adapter() as (adapter, root):
                for side in ("baseline", "candidate"):
                    name = "binding-claude-" + side
                    workspace = successor.WORKSPACES / name
                    workspace.mkdir(parents=True)
                    config = workspace / ".capy.toml"
                    config.write_text("test-only-secret" if secret_present else "[storage]\n")
                    (workspace / "knowledge.db").write_text("must not retain")
                    evidence = root / name
                    evidence.mkdir()
                    successor.inputs.write_new(evidence / "launch.json", {"workspace": str(workspace)})
                    successor.inputs.write_new(evidence / "prepared.json", {
                        "runtime_files": {}, "capy_config_sha256": successor.inputs.sha(config)})
                with patch.object(adapter, "check_binding"), \
                        patch.object(adapter.prior.matrix.codex, "secrets", return_value=["test-only-secret"]):
                    if secret_present:
                        with self.assertRaisesRegex(ValueError, "credential"):
                            adapter.retain()
                        self.assertFalse((root / "runtime-inputs.json").exists())
                    else:
                        adapter.retain()
                        retained = successor.inputs.read(root / "runtime-inputs.json")
                        self.assertEqual(len(retained), 2)
                        self.assertTrue(all(name.endswith("/.capy.toml") for name in retained))
                        with self.assertRaises(FileExistsError):
                            adapter.retain()

    def test_absent_or_blocked_attestation_never_launches_measurement(self):
        with self.adapter() as (adapter, root):
            with patch.object(adapter, "capture") as capture:
                with self.assertRaises(FileNotFoundError):
                    adapter.run(adapter.jobs())
                successor.inputs.write_new(root / "preflight.json", {"status": "BLOCKED"})
                with self.assertRaisesRegex(ValueError, "preflight does not match"):
                    adapter.run(adapter.jobs())
                capture.assert_not_called()

    def test_preflight_rejects_missing_or_changed_retained_configuration(self):
        with self.adapter() as (adapter, root):
            prior = successor.inputs.read(successor.PRIOR / "preflight.json")
            proof = {
                "status": "PASS", "execution_freeze_sha256": successor.inputs.sha(successor.FROZEN),
                "calibration_results_sha256": successor.inputs.sha(successor.PRIOR / "calibration-results.json"),
                "binding_manifests": {k: v for k, v in prior["binding_manifests"].items() if "codex" in k},
                "inherited_state": prior["state"], "audit_files": {},
            }
            (root / "review.md").write_text("Synthetic guard-test approval; not actor evidence.\n")
            proof["independent_review"] = {"status": "PASS", "path": "review.md", "sha256": successor.inputs.sha(root / "review.md")}
            retained = {}
            for side in ("baseline", "candidate"):
                name = "binding-claude-" + side
                directory = root / name
                directory.mkdir()
                successor.inputs.write_new(directory / "manifest.json", {})
                proof["binding_manifests"][name] = successor.inputs.sha(directory / "manifest.json")
                target = root / "runtime-inputs" / name / ".capy.toml"
                target.parent.mkdir(parents=True)
                target.write_text("[storage]\n")
                digest = successor.inputs.sha(target)
                retained[target.relative_to(root).as_posix()] = digest
                successor.inputs.write_new(directory / "prepared.json", {"runtime_files": {}, "capy_config_sha256": digest})
                audit = root / "audits" / (name + ".json")
                audit.parent.mkdir(exist_ok=True)
                audit.write_text("{}")
                proof["audit_files"][audit.relative_to(root).as_posix()] = successor.inputs.sha(audit)
            successor.inputs.write_new(root / "runtime-inputs.json", retained)
            proof["runtime_inputs_sha256"] = successor.inputs.sha(root / "runtime-inputs.json")
            successor.inputs.write_new(root / "preflight.json", proof)
            with patch.object(adapter, "check_binding"):
                adapter.preflight()
                target.write_text("changed")
                with self.assertRaisesRegex(ValueError, "Changed or unsafe"):
                    adapter.preflight()
                target.unlink()
                with self.assertRaises(FileNotFoundError):
                    adapter.preflight()


if __name__ == "__main__":
    unittest.main()
