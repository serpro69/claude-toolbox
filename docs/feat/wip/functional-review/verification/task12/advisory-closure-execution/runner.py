"""Serial adapter for the frozen 64-session advisory comparison. Python 3.12."""
import argparse
from contextlib import contextmanager
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys

import inputs

HERE = Path(__file__).resolve().parent
FROZEN = HERE / "execution-freeze.json"
WORKSPACES = Path("/tmp/fr-advisory-actors-20261017")
VERIFICATION_REL = Path("docs/feat/wip/functional-review/verification")


def checked_files(root, records):
    root = Path(root).resolve()
    for relative, digest in records.items():
        path = root / relative
        if (Path(relative).is_absolute() or ".." in Path(relative).parts
                or not path.resolve().is_relative_to(root) or inputs.sha(path) != digest):
            raise ValueError("Changed or unsafe sealed file: " + relative)


def runtime_identity():
    expected = inputs.read(inputs.PREPARATION / "runtime.json")
    for name, identity in expected["executables"].items():
        actual = shutil.which(name)
        if (not actual or Path(actual).resolve() != Path(identity["path"])
                or inputs.sha(actual) != identity["sha256"]):
            raise ValueError("Runtime executable changed: " + name)
        if subprocess.check_output([name, "--version"], text=True).strip() != expected["versions"][name]:
            raise ValueError("Runtime version changed: " + name)
    if Path(sys.executable).resolve() != Path(expected["executables"]["python3"]["path"]):
        raise ValueError("Use the declared Python interpreter and PATH")
    return expected


