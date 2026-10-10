"""Successor probe finalization; live use remains deferred by the user."""
import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
import controller
from runtime import capture_signals, finalize_probe

spec = importlib.util.spec_from_file_location("historical_pal_probe", Path(__file__).resolve().parents[1] / "probe_pal.py")
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)


class Pal(previous.Pal):
    def close(self):
        # A buffered stdin close may fail after the server exits. It must not
        # bypass waiting, termination, or closure of the owned output streams.
        try:
            self.process.stdin.close()
        finally:
            try:
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.terminate()
                    try:
                        self.process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        self.process.kill()
                        self.process.wait()
            finally:
                try:
                    self.process.stdout.close()
                finally:
                    self.error_log.close()


def probe(workspace, evidence, factory=Pal):
    evidence.mkdir(parents=True, exist_ok=False)
    client = None
    primary = None
    def stop_owned_server():
        # EOF wakes the inherited bounded response read. Popen.kill handles an
        # already-exited child; the constructor has its own acquisition guard.
        if client is not None:
            client.process.kill()

    with capture_signals(stop_owned_server) as interruption:
        try:
            if interruption[0]:
                raise InterruptedError("Probe interrupted before acquisition")
            client = factory(workspace, evidence)
            if interruption[0]:
                raise InterruptedError("Probe interrupted before initialization")
            client.initialize()
            if interruption[0]:
                raise InterruptedError("Probe interrupted during initialization")
            result = client.call("tools/list", {})
            if interruption[0]:
                raise InterruptedError("Probe interrupted during tool listing")
            controller.seed.write_json(evidence / "result.json", {
                "status": "connected", "tools": [item["name"] for item in result["tools"]]})
        except BaseException as exc:
            primary = exc
            controller.seed.write_json(evidence / "result.json", {
                "status": "failed", "error": type(exc).__name__, "message": str(exc)})
            raise
        finally:
            if client is None:
                controller.seed.seal(evidence)
            else:
                finalize_probe(client, evidence, controller.seed.write_json,
                               controller.seed.seal, primary)
        return 128 + interruption[0] if interruption[0] else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    raise SystemExit(probe(args.workspace, args.evidence))
