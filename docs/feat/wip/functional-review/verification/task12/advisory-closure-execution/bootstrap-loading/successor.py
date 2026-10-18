"""Binding-only prompt correction with inherited launch and strict receipt gates."""
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent
HOST = PRIOR / "high-effort-host"
sys.path.insert(0, str(PRIOR))
import inputs
import runner

HOST_SOURCE_SHA = "df57e3f989303a277ab17b9952cfe9ae90e7d58def704a13fa76fd24b3a3c630"
HOST_FREEZE_SHA = "be7d605b7aabe88855051362a3f92bc99a0cf56a6fe22b0805adfc1763830764"
GUARD_FREEZE_SHA = "f7d0a820204eaa899a2b9ed6840325cf93190fa07aeb4a072aee56fb0ba96fb1"
if inputs.sha(HOST / "successor.py") != HOST_SOURCE_SHA:
    raise ValueError("Frozen host launcher changed")
# Load a separate module object: its configuration belongs only to this successor.
# Historical files, modules used by other processes, and seals stay unchanged.
spec = importlib.util.spec_from_file_location("bootstrap_host", HOST / "successor.py")
host = importlib.util.module_from_spec(spec)
spec.loader.exec_module(host)
host.HERE = HERE
host.FROZEN = HERE / "execution-freeze.json"
host.WORKSPACES = Path("/tmp/fr-advisory-bootstrap-20261018")
host.DEPENDENCIES = ("successor.py", "test_successor.py", "run-contract.md", "binding-prompt.txt")


def binding_prompt():
    return (host.HERE / "binding-prompt.txt").read_text().rstrip("\n")


class Adapter(host.Adapter):
    def inherited_evidence(self):
        records = super().inherited_evidence()
        if records != inputs.read(HOST / "execution-freeze.json")["inherited_evidence"]:
            raise ValueError("Reviewed historical evidence changed")
        for filename, digest in (("execution-freeze.json", HOST_FREEZE_SHA),
                                 ("guard-freeze.json", GUARD_FREEZE_SHA)):
            if inputs.sha(HOST / filename) != digest:
                raise ValueError("Host/guard predecessor identity changed")
            record = inputs.read(HOST / filename)
            runner.checked_files(HOST, record["dependencies"])
            for name in (filename, *record["dependencies"]):
                records["high-effort-host/" + name] = inputs.sha(HOST / name)
        return records

    def prepare(self, job):
        super().prepare(job)
        if job.provider == "claude" and job.binding:
            launch_path = job.evidence / "launch.json"
            launch = inputs.read(launch_path)
            launch["prompt"] = binding_prompt()
            (job.evidence / "prompt.txt").write_text(launch["prompt"] + "\n")
            self.seed.write_json(launch_path, launch)
            prepared = inputs.read(job.evidence / "prepared.json")
            prepared["launch_sha256"] = inputs.sha(launch_path)
            prepared["prompt_sha256"] = inputs.sha(job.evidence / "prompt.txt")
            self.seed.write_json(job.evidence / "prepared.json", prepared)

    def check_prompt(self, directory):
        launch = inputs.read(directory / "launch.json")
        if (launch["prompt"] != binding_prompt()
                or (directory / "prompt.txt").read_text() != binding_prompt() + "\n"):
            raise ValueError("Binding prompt differs from successor declaration")

    def capture(self, job, interruption):
        if job.provider == "claude" and job.binding:
            self.verify()
            self.check_prompt(job.evidence)
        return super().capture(job, interruption)

    def check_binding(self, directory, provider, side, frozen):
        super().check_binding(directory, provider, side, frozen)
        if provider == "claude":
            self.check_prompt(directory)

    def verify_receipt(self, side):
        source = host.HERE / ("binding-claude-" + side)
        self.check_binding(source, "claude", side, host.FROZEN)
        detail = host.preflight_audit.claude(
            source, self.root / side / "retained/klaude-plugin", side)
        expected = {"manifest_sha256": inputs.sha(source / "manifest.json"),
                    "effort": host.effort_receipt(source), **detail}
        actual = inputs.read(host.HERE / "audits" / (source.name + ".json"))
        if json.dumps(actual, sort_keys=True) != json.dumps(expected, sort_keys=True):
            raise ValueError("Receipt audit differs from successful sealed evidence: " + side)

    def preflight(self):
        self.verify()
        for side in ("baseline", "candidate"):
            self.verify_receipt(side)
        # Preserve the reviewed guard correction before all original prerequisites.
        return super().preflight()


def main():
    previous = host.Adapter
    try:
        host.Adapter = Adapter
        return host.main()
    finally:
        host.Adapter = previous


if __name__ == "__main__":
    raise SystemExit(main())
