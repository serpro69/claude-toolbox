"""Owned, serial capture boundaries; historical capture code stays immutable."""
import json
from contextlib import contextmanager
import os
from pathlib import Path
import select
import signal
import subprocess
import time


@contextmanager
def capture_signals(on_request=None):
    """Defer interruption until the capture owner has sealed its evidence."""
    request = [None]

    def request_stop(number, frame):
        if request[0] is None:
            request[0] = number
            if on_request is not None:
                on_request()

    previous = {s: signal.getsignal(s) for s in (signal.SIGINT, signal.SIGTERM)}
    try:
        for s in previous:
            signal.signal(s, request_stop)
        yield request
    finally:
        for s, handler in previous.items():
            signal.signal(s, handler)


def capture_stream(command, workspace, environment, events, errors, consume,
                   interruption, *, timeout=1800, terminate_grace=5):
    """Stream lines while owning the process group through interruption/timeout.

    Signal handlers only record requests. They never raise between acquisition
    and cleanup registration. The loop terminates and reaps the owned group.
    """
    process = None
    try:
        if interruption[0] is not None:
            return {"exit_code": 128 + interruption[0],
                    "interrupted_by": interruption[0], "timed_out": False}
        process = subprocess.Popen(command, cwd=workspace, env=environment,
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=errors,
            start_new_session=True)
        deadline = time.monotonic() + timeout
        stopping = None
        timed_out = False
        buffer = b""
        sequence = 0
        while True:
            now = time.monotonic()
            if stopping is None and (interruption[0] is not None or now >= deadline):
                timed_out = interruption[0] is None
                stopping = now
                _signal_group(process, signal.SIGTERM)
            if stopping is not None and now - stopping >= terminate_grace:
                _signal_group(process, signal.SIGKILL)
                # Even a descendant holding stdout cannot keep this reader alive.
                break
            if not select.select([process.stdout], [], [], 0.1)[0]:
                continue
            chunk = os.read(process.stdout.fileno(), 65536)
            if not chunk:
                if buffer:
                    sequence += 1
                    consume(sequence, buffer, events)
                break
            buffer += chunk
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                sequence += 1
                consume(sequence, line, events)
        # This successor capture is Linux-only, like its declared Task 12 host.
        # Observe exit without reaping so the leader's PID cannot be recycled
        # before cleanup of descendants that closed stdout or ignored SIGTERM.
        while stopping is None and interruption[0] is None:
            if os.waitid(os.P_PID, process.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT) is not None:
                break
            if time.monotonic() >= deadline:
                timed_out = True
                break
            time.sleep(0.01)
        _signal_group(process, signal.SIGKILL)
        status = process.wait()
        return {"exit_code": status, "interrupted_by": interruption[0],
                "timed_out": timed_out}
    finally:
        if process is not None:
            # Do not reap before group cleanup: retaining the child identity
            # prevents accidentally signalling a recycled process-group ID.
            if process.returncode is None:
                _signal_group(process, signal.SIGKILL)
                process.wait()
            process.stdout.close()


def _signal_group(process, number):
    try:
        os.killpg(process.pid, number)
    except ProcessLookupError:
        pass


def completion_status(evidence):
    """A sealed runtime failure is data, but must not become batch success."""
    evidence = Path(evidence)
    if not (evidence / "manifest.json").is_file():
        raise RuntimeError("Capture did not seal its evidence")
    result = json.loads((evidence / "completion.json").read_text())
    code = result.get("exit_code")
    if type(code) is not int:
        raise ValueError("Completion lacks an integer runtime exit code")
    if result.get("interrupted_by"):
        return 128 + result["interrupted_by"]
    if result.get("timed_out"):
        return 124
    return code if 0 <= code <= 255 else 1


def run_batch(jobs, prepare, capture):
    """No actor starts until every input is prepared; captures have one owner."""
    jobs = list(jobs)
    with capture_signals() as interruption:
        for job in jobs:
            prepare(job)
            if interruption[0]:
                return 128 + interruption[0]
        for job in jobs:
            capture(job, interruption)
            status = completion_status(job.evidence)
            if interruption[0] or status:
                return 128 + interruption[0] if interruption[0] else status
    return 0


def finalize_probe(client, evidence, write_json, seal, primary_error=None):
    """Retain the primary failure; close errors cannot skip evidence sealing."""
    failures = []
    for operation in (client.close,
                      lambda: write_json(evidence / "events.json", client.events),
                      lambda: seal(evidence)):
        try:
            operation()
        except BaseException as exc:
            failures.append(exc)
    if failures:
        primary = primary_error or failures[0]
        for failure in failures:
            if failure is not primary:
                primary.add_note("Probe finalization also failed: " + type(failure).__name__)
        if primary_error is None:
            raise primary
