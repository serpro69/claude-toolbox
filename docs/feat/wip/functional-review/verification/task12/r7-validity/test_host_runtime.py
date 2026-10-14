"""Run inherited capture regressions through the explicit host correction."""
import os
import signal
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import runner
import host_runtime
import test_runtime as historical_tests


class HostRuntimeTests(historical_tests.RuntimeTests):
    def setUp(self):
        super().setUp()
        self.addCleanup(patch.stopall)
        patch.object(runner.prior.matrix.runtime, "_signal_group", host_runtime.signal_group).start()

    def test_cancel_kills_descendant_that_closed_stdout_and_ignored_term(self):
        # The inherited assertion reads Linux /proc; use a real ps observation
        # here so macOS cannot pass merely because /proc does not exist.
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
        children = []
        def consume(sequence, line, stream):
            children.append(int(line))
            os.kill(os.getpid(), signal.SIGTERM)
        with runner.prior.matrix.runtime.capture_signals() as interruption:
            result = self.stream(source, consume, interruption)
        self.assertEqual(result["interrupted_by"], signal.SIGTERM)
        state = subprocess.run(["/bin/ps", "-p", str(children[0]), "-o", "stat="],
                               capture_output=True, text=True, timeout=5)
        self.assertIn(state.returncode, (0, 1))
        self.assertTrue(not state.stdout.strip() or state.stdout.strip().startswith("Z"))


class PermissionTests(unittest.TestCase):
    def check_group(self, listing, exited=True, platform="darwin", returncode=None):
        process = SimpleNamespace(pid=12345, returncode=returncode)
        with patch.object(host_runtime.os, "killpg", side_effect=PermissionError("denied")), \
             patch.object(host_runtime.os, "waitid", return_value=object() if exited else None), \
             patch.object(host_runtime.sys, "platform", platform), \
             patch.object(host_runtime.subprocess, "run",
                          return_value=SimpleNamespace(stdout=listing)):
            host_runtime.signal_group(process, signal.SIGKILL)

    def test_dead_group_is_tolerated_only_before_leader_reap(self):
        self.check_group("12345 12345 Z\n12346 12345 Z+\n")
        with self.assertRaises(PermissionError):
            self.check_group("12345 12345 Z\n", returncode=0)

    def test_live_child_or_member_is_not_suppressed(self):
        with self.assertRaises(PermissionError):
            self.check_group("12345 12345 Z\n12346 12345 S\n")
        with self.assertRaises(PermissionError):
            self.check_group("12345 12345 S\n", exited=False)

    def test_missing_leader_or_other_platform_is_not_suppressed(self):
        with self.assertRaises(PermissionError):
            self.check_group("12346 12345 Z\n")
        with self.assertRaises(PermissionError):
            self.check_group("12345 12345 Z\n", platform="linux")

    def test_malformed_group_observation_fails_loudly(self):
        with self.assertRaises(ValueError):
            self.check_group("invalid observation\n")


if __name__ == "__main__":
    unittest.main()
