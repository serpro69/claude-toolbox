"""Offline regressions for the three Task 12 runner review findings."""
import io
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import runtime
import capture
import probe_pal


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def job(self, name):
        return SimpleNamespace(evidence=self.root / name)

    def completed(self, job, code=0):
        job.evidence.mkdir()
        (job.evidence / "completion.json").write_text(json.dumps({"exit_code": code}))
        (job.evidence / "manifest.json").write_text("{}")

    def test_preparation_failure_starts_no_capture(self):
        launched = []
        def prepare(job):
            if job.evidence.name == "second":
                raise FileExistsError("existing workspace")
        with self.assertRaises(FileExistsError):
            runtime.run_batch([self.job("first"), self.job("second")], prepare,
                              lambda job, interruption: launched.append(job))
        self.assertEqual(launched, [])

    def test_runtime_failure_stops_batch_after_sealed_completion(self):
        prepared, launched = [], []
        def run(job, interruption):
            self.assertEqual(prepared, ["first", "second"])
            launched.append(job.evidence.name)
            self.completed(job, 7)
        code = runtime.run_batch([self.job("first"), self.job("second")],
                                 lambda job: prepared.append(job.evidence.name), run)
        self.assertEqual(code, 7)
        self.assertEqual(launched, ["first"])

    def test_behavioral_failure_with_exit_zero_is_capture_success(self):
        def run(job, interruption):
            self.completed(job)
            (job.evidence / "report.md").write_text("Behavioral assertion: FAIL")
        self.assertEqual(runtime.run_batch([self.job("run")], lambda job: None, run), 0)

    def test_missing_completion_is_not_success(self):
        evidence = self.root / "run"
        evidence.mkdir()
        (evidence / "manifest.json").write_text("{}")
        with self.assertRaises(FileNotFoundError):
            runtime.completion_status(evidence)

    def stream(self, source, consume, interruption, **kwargs):
        return runtime.capture_stream([sys.executable, "-u", "-c", source], self.root,
            os.environ.copy(), io.StringIO(), subprocess.DEVNULL, consume,
            interruption, terminate_grace=0.15, **kwargs)

    def test_success_and_nonzero_runtime_status(self):
        for code in (0, 9):
            with self.subTest(code=code), runtime.capture_signals() as interruption:
                seen = []
                result = self.stream(f"print('one'); raise SystemExit({code})",
                    lambda seq, line, stream: seen.append((seq, line)), interruption)
                self.assertEqual(seen, [(1, b"one")])
                self.assertEqual(result["exit_code"], code)
                self.assertFalse(result["timed_out"])

    def test_interrupt_kills_reaps_and_allows_sealing(self):
        source = "import os,signal\nsignal.signal(signal.SIGTERM,signal.SIG_IGN)\nprint(os.getpid(),flush=True)\nwhile True: signal.pause()"
        for number in (signal.SIGTERM, signal.SIGINT):
            with self.subTest(number=number), runtime.capture_signals() as interruption:
                pid = []
                def consume(seq, line, stream):
                    pid.append(int(line))
                    os.kill(os.getpid(), number)
                    os.kill(os.getpid(), number)
                result = self.stream(source, consume, interruption)
                self.assertEqual(result["interrupted_by"], number)
                self.assertNotEqual(result["exit_code"], 0)
                with self.assertRaises(ProcessLookupError):
                    os.kill(pid[0], 0)
                # A further signal during finalization is recorded, not raised.
                os.kill(os.getpid(), number)
                sealed = self.root / f"sealed-{number}"
                sealed.write_text("sealed after child reaped")
                self.assertTrue(sealed.exists())

    def test_consumer_failure_reaps_child(self):
        pid = []
        def consume(seq, line, stream):
            pid.append(int(line))
            raise ValueError("invalid event")
        with runtime.capture_signals() as interruption:
            with self.assertRaisesRegex(ValueError, "invalid event"):
                self.stream("import os,signal\nprint(os.getpid(),flush=True)\nsignal.pause()", consume, interruption)
        with self.assertRaises(ProcessLookupError):
            os.kill(pid[0], 0)

    def test_timeout_is_explicit_and_reaps(self):
        with runtime.capture_signals() as interruption:
            result = self.stream("import signal\nsignal.pause()", lambda *args: None,
                                 interruption, timeout=0.1)
        self.assertTrue(result["timed_out"])
        self.assertNotEqual(result["exit_code"], 0)

    def test_stdout_eof_does_not_shorten_execution_deadline(self):
        with runtime.capture_signals() as interruption:
            result = self.stream("import os,time\nos.close(1)\ntime.sleep(0.3)",
                                 lambda *args: None, interruption, timeout=2)
        self.assertEqual(result["exit_code"], 0)
        self.assertFalse(result["timed_out"])

    def test_cancel_kills_descendant_that_closed_stdout_and_ignored_term(self):
        source = """import os,signal
r,w=os.pipe()
child=os.fork()
if child == 0:
    os.close(r)
    os.close(1)
    signal.signal(signal.SIGTERM,signal.SIG_IGN)
    os.write(w,b'ready')
    os.close(w)
    while True: signal.pause()
os.close(w)
os.read(r,5)
os.close(r)
print(child,flush=True)
while True: signal.pause()
"""
        child = []
        def consume(seq, line, stream):
            child.append(int(line))
            os.kill(os.getpid(), signal.SIGTERM)
        with runtime.capture_signals() as interruption:
            result = self.stream(source, consume, interruption)
        self.assertEqual(result["interrupted_by"], signal.SIGTERM)
        # The grandchild is reparented; its reaping is owned by init. It must
        # already be dead, even if init has not yet collected its zombie.
        deadline = time.monotonic() + 2
        while True:
            try:
                state = Path(f"/proc/{child[0]}/stat").read_text().split()[2]
            except FileNotFoundError:
                break
            if state == "Z":
                break
            self.assertLess(time.monotonic(), deadline, "descendant survived capture")
            time.sleep(0.01)

    def test_command_policy_matches_historical_capture(self):
        previous = Path(__file__).resolve().parents[1] / "runs/claude-candidate-R1-standard-1/command.json"
        command = json.loads(previous.read_text())["argv"]
        self.assertEqual(capture.command_for(command[-1]), command)

    def test_probe_broken_pipe_keeps_primary_error_and_seals(self):
        evidence = self.root / "probe"
        made = []
        def factory(workspace, target):
            client = object.__new__(probe_pal.Pal)
            client.events = [{"attempt": "initialize"}]
            client.error_log = (target / "stderr.txt").open("w")
            client.error_log.write("synthetic-secret")
            client.process = subprocess.Popen([sys.executable, "-c", "pass"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=client.error_log)
            client.process.wait()
            # Buffered write succeeds; close flushes into the dead process.
            client.process.stdin.write(b"request")
            def initialize():
                raise RuntimeError("original startup failure")
            client.initialize = initialize
            made.append(client)
            return client
        original_seal = probe_pal.controller.seed.seal
        with patch.object(probe_pal.controller.seed, "seal",
                          side_effect=lambda path: original_seal(path, ["synthetic-secret"])):
            with self.assertRaisesRegex(RuntimeError, "original startup failure") as caught:
                probe_pal.probe(self.root, evidence, factory)
        self.assertIn("BrokenPipeError", " ".join(caught.exception.__notes__))
        self.assertTrue((evidence / "manifest.json").exists())
        self.assertEqual(json.loads((evidence / "events.json").read_text()), made[0].events)
        self.assertNotIn("synthetic-secret", (evidence / "stderr.txt").read_text())
        self.assertTrue(made[0].error_log.closed)
        self.assertTrue(made[0].process.stdout.closed)

    def test_finalization_failure_does_not_skip_seal_or_replace_primary(self):
        calls = []
        primary = RuntimeError("startup")
        client = SimpleNamespace(events=[], close=lambda: (_ for _ in ()).throw(BrokenPipeError()))
        def write(*args):
            calls.append("write")
            raise OSError("disk full")
        runtime.finalize_probe(client, self.root, write, lambda path: calls.append("seal"), primary)
        self.assertEqual(calls, ["write", "seal"])
        self.assertEqual(len(primary.__notes__), 2)

    def test_probe_interruption_wakes_response_read_and_skips_listing(self):
        evidence = self.root / "cancelled-probe"
        made = []
        def factory(workspace, target):
            client = object.__new__(probe_pal.Pal)
            client.events, client.buffer, client.sequence = [], b"", 0
            client.error_log = (target / "stderr.txt").open("w")
            source = "import os,signal,sys\nsys.stdin.readline()\nos.kill(int(sys.argv[1]),signal.SIGINT)\nwhile True: signal.pause()"
            client.process = subprocess.Popen([sys.executable, "-c", source, str(os.getpid())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=client.error_log)
            made.append(client)
            return client
        original_seal = probe_pal.controller.seed.seal
        with patch.object(probe_pal.controller.seed, "seal",
                          side_effect=lambda path: original_seal(path, [])):
            with self.assertRaisesRegex(RuntimeError, "closed stdout"):
                probe_pal.probe(self.root, evidence, factory)
        self.assertEqual([e["request"]["method"] for e in made[0].events], ["initialize"])
        self.assertIsNotNone(made[0].process.returncode)
        self.assertTrue((evidence / "manifest.json").exists())

    def test_transport_nonzero_is_sealed_and_redacted_before_status(self):
        workspace = self.root / "workspace"
        from probe_state import workspace_at
        workspace_at(workspace)
        evidence = self.root / "capture"
        evidence.mkdir()
        (evidence / "launch.json").write_text(json.dumps({"workspace": str(workspace), "prompt": "ordinary"}))
        home = self.root / "fake-home"
        (home / ".codex").mkdir(parents=True)
        (home / ".codex/config.toml").write_text('[mcp_servers.pal.env]\nAPI_KEY="synthetic-secret"\n')
        command = [sys.executable, "-c", 'import json; print(json.dumps({"type":"result","result":"synthetic-secret"})); raise SystemExit(9)']
        with patch.object(capture.Path, "home", return_value=home), patch.object(capture, "command_for", return_value=command):
            status = capture.run_claude(evidence)
        self.assertEqual(status, 9)
        self.assertEqual(runtime.completion_status(evidence), 9)
        self.assertEqual((evidence / "report.md").read_text(), "[credential redacted]\n")
        seal = json.loads((evidence / "manifest.json").read_text())
        self.assertIn("completion.json", seal)
        self.assertIn("events.jsonl", seal)

    def test_packet_snapshot_retains_bytes_without_claiming_receipt(self):
        with tempfile.TemporaryDirectory(prefix="kk-review-instructions-", dir="/tmp") as directory:
            path = Path(directory) / "part-01.md"
            path.write_text("original instructions\n")
            capture.snapshot_instruction_packet({"file_path": str(path)}, self.root, 7)
        event = json.loads((self.root / "payload-events.jsonl").read_text())
        record = event["files"][0]
        self.assertEqual(event["event_sequence"], 7)
        self.assertEqual((self.root / record["artifact"]).read_text(), "original instructions\n")
        self.assertIn("unverified", record["receipt"])

    def test_oversized_packet_is_rejected_without_retained_payload(self):
        with tempfile.TemporaryDirectory(prefix="kk-review-instructions-", dir="/tmp") as directory:
            path = Path(directory) / "part-01.md"
            path.write_bytes(b"x" * 13001)
            with self.assertRaisesRegex(ValueError, "part bound"):
                capture.snapshot_instruction_packet({"file_path": str(path)}, self.root, 7)
        self.assertFalse((self.root / "payloads").exists())


if __name__ == "__main__":
    unittest.main()
