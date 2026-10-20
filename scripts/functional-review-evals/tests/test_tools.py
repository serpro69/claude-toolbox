"""Offline extraction checks, runnable outside the repository."""
import io
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bundles
import grading
import inventory
import receipts
import runtime


class ToolsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def request(self, provider="claude"):
        source, fixture = self.root / "capture", self.root / "fixture"
        source.mkdir()
        fixture.mkdir()
        (source / "report.md").write_text("Observed failure; retain this attempt.\n")
        if provider == "claude":
            rows = [{"sequence": 7, "event": {"type": "user", "parent_tool_use_id": "child-1",
                "message": {"content": [{"type": "tool_result", "tool_use_id": "read-1", "content": "returned bytes"}]}}}]
            (source / "events.jsonl").write_text("\n".join(map(json.dumps, rows)))
        else:
            rows = [{"item": {"type": "reasoning", "text": "PRIVATE"}},
                {"startedAtMs": 1, "completedAtMs": 2, "item": {"type": "commandExecution", "id": "read-1",
                    "exitCode": 1, "aggregatedOutput": "permission denied", "encrypted_content": "PRIVATE"}}]
            (source / "items-main.json").write_text(json.dumps(rows))
        grading.write_json(source / "manifest.json", {p.name: grading.digest(p) for p in source.iterdir()})
        grading.write_json(fixture / "eval.json", {"assertions": [{"id": "1.1", "text": "Read the input"}]})
        (fixture / "oracle").mkdir()
        (fixture / "oracle/expected.json").write_text('{"1.1": "FAIL"}')
        request = {"capture": str(source), "capture_manifest_sha256": grading.digest(source / "manifest.json"),
            "fixture": str(fixture), "fixture_manifest": {p.relative_to(fixture).as_posix(): grading.digest(p)
                for p in fixture.rglob("*") if p.is_file()}, "provider": provider,
            "run": {"run": "synthetic", "provider": provider},
            "identity": {"evidence_contract": "synthetic receipt/use", "runtime": "offline test"}}
        for role in ("grader", "rubric"):
            path = self.root / (role + ".md")
            path.write_text("Synthetic " + role)
            request[role] = {"path": str(path), "sha256": grading.digest(path)}
        path = self.root / "request.json"
        grading.write_json(path, request)
        return path, request

    def test_packaging_keeps_failure_and_sealed_oracle_only(self):
        path, request = self.request()
        (Path(request["fixture"]) / "oracle/unsealed.json").write_text("invented answer")
        destination = self.root / "graded"
        manifest = grading.prepare(path, destination)
        self.assertEqual((destination / "captured/report.md").read_text(), "Observed failure; retain this attempt.\n")
        self.assertFalse((destination / "oracle/unsealed.json").exists())
        self.assertTrue((destination / "oracle/expected.json").exists())
        event = json.loads((destination / "events.jsonl").read_text())
        self.assertEqual((event["id"], event["actor"], event["block"]["content"]),
                         ("e7.0", "child-of:child-1", "returned bytes"))
        for record in manifest["files"]:
            self.assertEqual(grading.digest(destination / record["path"]), record["sha256"])
        with self.assertRaises(FileExistsError):
            grading.prepare(path, destination)

    def test_tampered_capture_is_not_resealed(self):
        path, request = self.request()
        (Path(request["capture"]) / "report.md").write_text("changed")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            grading.prepare(path, self.root / "graded")
        self.assertFalse((self.root / "graded").exists())

    def test_tampered_rubric_is_rejected_before_output(self):
        path, request = self.request()
        Path(request["rubric"]["path"]).write_text("changed criteria")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            grading.prepare(path, self.root / "graded")
        self.assertFalse((self.root / "graded").exists())

    def test_codex_preserves_failure_timing_without_private_or_unsealed_items(self):
        path, request = self.request("codex")
        (Path(request["capture"]) / "items-extra.json").write_text("invented event")
        grading.prepare(path, self.root / "graded")
        content = (self.root / "graded/events.jsonl").read_text()
        event = json.loads(content)
        self.assertEqual((event["id"], event["completedAtMs"], event["item"]["exitCode"]), ("read-1", 2, 1))
        self.assertNotIn("PRIVATE", content)
        self.assertNotIn("invented", content)

    def test_paths_reject_links_traversal_and_missing_members(self):
        (self.root / "source").write_text("sealed")
        sha = grading.digest(self.root / "source")
        (self.root / "link").symlink_to("source")
        for relative in ("link", "../source", str(self.root / "source"), "missing", "."):
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                grading.checked_file(self.root, relative, sha)

    def test_bundle_build_preserves_bytes_and_excludes_evals(self):
        repo = self.root / "repo"
        repo.mkdir()
        environment = {"PATH": os.defpath, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}
        command = ["git", "-C", str(repo), "-c", "core.hooksPath=" + os.devnull,
                   "-c", "commit.gpgsign=false", "-c", "user.name=Test", "-c", "user.email=test@example.invalid"]
        subprocess.run([*command, "init", "-q"], env=environment, check=True)
        for tree in bundles.TREES:
            root = repo / tree
            root.mkdir(parents=True)
            (root / "instruction.md").write_bytes(b"original\n")
        (repo / "klaude-plugin/shared.md").symlink_to("instruction.md")
        (repo / "klaude-plugin/evals").mkdir()
        (repo / "klaude-plugin/evals/answer.json").write_text("grader-only")
        subprocess.run([*command, "add", "."], env=environment, check=True)
        subprocess.run([*command, "commit", "-qm", "Input"], env=environment, check=True)
        destination = self.root / "bundle"
        identity = bundles.build(repo, "HEAD", destination)
        self.assertEqual(identity["excluded_files"], 1)
        self.assertFalse((destination / "retained/klaude-plugin/evals").exists())
        self.assertEqual((destination / "retained/klaude-plugin/shared.md").read_bytes(), b"original\n")
        with self.assertRaises(FileExistsError):
            bundles.build(repo, "HEAD", destination)

    def test_bundle_rejects_escaping_links_and_evaluator_material(self):
        root = self.root / "bundle"
        root.mkdir()
        (self.root / "answer").write_text("outside")
        (root / "link").symlink_to("../answer")
        with self.assertRaisesRegex(ValueError, "Escaping link"):
            bundles.manifest(root)
        (root / "link").unlink()
        (root / "eval.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "Evaluator material"):
            bundles.manifest(root)

    def test_history_collects_paginated_children_without_private_values(self):
        calls = []
        def call(method, params):
            calls.append((method, params))
            if method == "thread/read":
                return {"thread": {"id": params["threadId"]}}
            if params["threadId"] == "main" and "cursor" not in params:
                return {"data": [{"item": {"type": "collabAgentToolCall", "receiverThreadIds": ["child"]}}], "nextCursor": "page2"}
            return {"data": [{"item": {"type": "agentMessage", "text": 'token-"quoted', "encrypted_content": "PRIVATE"}}]}
        server = SimpleNamespace(received=[], call=call)
        evidence = self.root / "history"
        self.assertEqual(receipts.collect_history(server, "main", evidence, ['token-"quoted']), ["child", "main"])
        self.assertEqual(len(calls), 5)
        retained = (evidence / "items-main.json").read_text()
        self.assertNotIn("PRIVATE", retained)
        self.assertNotIn("quoted", retained)
        self.assertIn("[credential redacted]", retained)

    def test_history_refuses_repeated_cursor_and_path_escape(self):
        server = SimpleNamespace(received=[], call=lambda *args: {"data": [], "nextCursor": "same"})
        with self.assertRaisesRegex(ValueError, "Repeated"):
            receipts.collect_history(server, "main", self.root / "repeat")
        with self.assertRaisesRegex(ValueError, "Unsafe"):
            receipts.collect_history(server, "../escape", self.root / "unsafe")

    def test_history_survives_supplementary_metadata_failure(self):
        items = [{"item": {"type": "agentMessage", "id": "a", "text": "retained"}}]
        def call(method, params):
            if method == "thread/read":
                raise RuntimeError("metadata unavailable")
            return {"data": items}
        evidence = self.root / "partial"
        with self.assertRaisesRegex(RuntimeError, "metadata unavailable"):
            receipts.collect_history(SimpleNamespace(received=[], call=call), "main", evidence)
        self.assertEqual(json.loads((evidence / "items-main.json").read_text()), items)
        self.assertFalse((evidence / "thread-main.json").exists())

    def test_inventory_preserves_symlinks_and_detects_missing_extra_changed_members(self):
        evidence = self.root / "evidence"
        evidence.mkdir()
        (evidence / "file").write_text("original")
        (evidence / "link").symlink_to("file")
        (evidence / "__pycache__").mkdir()
        (evidence / "__pycache__/cache.pyc").write_bytes(b"cache")
        manifest = self.root / "inventory.json"
        saved = inventory.create(evidence, manifest, "evidence", "original-revision")
        self.assertEqual(saved["counts"], {"file": 1, "symlink": 1, "directory": 0})
        self.assertEqual(saved["exclusions"], ["__pycache__/"])
        inventory.verify(evidence, manifest)
        (evidence / "file").write_text("changed")
        with self.assertRaisesRegex(ValueError, "mismatch"):
            inventory.verify(evidence, manifest)
        (evidence / "file").write_text("original")
        (evidence / "extra").write_text("extra")
        with self.assertRaisesRegex(ValueError, "mismatch"):
            inventory.verify(evidence, manifest)
        (evidence / "extra").unlink()
        (evidence / "link").unlink()
        with self.assertRaisesRegex(ValueError, "mismatch"):
            inventory.verify(evidence, manifest)

    def test_preparation_and_runtime_failure_stop_serial_batch(self):
        jobs = [SimpleNamespace(evidence=self.root / name) for name in ("one", "two")]
        launched = []
        def prepare(job):
            if job is jobs[1]:
                raise ValueError("preparation failed")
        with self.assertRaisesRegex(ValueError, "preparation failed"):
            runtime.run_batch(jobs, prepare, lambda *args: launched.append(args))
        self.assertEqual(launched, [])
        def capture(job, interruption):
            launched.append(job)
            job.evidence.mkdir()
            grading.write_json(job.evidence / "manifest.json", {})
            grading.write_json(job.evidence / "completion.json", {"exit_code": 9})
        self.assertEqual(runtime.run_batch(jobs, lambda job: None, capture), 9)
        self.assertEqual(launched, jobs[:1])

    def test_interrupt_reaps_owned_process_and_preserves_signal(self):
        seen = []
        def consume(sequence, line, stream):
            seen.append(int(line))
            os.kill(os.getpid(), signal.SIGTERM)
        with runtime.capture_signals() as interruption:
            result = runtime.capture_stream([sys.executable, "-u", "-c",
                "import os,signal; print(os.getpid()); signal.pause()"], self.root, {},
                io.StringIO(), subprocess.DEVNULL, consume, interruption, timeout=3, terminate_grace=0.1)
        self.assertEqual(result["interrupted_by"], signal.SIGTERM)
        with self.assertRaises(ProcessLookupError):
            os.kill(seen[0], 0)

    def test_timeout_remains_failure(self):
        with runtime.capture_signals() as interruption:
            result = runtime.capture_stream([sys.executable, "-c", "import signal; signal.pause()"],
                self.root, {}, io.StringIO(), subprocess.DEVNULL,
                lambda *args: None, interruption, timeout=0.1, terminate_grace=0.1)
        self.assertTrue(result["timed_out"])
        self.assertNotEqual(result["exit_code"], 0)
        grading.write_json(self.root / "manifest.json", {})
        grading.write_json(self.root / "completion.json", result)
        self.assertEqual(runtime.completion_status(self.root), 124)

    def test_finalization_keeps_primary_error_and_attempts_sealing(self):
        primary = RuntimeError("startup")
        client = SimpleNamespace(events=[], close=lambda: (_ for _ in ()).throw(BrokenPipeError()))
        seen = []
        runtime.finalize_probe(client, self.root, lambda *args: seen.append("write"),
                               lambda path: seen.append("seal"), primary)
        self.assertEqual(seen, ["write", "seal"])
        self.assertIn("BrokenPipeError", primary.__notes__[0])


if __name__ == "__main__":
    unittest.main()
