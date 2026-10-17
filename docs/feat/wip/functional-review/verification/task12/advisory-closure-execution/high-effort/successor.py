"""Claude effort correction; preserve the original adapter and all sealed evidence."""
import argparse
from contextlib import contextmanager
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent
sys.path.insert(0, str(PRIOR))
import inputs
import runner
import preflight_audit

FROZEN = HERE / "execution-freeze.json"
WORKSPACES = Path("/tmp/fr-advisory-high-effort-20261017")
EFFORT_ENV = {"CLAUDE_CODE_EFFORT_LEVEL": "high"}
PREDECESSOR_SHA = "edc9cc7798bc3b2f7759a0c707db26abe2ead848bf51b6ec9de8535497a5dd85"
DEPENDENCIES = ("successor.py", "test_successor.py", "run-contract.md")


@contextmanager
def effort_override(transport):
    """The inherited launcher uses this same mapping for Popen and command.json."""
    previous = transport.MODEL_ENV
    transport.MODEL_ENV = {**previous, **EFFORT_ENV}
    try:
        yield
    finally:
        transport.MODEL_ENV = previous


def effort_receipt(directory):
    command = inputs.read(directory / "command.json")
    argv = command["argv"]
    if (command["model_environment"].get("CLAUDE_CODE_EFFORT_LEVEL") != "high"
            or argv[argv.index("--effort") + 1] != "high"):
        raise ValueError("Claude effort launch receipt missing or inconsistent")
    return {"selected_environment": EFFORT_ENV, "parent_cli_effort": "high",
            "command_sha256": inputs.sha(directory / "command.json"),
            "basis": "captured process environment and documented runtime precedence; not internal telemetry"}


