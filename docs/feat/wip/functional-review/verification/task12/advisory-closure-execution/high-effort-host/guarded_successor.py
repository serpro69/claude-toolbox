"""Verification-only successor: reject incomplete receipt evidence before readiness."""
from pathlib import Path
import json
import sys

import successor

HERE = Path(__file__).resolve().parent
GUARD_FREEZE = HERE / "guard-freeze.json"
EXECUTION_SHA = "be7d605b7aabe88855051362a3f92bc99a0cf56a6fe22b0805adfc1763830764"
GUARD_FILES = ("guarded_successor.py", "test_guarded_successor.py", "guard-contract.md")


def freeze_guard():
    successor.Adapter().verify()
    if successor.inputs.sha(successor.FROZEN) != EXECUTION_SHA:
        raise ValueError("Unexpected capture execution freeze")
    successor.inputs.write_new(GUARD_FREEZE, {
        "execution_freeze_sha256": EXECUTION_SHA,
        "dependencies": {name: successor.inputs.sha(HERE / name) for name in GUARD_FILES},
        "scope": "verification only; original actor/runtime/capture/calibration identities unchanged",
    })
    verify_guard()


def verify_guard():
    data = successor.inputs.read(GUARD_FREEZE)
    if (data["execution_freeze_sha256"] != EXECUTION_SHA
            or successor.inputs.sha(successor.FROZEN) != EXECUTION_SHA
            or set(data["dependencies"]) != set(GUARD_FILES)):
        raise ValueError("Receipt guard identity differs")
    successor.runner.checked_files(HERE, data["dependencies"])


def verify_receipt(adapter, side):
    source = successor.HERE / ("binding-claude-" + side)
    adapter.check_binding(source, "claude", side, successor.FROZEN)
    detail = successor.preflight_audit.claude(
        source, adapter.root / side / "retained/klaude-plugin", side)
    expected = {
        "manifest_sha256": successor.inputs.sha(source / "manifest.json"),
        "effort": successor.effort_receipt(source),
        **detail,
    }
    actual = successor.inputs.read(successor.HERE / "audits" / (source.name + ".json"))
    # The pinned auditor returns service tuples; their retained JSON uses arrays.
    if json.dumps(actual, sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError("Receipt audit differs from successful sealed evidence: " + side)


class Adapter(successor.Adapter):
    def preflight(self):
        verify_guard()
        self.verify()
        for side in ("baseline", "candidate"):
            verify_receipt(self, side)
        # Review approval, state, calibration, all four bindings and retained files
        # remain independently required; successful receipt checks cannot replace them.
        return super().preflight()


def main():
    if sys.argv[1:] == ["freeze-guard"]:
        freeze_guard()
        return 0
    verify_guard()
    previous = successor.Adapter
    try:
        successor.Adapter = Adapter
        return successor.main()
    finally:
        successor.Adapter = previous


if __name__ == "__main__":
    raise SystemExit(main())
