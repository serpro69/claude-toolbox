"""Frozen successor adapter for the bounded R1/R3/R5 diagnostic batch."""
import argparse
import json
from pathlib import Path
import sys

import capture
from runtime import run_batch

controller = capture.controller
HERE = Path(__file__).resolve().parent


def configure(declaration):
    declaration = declaration.resolve()
    config = json.loads(declaration.read_text())
    controller.CANDIDATE = config["candidate"]
    controller.SNAPSHOTS = {side: Path(path) for side, path in config["snapshots"].items()}
    if set(controller.SNAPSHOTS) != {"baseline", "candidate"}:
        raise ValueError("Both fixed actor snapshots are required")
    controller.HERE = declaration.parent
    controller.DEPENDENCIES.extend([Path(__file__), HERE / "runtime.py", HERE / "capture.py", declaration,
        HERE.parent / "prepare_grades.py", controller.VERIFICATION / "task8/prepare_grading.py"])
    return declaration.parent / "freeze.json"


def capture_job(job, interruption):
    previous = controller.seed.run_claude
    try:
        controller.seed.run_claude = lambda evidence: capture.run_claude(evidence, interruption)
        controller.run(job.evidence, job.frozen)
    finally:
        controller.seed.run_claude = previous


def jobs_for(frozen, workspace_root, cases):
    jobs = []
    for case in cases:
        for side in ("baseline", "candidate"):
            for repetition in (1, 2):
                name = f"claude-{side}-{case}-standard-{repetition}"
                jobs.append(argparse.Namespace(provider="claude", side=side, case=case,
                    mode="standard", snapshot=controller.SNAPSHOTS[side],
                    workspace=workspace_root / name, evidence=controller.HERE / "runs" / name,
                    frozen=frozen, binding=False))
    return jobs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("declaration", type=Path)
    sub = parser.add_subparsers(dest="operation", required=True)
    sub.add_parser("freeze")
    batch = sub.add_parser("batch")
    batch.add_argument("workspace_root", type=Path)
    batch.add_argument("--case", action="append", choices=("R1", "R3", "R5"))
    binding = sub.add_parser("binding")
    binding.add_argument("side", choices=("baseline", "candidate"))
    binding.add_argument("workspace", type=Path)
    binding.add_argument("evidence", type=Path)
    grade = sub.add_parser("grade")
    grade.add_argument("evidence", type=Path)
    grade.add_argument("destination", type=Path)
    args = parser.parse_args()
    frozen = configure(args.declaration)
    if args.operation == "freeze":
        controller.freeze(frozen)
        return 0
    if args.operation == "grade":
        from prepare_grades import prepare
        prepare(args.evidence.resolve(), args.destination.resolve(), frozen)
        return 0
    if args.operation == "batch":
        cases = args.case or ["R1", "R3", "R5"]
        if len(cases) != len(set(cases)):
            raise ValueError("Duplicate diagnostic case")
        jobs = jobs_for(frozen, args.workspace_root.resolve(), cases)
        return run_batch(jobs, controller.prepare, capture_job)
    job = argparse.Namespace(provider="claude", side=args.side, case="R1",
        mode="standard", snapshot=controller.SNAPSHOTS[args.side],
        workspace=args.workspace.resolve(), evidence=args.evidence.resolve(),
        frozen=frozen, binding=True)
    return run_batch([job], controller.prepare, capture_job)


if __name__ == "__main__":
    raise SystemExit(main())