class Adapter(runner.Adapter):
    def __init__(self):
        super().__init__()
        self.prior.HERE = self.prior.matrix.HERE = self.controller.HERE = HERE

    def inherited_evidence(self):
        proof = inputs.read(PRIOR / "preflight.json")
        paths = {"preflight.json", "preflight_audit.py", "preflight-review.md",
                 "calibration-results.json", "calibration-dispatches.json"}
        paths.update(proof["state"]["evidence"])
        paths.add(proof["state"]["path"])
        for side in ("baseline", "candidate"):
            root = PRIOR / ("binding-codex-" + side)
            paths.add(str((root / "manifest.json").relative_to(PRIOR)))
            paths.update(str((root / name).relative_to(PRIOR))
                         for name in inputs.read(root / "manifest.json"))
        return {name: inputs.sha(PRIOR / name) for name in sorted(paths)}

    def freeze(self):
        if inputs.sha(runner.FROZEN) != PREDECESSOR_SHA:
            raise ValueError("Predecessor execution identity changed")
        base = super().verify(runner.FROZEN)
        self.calibration_ready()
        runner.runtime_identity()
        inputs.write_new(FROZEN, {
            "predecessor_sha256": PREDECESSOR_SHA,
            "base": base,
            "claude_environment": EFFORT_ENV,
            "dependencies": {name: inputs.sha(HERE / name) for name in DEPENDENCIES},
            "inherited_evidence": self.inherited_evidence(),
            "calibration_relationship": "unchanged grader, packets, rubric, dispatches and returns; verify predecessor calibration",
        })
        self.verify()

    def verify(self, frozen=None):
        if frozen is not None and Path(frozen).resolve() != FROZEN:
            raise ValueError("Unexpected successor execution freeze")
        if inputs.sha(runner.FROZEN) != PREDECESSOR_SHA:
            raise ValueError("Predecessor execution identity changed")
        base = super().verify(runner.FROZEN)
        # The parent adapter returns the current case's rubric as a convenience.
        base["rubric_sha256"] = inputs.sha(self.rubric("R5"))
        data = inputs.read(FROZEN)
        if (data["predecessor_sha256"] != PREDECESSOR_SHA or data["base"] != base
                or data["claude_environment"] != EFFORT_ENV
                or set(data["dependencies"]) != set(DEPENDENCIES)):
            raise ValueError("Successor identity differs")
        runner.checked_files(HERE, data["dependencies"])
        if data["inherited_evidence"] != self.inherited_evidence():
            raise ValueError("Inherited evidence changed")
        return {**base, "rubric_sha256": inputs.sha(self.controller.RUBRIC)}

    def jobs(self):
        jobs = super().jobs()
        for job in jobs:
            job.workspace = WORKSPACES / job.evidence.name
            job.evidence = HERE / "runs" / job.evidence.name
            job.frozen = FROZEN
        return jobs

    def prepare(self, job):
        super().prepare(job)
        if job.provider == "claude":
            path = job.evidence / "launch.json"
            launch = inputs.read(path)
            launch["claude_effort_environment"] = EFFORT_ENV
            launch["models"]["claude_subagent_effort"] = "high"
            self.seed.write_json(path, launch)
            prepared = inputs.read(job.evidence / "prepared.json")
            prepared["launch_sha256"] = inputs.sha(path)
            self.seed.write_json(job.evidence / "prepared.json", prepared)

    def capture(self, job, interruption):
        if job.provider != "claude":
            return super().capture(job, interruption)
        launch = inputs.read(job.evidence / "launch.json")
        if (launch.get("claude_effort_environment") != EFFORT_ENV
                or launch["models"].get("claude_subagent_effort") != "high"):
            raise ValueError("Prepared Claude effort differs")
        with effort_override(self.prior.matrix.driver.capture):
            return super().capture(job, interruption)

    def audit(self):
        self.verify()
        self.calibration_ready()
        destination = HERE / "audits"
        destination.mkdir(exist_ok=False)
        for side in ("baseline", "candidate"):
            source = HERE / ("binding-claude-" + side)
            self.check_binding(source, "claude", side, FROZEN)
            detail = preflight_audit.claude(source, self.root / side / "retained/klaude-plugin", side)
            inputs.write_new(destination / (source.name + ".json"), {
                "manifest_sha256": inputs.sha(source / "manifest.json"),
                "effort": effort_receipt(source), **detail})

    def check_binding(self, directory, provider, side, frozen):
        runner.checked_files(directory, inputs.read(directory / "manifest.json"))
        if self.prior.matrix.runtime.completion_status(directory):
            raise ValueError("Binding failed")
        launch = inputs.read(directory / "launch.json")
        if (launch["fixture_manifest_sha256"] != inputs.sha(frozen)
                or launch["purpose"] != "binding probe" or launch["provider"] != provider
                or launch["side"] != side
                or launch["actor"] != inputs.read(self.controller.SNAPSHOTS[side] / "identity.json")
                or inputs.read(directory / "completion.json")["final_files"] != launch["initial_files"]):
            raise ValueError("Binding identity or subject changed")
        if provider == "claude":
            effort_receipt(directory)

    def retain(self):
        self.verify()
        destination = HERE / "runtime-inputs"
        destination.mkdir(exist_ok=False)
        secrets = [value.encode() for value in self.prior.matrix.codex.secrets() if value]
        retained = {}
        for side in ("baseline", "candidate"):
            name = "binding-claude-" + side
            source = HERE / name
            self.check_binding(source, "claude", side, FROZEN)
            workspace = Path(inputs.read(source / "launch.json")["workspace"])
            if workspace != WORKSPACES / name or workspace.is_symlink():
                raise ValueError("Unexpected owned workspace")
            prepared = inputs.read(source / "prepared.json")
            records = {**prepared["runtime_files"], ".capy.toml": prepared["capy_config_sha256"]}
            runner.checked_files(workspace, records)
            for relative, digest in records.items():
                path = workspace / relative
                content = path.read_bytes()
                if path.is_symlink() or any(secret in content for secret in secrets):
                    raise ValueError("Runtime link or credential in retained input")
                target = destination / name / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("xb") as stream:
                    stream.write(content)
                retained[target.relative_to(HERE).as_posix()] = digest
        runner.checked_files(HERE, retained)
        inputs.write_new(HERE / "runtime-inputs.json", retained)

    def preflight(self):
        self.verify()
        self.calibration_ready()
        proof = inputs.read(HERE / "preflight.json")
        if (proof["status"] != "PASS" or proof["execution_freeze_sha256"] != inputs.sha(FROZEN)
                or proof["calibration_results_sha256"] != inputs.sha(PRIOR / "calibration-results.json")):
            raise ValueError("Successor preflight does not match execution/calibration")
        expected = {f"binding-{provider}-{side}" for provider in ("claude", "codex")
                    for side in ("baseline", "candidate")}
        if set(proof["binding_manifests"]) != expected:
            raise ValueError("All four identified bindings are required")
        for name, digest in proof["binding_manifests"].items():
            _, provider, side = name.split("-")
            directory = (HERE if provider == "claude" else PRIOR) / name
            if inputs.sha(directory / "manifest.json") != digest:
                raise ValueError("Binding seal changed")
            self.check_binding(directory, provider, side, FROZEN if provider == "claude" else runner.FROZEN)
        prior = inputs.read(PRIOR / "preflight.json")
        if proof["inherited_state"] != prior["state"]:
            raise ValueError("State evidence differs from reviewed predecessor")
        state = inputs.read(PRIOR / prior["state"]["path"])
        if (len(state) != 2 or len({r["store"] for r in state}) != 2
                or len({r["workspace"] for r in state}) != 2):
            raise ValueError("Two independent state probes required")
        for row in state:
            if (row["status"] != "PASS" or row["initial_seed"] != "empty"
                    or row["index_search"] != "PASS" or row["foreign_marker_absent"] is not True
                    or row["vault"] != "unavailable; CAPY_VAULT_KEY unset"):
                raise ValueError("State isolation was not established")
        review = proof["independent_review"]
        runner.checked_files(HERE, {review["path"]: review["sha256"]})
        if review["status"] != "PASS":
            raise ValueError("Independent preflight review not approved")
        runner.checked_files(HERE, proof["audit_files"])
        expected_audits = {f"audits/binding-claude-{s}.json" for s in ("baseline", "candidate")}
        if set(proof["audit_files"]) != expected_audits:
            raise ValueError("Both fresh Claude receipt audits required")
        retained = inputs.read(HERE / "runtime-inputs.json")
        if proof["runtime_inputs_sha256"] != inputs.sha(HERE / "runtime-inputs.json"):
            raise ValueError("Runtime retention receipt changed")
        expected_runtime = {}
        for side in ("baseline", "candidate"):
            name = "binding-claude-" + side
            prepared = inputs.read(HERE / name / "prepared.json")
            records = {**prepared["runtime_files"], ".capy.toml": prepared["capy_config_sha256"]}
            expected_runtime.update({f"runtime-inputs/{name}/{path}": digest for path, digest in records.items()})
        if retained != expected_runtime:
            raise ValueError("Runtime retention coverage differs")
        runner.checked_files(HERE, retained)

    def grade(self, job):
        sys.path.insert(0, str(self.verification / "task12"))
        from prepare_grades import prepare
        with self.case_context(job.case):
            prepare(job.evidence, HERE / "grading" / job.evidence.name, FROZEN)
        path = HERE / "grading" / job.evidence.name / "manifest.json"
        manifest = inputs.read(path)
        manifest["identity"]["rubric_version"] = self.matrix_data["cases"][job.case]["rubric"]
        self.seed.write_json(path, manifest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("freeze", "verify", "binding", "audit", "retain", "preflight", "list", "prepare", "run", "grade"))
    parser.add_argument("--side", choices=("baseline", "candidate"))
    parser.add_argument("--job")
    args = parser.parse_args()
    if (args.operation == "binding") != bool(args.side) or (args.job and args.operation != "grade"):
        parser.error("binding requires --side; --job is grading-only")
    adapter = Adapter()
    if args.operation == "freeze":
        adapter.freeze()
        return 0
    adapter.verify()
    runner.runtime_identity()
    if args.operation == "binding":
        adapter.calibration_ready()
        name = "binding-claude-" + args.side
        job = argparse.Namespace(provider="claude", side=args.side, case="R6M", mode="standard",
            repetition=0, snapshot=adapter.controller.SNAPSHOTS[args.side],
            workspace=WORKSPACES / name, evidence=HERE / name, frozen=FROZEN, binding=True)
        return adapter.prior.matrix.runtime.run_batch([job], adapter.prepare, adapter.capture)
    if args.operation in ("audit", "retain", "preflight"):
        getattr(adapter, args.operation)()
    elif args.operation == "list":
        print("\n".join(j.evidence.name for j in adapter.jobs()))
    elif args.operation == "prepare":
        adapter.preflight()
        for job in adapter.jobs():
            adapter.prepare(job)
    elif args.operation == "run":
        return adapter.run(adapter.jobs())
    elif args.operation == "grade":
        selected = [j for j in adapter.jobs() if not args.job or j.evidence.name == args.job]
        if not selected:
            parser.error("unknown job")
        for job in selected:
            adapter.grade(job)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