class Adapter:
    def __init__(self, root=inputs.DEFAULT_ROOT):
        self.root = inputs.verify_restored(root)
        self.repository = self.root / "repository"
        self.verification = self.repository / VERIFICATION_REL
        self.matrix_data = inputs.read(inputs.PREPARATION / "matrix.json")
        self.preparation = inputs.read(inputs.PREPARATION / "freeze.json")
        # One restored runtime per process; do not reuse modules from another checkout.
        for name in ("controller", "capture", "driver", "runtime", "probe_state", "prepare_grades"):
            module = sys.modules.get(name)
            if module and not Path(module.__file__).resolve().is_relative_to(self.repository):
                raise ValueError("Conflicting runtime import: " + name)
        sys.dont_write_bytecode = True
        spec = importlib.util.spec_from_file_location("advisory_transport",
            self.verification / "task12/r7-conclusions/runner.py")
        self.prior = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.prior)
        self.controller = self.prior.matrix.controller
        self.seed = self.controller.seed
        self.prior.HERE = self.prior.matrix.HERE = self.controller.HERE = HERE
        self.controller.BASELINE = self.preparation["baseline_revision"]
        self.controller.CANDIDATE = self.preparation["candidate_revision"]
        self.controller.SNAPSHOTS = {s: self.root / s for s in ("baseline", "candidate")}
        cases = {key: ("review-code", Path(row["fixture"]).name, ("standard", "isolated"))
                 for key, row in self.matrix_data["cases"].items()}
        self.controller.CASES = self.seed.SEEDS = cases
        self.seed.REPO = self.repository
        self.controller.GRADER = self.verification / "task2b/grader.md"
        self.controller.RUBRIC = self.rubric("R5")
        self.controller.verify_frozen = self.verify
        self.prior.matrix.marketplace = lambda side: "fr-advisory-" + (
            self.controller.BASELINE if side == "baseline" else self.controller.CANDIDATE)[:8]

    def rubric(self, case):
        name = self.matrix_data["cases"][case]["rubric"]
        return self.verification / ("task12/r6-validity/rubric.md"
                                    if name == "r6-validity-v1" else "task2-rubric-v2.md")

    @contextmanager
    def case_context(self, case):
        original = self.controller.RUBRIC
        self.controller.RUBRIC = self.rubric(case)
        try:
            yield
        finally:
            self.controller.RUBRIC = original

    def jobs(self):
        return [argparse.Namespace(**{k: row[k] for k in
                ("provider", "side", "case", "mode", "repetition")},
                snapshot=self.controller.SNAPSHOTS[row["side"]],
                workspace=WORKSPACES / row["id"], evidence=HERE / "runs" / row["id"],
                frozen=FROZEN, binding=False) for row in self.matrix_data["jobs"]]

    def freeze(self):
        runtime = runtime_identity()
        data = {
            "preparation_sha256": inputs.PREPARATION_SHA,
            "baseline": self.controller.BASELINE, "candidate": self.controller.CANDIDATE,
            "input_root": str(self.root), "controller_python": sys.version,
            "runtimes": runtime["versions"], "runtime_identity": runtime,
            "rubrics": {case: inputs.sha(self.rubric(case)) for case in self.controller.CASES},
            "grader_sha256": inputs.sha(self.controller.GRADER),
            "fixtures": {case: self.seed.files(self.seed.fixture(case)) for case in self.controller.CASES},
            "prompts": {f"{r['provider']}/{r['case']}/{r['mode']}": r["prompt"]
                        for r in self.matrix_data["jobs"]},
            "snapshots": {side: inputs.read(path / "identity.json")
                          for side, path in self.controller.SNAPSHOTS.items()},
            "dependencies": {p.name: inputs.sha(p) for p in
                (HERE / "runner.py", HERE / "inputs.py", HERE / "calibration.py",
                 HERE / "test_runner.py", HERE / "execution-contract.md")},
            "calibration_inputs": {p.relative_to(HERE).as_posix(): inputs.sha(p)
                for p in sorted((HERE / "calibration").rglob("*")) if p.is_file()},
        }
        if not data["calibration_inputs"]:
            raise ValueError("Build and review calibration inputs first")
        inputs.write_new(FROZEN, data)
        self.verify(FROZEN)

    def verify(self, frozen=None):
        frozen = FROZEN if frozen is None else frozen
        if Path(frozen).resolve() != FROZEN:
            raise ValueError("Unexpected execution freeze")
        data = inputs.read(frozen)
        inputs.verify_restored(self.root)
        if (data["preparation_sha256"] != inputs.PREPARATION_SHA
                or data["input_root"] != str(self.root)
                or data["baseline"] != self.controller.BASELINE
                or data["candidate"] != self.controller.CANDIDATE):
            raise ValueError("Frozen source identity differs")
        checked_files(HERE, data["dependencies"])
        checked_files(HERE, data["calibration_inputs"])
        for side, path in self.controller.SNAPSHOTS.items():
            if inputs.read(path / "identity.json") != data["snapshots"][side]:
                raise ValueError("Snapshot identity drift")
        if inputs.sha(self.controller.GRADER) != data["grader_sha256"]:
            raise ValueError("Grader drift")
        for case in self.controller.CASES:
            if (self.seed.files(self.seed.fixture(case)) != data["fixtures"][case]
                    or inputs.sha(self.rubric(case)) != data["rubrics"][case]):
                raise ValueError("Fixture/rubric drift")
        expected = {f"{r['provider']}/{r['case']}/{r['mode']}": r["prompt"]
                    for r in self.matrix_data["jobs"]}
        if expected != data["prompts"]:
            raise ValueError("Prompt drift")
        # The inherited preparer/grading adapter expects a single selected rubric.
        return {**data, "rubric_sha256": inputs.sha(self.controller.RUBRIC)}

    def calibration_ready(self):
        import calibration
        calibration.verify_results()

    def preflight(self):
        self.verify()
        self.calibration_ready()
        proof = inputs.read(HERE / "preflight.json")
        if (proof["status"] != "PASS" or proof["execution_freeze_sha256"] != inputs.sha(FROZEN)
                or proof["calibration_results_sha256"] != inputs.sha(HERE / "calibration-results.json")):
            raise ValueError("Preflight does not match execution/calibration")
        expected = {f"binding-{provider}-{side}" for provider in ("claude", "codex")
                    for side in ("baseline", "candidate")}
        if set(proof["binding_manifests"]) != expected:
            raise ValueError("All four bindings are required")
        for name, digest in proof["binding_manifests"].items():
            directory = HERE / name
            if inputs.sha(directory / "manifest.json") != digest:
                raise ValueError("Binding seal changed")
            checked_files(directory, inputs.read(directory / "manifest.json"))
            if self.prior.matrix.runtime.completion_status(directory):
                raise ValueError("Binding failed")
            _, provider, side = name.split("-")
            launch = inputs.read(directory / "launch.json")
            if (launch["fixture_manifest_sha256"] != inputs.sha(FROZEN)
                    or launch["provider"] != provider or launch["side"] != side
                    or launch["purpose"] != "binding probe"
                    or launch["actor"] != inputs.read(self.controller.SNAPSHOTS[side] / "identity.json")):
                raise ValueError("Binding belongs to another runtime/source")
        for key in ("state", "independent_review"):
            record = proof[key]
            checked_files(HERE, {record["path"]: record["sha256"]})
            if record["status"] != "PASS":
                raise ValueError("Preflight prerequisite not approved: " + key)
        state = inputs.read(HERE / proof["state"]["path"])
        if len(state) != 2 or len({r["store"] for r in state}) != 2 or len({r["workspace"] for r in state}) != 2:
            raise ValueError("Two independent state probes required")
        for row in state:
            if (row["status"] != "PASS" or row["initial_seed"] != "empty"
                    or row["index_search"] != "PASS" or row["foreign_marker_absent"] is not True
                    or row["vault"] != "unavailable; CAPY_VAULT_KEY unset"):
                raise ValueError("State isolation was not established")
        checked_files(HERE, proof["state"]["evidence"])
        if not proof["state"]["evidence"]:
            raise ValueError("State summary needs retained probe evidence")

    def prepare(self, job):
        if job.workspace.exists() or job.evidence.exists():
            raise FileExistsError("Refuse workspace/evidence reuse")
        with self.case_context(job.case):
            self.prior.prepare(job)

    def capture(self, job, interruption):
        if any((job.evidence / p).exists() for p in
               ("manifest.json", "command.json", "events.jsonl", "protocol.jsonl", "capture-error.json")):
            raise FileExistsError("Refuse to overwrite or retry an attempt")
        with self.case_context(job.case):
            self.prior.capture(job, interruption)

    def run(self, jobs):
        self.preflight()
        runtime_identity()
        validate_batch(jobs)
        with self.prior.matrix.runtime.capture_signals() as interruption:
            for job in jobs:
                self.capture(job, interruption)
                result = self.prior.matrix.runtime.completion_status(job.evidence)
                if interruption[0] or result:
                    return 128 + interruption[0] if interruption[0] else result
        return 0

    def grade(self, job):
        # Use the inherited sealed-evidence exporter with this case's pinned rubric.
        sys.path.insert(0, str(self.verification / "task12"))
        from prepare_grades import prepare
        with self.case_context(job.case):
            prepare(job.evidence, HERE / "grading" / job.evidence.name, FROZEN)
        path = HERE / "grading" / job.evidence.name / "manifest.json"
        manifest = inputs.read(path)
        manifest["identity"]["rubric_version"] = self.matrix_data["cases"][job.case]["rubric"]
        self.seed.write_json(path, manifest)


