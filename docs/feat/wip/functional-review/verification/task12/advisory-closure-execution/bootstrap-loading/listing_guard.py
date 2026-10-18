"""Separately frozen verifier for unchanged bootstrap captures and runtime."""
import json
import sys

import successor
import listing_audit

HERE = successor.HERE
FREEZE = HERE / "verifier-freeze.json"
EXECUTION_SHA = "4a0c926f6af7a70e5b12fc175e670b7d68715ccb0295d8a94b8ba2dd7ebecdec"
FILES = ("listing_guard.py", "listing_audit.py", "test_listing_audit.py", "listing-audit-contract.md")


def verify_verifier():
    data = successor.inputs.read(FREEZE)
    if (successor.inputs.sha(successor.host.FROZEN) != EXECUTION_SHA
            or data["execution_freeze_sha256"] != EXECUTION_SHA
            or set(data["dependencies"]) != set(FILES)):
        raise ValueError("Verifier/execution identity differs")
    successor.runner.checked_files(HERE, data["dependencies"])


def freeze_verifier():
    successor.Adapter().verify()
    if successor.inputs.sha(successor.host.FROZEN) != EXECUTION_SHA:
        raise ValueError("Unexpected capture execution identity")
    successor.inputs.write_new(FREEZE, {"execution_freeze_sha256": EXECUTION_SHA,
        "dependencies": {name: successor.inputs.sha(HERE / name) for name in FILES},
        "scope": "verification only; original actor/runtime/capture/calibration identities unchanged"})
    verify_verifier()


class Adapter(successor.Adapter):
    def receipt(self, side):
        verify_verifier()
        self.verify()
        source = HERE / ("binding-claude-" + side)
        self.check_binding(source, "claude", side, successor.host.FROZEN)
        detail = listing_audit.claude(source, self.root / side / "retained/klaude-plugin", side)
        return {"manifest_sha256": successor.inputs.sha(source / "manifest.json"),
                "effort": successor.host.effort_receipt(source), **detail}

    def verify_receipt(self, side):
        expected = self.receipt(side)
        actual = successor.inputs.read(HERE / "audits" / ("binding-claude-" + side + ".json"))
        if json.dumps(actual, sort_keys=True) != json.dumps(expected, sort_keys=True):
            raise ValueError("Receipt audit differs from successful sealed evidence: " + side)

    def audit(self):
        self.calibration_ready()
        (HERE / "audits").mkdir(exist_ok=True)
        for side in ("baseline", "candidate"):
            expected = self.receipt(side)
            path = HERE / "audits" / ("binding-claude-" + side + ".json")
            if path.exists():
                self.verify_receipt(side)
            else:
                successor.inputs.write_new(path, expected)

    def preflight(self):
        verify_verifier()
        proof = successor.inputs.read(HERE / "preflight.json")
        if proof.get("verifier_freeze_sha256") != successor.inputs.sha(FREEZE):
            raise ValueError("Preflight does not bind selected verifier")
        return super().preflight()


def main():
    if sys.argv[1:] == ["freeze-verifier"]:
        freeze_verifier()
        return 0
    verify_verifier()
    previous = successor.Adapter
    try:
        successor.Adapter = Adapter
        return successor.main()
    finally:
        successor.Adapter = previous


if __name__ == "__main__":
    raise SystemExit(main())
