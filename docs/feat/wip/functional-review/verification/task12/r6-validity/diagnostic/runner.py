"""Eight R6 standard diagnostics on unchanged instructions; no PAL."""
import argparse
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKSPACES = Path("/tmp/fr-r6-diagnostic-20261017").resolve()
REVISION = "6093213a2710708d90b43733ac024da6779bc32b"
CASES = {
    "R6M": ("review-code", "functional-inherited-defect-exposed", ("standard",)),
    "R6D": ("review-code", "functional-inherited-defect-dormant", ("standard",)),
}
TASK12 = HERE.parents[1]
spec = importlib.util.spec_from_file_location("r6_prior", TASK12 / "r7-conclusions/runner.py")
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
controller = prior.matrix.controller
seed = controller.seed


def configure():
    prior.HERE, prior.WORKSPACES, prior.CASES = HERE, WORKSPACES, set(CASES)
    prior.matrix.HERE = controller.HERE = HERE
    prior.matrix.marketplace = lambda side: "fr-r6-6093213a-20261017"
    controller.BASELINE = controller.CANDIDATE = REVISION
    controller.CASES = seed.SEEDS = CASES
    controller.SNAPSHOTS = {side: HERE / "source-inputs" for side in ("baseline", "candidate")}
    controller.RUBRIC = HERE.parent / "rubric.md"
    extra = [Path(__file__), HERE / "calibration.py", HERE / "test_runner.py",
             TASK12 / "r7-conclusions/runner.py", TASK12 / "opus55/matrix.py",
             TASK12 / "rework/driver.py", TASK12 / "rework/runtime.py",
             TASK12 / "rework/capture.py", TASK12 / "prepare_grades.py",
             controller.VERIFICATION / "task8/prepare_grading.py"]
    extra.extend(p for p in (HERE / "calibration").rglob("*") if p.is_file())
    for name in ("ordered", "early-edit", "missing-events", "requested-only", "complete-omission"):
        extra.extend(p for p in (TASK12 / "r7-conclusions/calibration/inputs" / name).rglob("*") if p.is_file())
    controller.DEPENDENCIES = list(dict.fromkeys([*controller.DEPENDENCIES, *extra]))
    return HERE / "freeze.json"


def jobs_for(frozen):
    return [job for job in prior.jobs_for(frozen) if job.side == "candidate"]


def validate_batch(jobs, all_jobs):
    for job in all_jobs:
        if not (job.evidence / "prepared.json").is_file():
            raise ValueError("Prepare all eight inputs before measurement")
    for job in jobs:
        if any((job.evidence / name).exists() for name in
               ("manifest.json", "command.json", "events.jsonl", "protocol.jsonl")):
            raise FileExistsError("Refuse to overwrite or retry a retained attempt")


def verify_calibration():
    expected = json.loads((HERE / "calibration/expected-verdicts.json").read_text())
    results = json.loads((HERE / "calibration/results.json").read_text())
    for name, outcome in expected.items():
        if results["semantic"][name]["verdicts"] != outcome["verdicts"]:
            raise ValueError("Calibration verdict mismatch: " + name)
        if results["semantic"][name]["triggers"] != outcome["triggers"]:
            raise ValueError("Calibration trigger mismatch: " + name)
    old = json.loads((TASK12 / "r7-conclusions/calibration/inputs/expected-verdicts.json").read_text())
    for name in ("ordered", "early-edit", "missing-events", "requested-only", "complete-omission"):
        if results["ordering"][name] != old[name]:
            raise ValueError("Ordering calibration mismatch: " + name)


def verify_preflight(frozen):
    proof = json.loads((HERE / "preflight.json").read_text())
    if proof["freeze_sha256"] != seed.sha(frozen.read_bytes()) or proof["status"] != "PASS":
        raise ValueError("Preflight belongs to another freeze or did not pass")
    for name in ("binding-claude", "binding-codex"):
        source = HERE / name
        if seed.sha((source / "manifest.json").read_bytes()) != proof["binding_manifests"][name]:
            raise ValueError("Binding seal changed")
        for relative, digest in json.loads((source / "manifest.json").read_text()).items():
            if seed.sha((source / relative).read_bytes()) != digest:
                raise ValueError("Binding evidence changed: " + relative)
        if prior.matrix.runtime.completion_status(source):
            raise ValueError("Binding did not complete")
    if seed.sha((HERE / "state-probe/summary.json").read_bytes()) != proof["state_summary_sha256"]:
        raise ValueError("State probe summary changed")


def prepare_grades(job, frozen):
    from prepare_grades import prepare
    target = HERE / "grading" / job.evidence.name
    prepare(job.evidence, target, frozen)
    path = target / "manifest.json"
    manifest = json.loads(path.read_text())
    manifest["identity"]["rubric_version"] = "r6-validity-v1"
    manifest["identity"]["diagnostic_adapter"] = seed.sha(Path(__file__).read_bytes())
    manifest["run"]["purpose"] = "unchanged-instruction diagnostic; not a paired comparison"
    manifest["completeness"]["dispatches"] = "standard mode; isolated-dispatch condition absent"
    seed.write_json(path, manifest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("freeze", "binding", "prepare", "run", "grade", "list"))
    parser.add_argument("--provider", choices=("claude", "codex"))
    parser.add_argument("--run")
    args = parser.parse_args()
    if args.provider and args.operation != "binding":
        parser.error("--provider is only for a binding probe")
    if args.operation == "binding" and not args.provider:
        parser.error("binding requires --provider")
    if args.run and args.operation not in ("run", "grade"):
        parser.error("--run only selects a prepared capture or grading package")
    frozen = configure()
    all_jobs = jobs_for(frozen)
    jobs = [job for job in all_jobs if not args.run or job.evidence.name == args.run]
    if not jobs:
        parser.error("unknown run")
    if args.operation == "freeze":
        verify_calibration()
        controller.freeze(frozen)
    elif args.operation == "binding":
        name = "binding-" + args.provider
        job = argparse.Namespace(provider=args.provider, side="candidate", case="R6M",
            mode="standard", repetition=0, snapshot=controller.SNAPSHOTS["candidate"],
            workspace=WORKSPACES / name, evidence=HERE / name, frozen=frozen, binding=True)
        return prior.matrix.runtime.run_batch([job], prior.prepare, prior.capture)
    elif args.operation == "prepare":
        for job in jobs:
            prior.prepare(job)
    elif args.operation == "grade":
        for job in jobs:
            prepare_grades(job, frozen)
    elif args.operation == "list":
        print(json.dumps([job.evidence.name for job in jobs], indent=2))
    else:
        verify_preflight(frozen)
        validate_batch(jobs, all_jobs)
        with prior.matrix.runtime.capture_signals() as interruption:
            for job in jobs:
                prior.capture(job, interruption)
                status = prior.matrix.runtime.completion_status(job.evidence)
                if interruption[0] or status:
                    return 128 + interruption[0] if interruption[0] else status
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
