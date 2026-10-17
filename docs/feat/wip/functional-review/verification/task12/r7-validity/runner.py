"""Task 12.14: four unchanged-skill Claude standard diagnostics; no PAL."""
import argparse
import importlib.util
import json
from pathlib import Path
import host_runtime

HERE = Path(__file__).resolve().parent
WORKSPACES = Path("/tmp/fr-r7-validity-20261014").resolve()
REVISION = "6bc277ea6d1ee023cb30a1246c983456eff86fdb"
CASES = {
    "R7M": ("review-code", "functional-material-provider-unknown", ("standard",)),
    "R7B": ("review-code", "functional-benign-provider-contract", ("standard",)),
}
spec = importlib.util.spec_from_file_location("prior_r7", HERE.parent / "r7-conclusions/runner.py")
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
controller = prior.matrix.controller
seed = controller.seed


def configure():
    # Historical transport uses side keys; only "candidate" is launched, as
    # unchanged current source. Neither alias represents a new skill candidate.
    prior.HERE, prior.WORKSPACES, prior.CASES = HERE, WORKSPACES, set(CASES)
    prior.matrix.HERE = HERE
    controller.HERE = HERE
    controller.BASELINE = controller.CANDIDATE = REVISION
    controller.CASES = seed.SEEDS = CASES
    controller.SNAPSHOTS = {side: HERE / "source-inputs" for side in ("baseline", "candidate")}
    controller.RUBRIC = HERE / "rubric.md"
    extra = [
        Path(__file__), HERE / "host_runtime.py", HERE.parent / "r7-conclusions/runner.py",
        HERE.parent / "opus55/matrix.py", HERE.parent / "rework/driver.py",
        HERE.parent / "rework/runtime.py", HERE.parent / "rework/capture.py",
        HERE.parent / "prepare_grades.py", controller.VERIFICATION / "task8/prepare_grading.py",
    ]
    controller.DEPENDENCIES = list(dict.fromkeys([*controller.DEPENDENCIES, *extra]))
    return HERE / "freeze.json"


def jobs_for(frozen):
    return [job for job in prior.jobs_for(frozen, ("claude",)) if job.side == "candidate"]


def capture(job, interruption):
    runtime = prior.matrix.runtime
    previous = runtime._signal_group
    try:
        runtime._signal_group = host_runtime.signal_group
        return prior.capture(job, interruption)
    finally:
        runtime._signal_group = previous


def prepare_grades(job, frozen):
    from prepare_grades import prepare
    target = HERE / "grading" / job.evidence.name
    prepare(job.evidence, target, frozen)
    path = target / "manifest.json"
    manifest = json.loads(path.read_text())
    manifest["identity"]["rubric_version"] = "r7-validity-v1"
    manifest["identity"]["diagnostic_adapter"] = seed.sha(Path(__file__).read_bytes())
    manifest["run"]["purpose"] = "unchanged-current-skill diagnostic; not a paired comparison"
    manifest["completeness"]["dispatches"] = "standard mode; no independent actor handoff assertion"
    seed.write_json(path, manifest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("freeze", "binding", "prepare", "run", "grade", "list"))
    parser.add_argument("--run")
    args = parser.parse_args()
    if args.run and args.operation not in ("run", "grade"):
        parser.error("--run only selects an already prepared run or grading package")
    frozen = configure()
    jobs = jobs_for(frozen)
    if args.run:
        jobs = [job for job in jobs if job.evidence.name == args.run]
        if not jobs:
            parser.error("unknown run")
    if args.operation == "freeze":
        controller.freeze(frozen)
    elif args.operation == "binding":
        job = argparse.Namespace(provider="claude", side="candidate", case="R7M",
            mode="standard", repetition=0, snapshot=controller.SNAPSHOTS["candidate"],
            workspace=WORKSPACES / "binding", evidence=HERE / "binding",
            frozen=frozen, binding=True)
        return prior.matrix.runtime.run_batch([job], prior.prepare, capture)
    elif args.operation == "prepare":
        for job in jobs:
            prior.prepare(job)
    elif args.operation == "grade":
        for job in jobs:
            prepare_grades(job, frozen)
    elif args.operation == "list":
        print(json.dumps([job.evidence.name for job in jobs], indent=2))
    else:
        # All four must be prepared, even when capture is resumed one run at a time.
        for job in jobs_for(frozen):
            if not (job.evidence / "prepared.json").is_file():
                raise ValueError("Prepare all four inputs before measurement")
        for job in jobs:
            if (job.evidence / "manifest.json").exists():
                raise FileExistsError("Refuse to overwrite any retained attempt")
        with prior.matrix.runtime.capture_signals() as interruption:
            for job in jobs:
                capture(job, interruption)
                status = prior.matrix.runtime.completion_status(job.evidence)
                if interruption[0] or status:
                    return 128 + interruption[0] if interruption[0] else status
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
