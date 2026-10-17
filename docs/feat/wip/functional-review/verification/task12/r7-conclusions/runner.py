"""Task 12.13: unchanged matrix transport, selected cases, explicit PAL exclusion."""
import argparse
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKSPACES = Path("/tmp/fr-r7-conclusions-20261013")
CASES = {"R7", "R3", "R5"}
spec = importlib.util.spec_from_file_location("r7_matrix", HERE.parent / "opus55/matrix.py")
matrix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(matrix)


def marketplace(side):
    revision = matrix.controller.BASELINE if side == "baseline" else matrix.controller.CANDIDATE
    return "fr-r7-" + revision[:8] + "-20261013"


def configure():
    matrix.HERE = HERE
    matrix.marketplace = marketplace
    frozen = matrix.configure()
    matrix.controller.DEPENDENCIES.append(Path(__file__))
    return frozen


def jobs_for(frozen, providers=("claude", "codex")):
    jobs = [job for job in matrix.jobs_for(frozen, providers) if job.case in CASES]
    for job in jobs:
        job.workspace = WORKSPACES / job.evidence.name
        job.evidence = HERE / "runs" / job.evidence.name
    return jobs


def prepare(job):
    matrix.prepare(job)
    if job.provider != "claude":
        return  # The inherited Codex adapter already disables PAL.
    seed = matrix.seed
    mcp = json.loads((job.workspace / ".runner/mcp.json").read_text())
    mcp["mcpServers"].pop("pal", None)
    mcp_path = job.workspace / ".runner/mcp-no-pal.json"
    seed.write_new_json(mcp_path, mcp)
    launch_path = job.evidence / "launch.json"
    launch = json.loads(launch_path.read_text())
    launch["models"]["pal"] = "user-deferred; absent from launched MCP configuration"
    launch["mcp"].pop("pal", None)
    seed.write_json(launch_path, launch)
    prepared_path = job.evidence / "prepared.json"
    prepared = json.loads(prepared_path.read_text())
    prepared["launch_sha256"] = seed.sha(launch_path.read_bytes())
    prepared["runtime_files"][".runner/mcp-no-pal.json"] = seed.sha(mcp_path.read_bytes())
    seed.write_json(prepared_path, prepared)


def capture(job, interruption):
    if job.provider != "claude":
        return matrix.capture(job, interruption)
    previous = matrix.driver.capture.command_for

    def command_without_pal(prompt):
        command = previous(prompt)
        command[command.index("--mcp-config") + 1] = ".runner/mcp-no-pal.json"
        return command

    try:
        matrix.driver.capture.command_for = command_without_pal
        return matrix.capture(job, interruption)
    finally:
        matrix.driver.capture.command_for = previous


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("freeze", "binding", "prepare", "run", "grade", "list"))
    parser.add_argument("--provider", choices=("claude", "codex"))
    parser.add_argument("--side", choices=("baseline", "candidate"))
    parser.add_argument("--run")
    args = parser.parse_args()
    if args.operation == "binding" and (not args.provider or not args.side or args.run):
        parser.error("binding requires provider and side, without --run")
    if args.operation != "binding" and args.side:
        parser.error("--side is only valid for binding")
    if args.run and args.operation not in ("run", "grade"):
        parser.error("--run is only valid for run or grade")
    frozen = configure()
    jobs = jobs_for(frozen, (args.provider,) if args.provider else ("claude", "codex"))
    if args.run:
        jobs = [job for job in jobs if job.evidence.name == args.run]
        if not jobs:
            parser.error("unknown run")
    if args.operation == "freeze":
        matrix.controller.freeze(frozen)
    elif args.operation == "binding":
        name = f"binding-{args.provider}-{args.side}"
        job = argparse.Namespace(provider=args.provider, side=args.side, case="R7", mode="standard",
            repetition=0, snapshot=matrix.controller.SNAPSHOTS[args.side],
            workspace=WORKSPACES / name, evidence=HERE / name, frozen=frozen, binding=True)
        return matrix.runtime.run_batch([job], prepare, capture)
    elif args.operation == "prepare":
        for job in jobs:
            prepare(job)
    elif args.operation == "grade":
        from prepare_grades import prepare as prepare_grade
        for job in jobs:
            prepare_grade(job.evidence, HERE / "grading" / job.evidence.name, frozen)
    elif args.operation == "list":
        print(json.dumps([job.evidence.name for job in jobs], indent=2))
    else:
        for job in jobs:
            if not (job.evidence / "prepared.json").is_file():
                raise ValueError("Prepare all selected inputs before running")
            if (job.evidence / "manifest.json").exists():
                raise FileExistsError("Refuse to overwrite prior attempts")
        with matrix.runtime.capture_signals() as interruption:
            for job in jobs:
                capture(job, interruption)
                status = matrix.runtime.completion_status(job.evidence)
                if interruption[0] or status:
                    return 128 + interruption[0] if interruption[0] else status
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