def validate_batch(jobs):
    if len(jobs) != 64 or len({j.evidence.name for j in jobs}) != 64:
        raise ValueError("The complete declared batch is required")
    for job in jobs:
        if not (job.evidence / "prepared.json").is_file():
            raise ValueError("Prepare all 64 inputs before capture")
        if any((job.evidence / p).exists() for p in
               ("manifest.json", "command.json", "events.jsonl", "protocol.jsonl", "capture-error.json")):
            raise FileExistsError("A declared attempt already exists; no implicit resume")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("restore", "list", "freeze", "verify", "prepare", "binding", "run", "grade"))
    parser.add_argument("--provider", choices=("claude", "codex"))
    parser.add_argument("--side", choices=("baseline", "candidate"))
    parser.add_argument("--job")
    args = parser.parse_args()
    if args.operation == "binding":
        if not args.provider or not args.side or args.job:
            parser.error("binding requires provider and side only")
    elif args.provider or args.side or (args.job and args.operation != "grade"):
        parser.error("provider/side are binding-only; job is grading-only")
    if args.operation == "restore":
        print(inputs.restore())
        return 0
    adapter = Adapter()
    jobs = adapter.jobs()
    if args.operation == "list":
        print("\n".join(j.evidence.name for j in jobs))
    elif args.operation == "freeze":
        adapter.freeze()
    elif args.operation == "verify":
        adapter.verify()
        runtime_identity()
    elif args.operation == "prepare":
        adapter.preflight()
        for job in jobs:
            adapter.prepare(job)
    elif args.operation == "binding":
        adapter.verify()
        adapter.calibration_ready()
        runtime_identity()
        name = f"binding-{args.provider}-{args.side}"
        job = argparse.Namespace(provider=args.provider, side=args.side, case="R6M", mode="standard",
            repetition=0, snapshot=adapter.controller.SNAPSHOTS[args.side], workspace=WORKSPACES / name,
            evidence=HERE / name, frozen=FROZEN, binding=True)
        return adapter.prior.matrix.runtime.run_batch([job], adapter.prepare, adapter.capture)
    elif args.operation == "run":
        return adapter.run(jobs)
    else:
        selected = [j for j in jobs if not args.job or j.evidence.name == args.job]
        if not selected:
            parser.error("unknown job")
        for job in selected:
            adapter.grade(job)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
