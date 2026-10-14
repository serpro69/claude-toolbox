"""Darwin-only handling of an unsignalable, entirely dead owned process group."""
import os
import subprocess
import sys


def signal_group(process, number):
    try:
        os.killpg(process.pid, number)
    except ProcessLookupError:
        pass
    except PermissionError:
        # Darwin can return EPERM for an unreaped zombie-only group. Never
        # reinterpret EPERM for a live child or live/unknown group membership.
        if sys.platform != "darwin" or process.returncode is not None:
            raise
        exited = os.waitid(os.P_PID, process.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT)
        if exited is None:
            raise
        result = subprocess.run(
            ["/bin/ps", "-ax", "-o", "pid=,pgid=,stat="],
            check=True, capture_output=True, text=True, timeout=5)
        members = {}
        for line in result.stdout.splitlines():
            pid, pgid, state = line.split()
            if int(pgid) == process.pid:
                members[int(pid)] = state
        if process.pid not in members or any(not state.startswith("Z") for state in members.values()):
            raise
        # Every retained member is dead and cannot fork. The caller still owns
        # and reaps the leader; no signal is sent after releasing its identity.
