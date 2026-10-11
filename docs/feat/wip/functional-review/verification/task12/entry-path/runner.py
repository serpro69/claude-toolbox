"""Task 12.12: bounded isolated-mode jobs using the unchanged reviewed transport."""
import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "rework"))
import driver
import runtime

CASES = ("R3", "R5", "R9-recovery")
WORKSPACES = Path("/tmp/fr-entry-path-20261011")
BINDING_PROMPT = (
    "This is an instruction-loading probe only. Do not review or modify subject files. "
    "Invoke /kk:review-code:isolated to load the selected command, its entry point "
    "and required workflow/methodology instructions, then stop before investigation. "
    "Run exactly `printenv TOOLBOX_PLUGIN_ROOT` to check the SessionStart root. "
    "Use the named kk:code-reviewer agent only to read its required methodology "
    "and the plugin's review-code/SKILL.md, without reviewing subject files. "
    "Give it the selected plugin root and have it identify the instruction paths it read. "
    "Do not access anything outside this workspace or the selected plugin."
)


def configure():
    frozen = driver.configure(HERE / "declaration.json")
    driver.controller.DEPENDENCIES.append(Path(__file__))
    return frozen


def job_for(frozen, side, case, repetition, binding=False):
    name = f"binding-{side}" if binding else f"claude-{side}-{case}-isolated-{repetition}"
    return argparse.Namespace(provider="claude", side=side, case=case,
        mode="isolated", repetition=repetition, binding=binding,
        snapshot=driver.controller.SNAPSHOTS[side], frozen=frozen,
        workspace=WORKSPACES / name,
        evidence=HERE / name if binding else HERE / "runs" / name)


def jobs_for(frozen):
    return [job_for(frozen, side, case, repetition)
            for case in CASES for side in ("baseline", "candidate")
            for repetition in (1, 2)]


def prepare(job):
    driver.prepare_job(job)
    if job.binding:
        seed = driver.controller.seed
        launch_path = job.evidence / "launch.json"
        launch = json.loads(launch_path.read_text())
        launch["prompt"] = BINDING_PROMPT
        seed.write_json(launch_path, launch)
        prompt_path = job.evidence / "prompt.txt"
        prompt_path.write_text(BINDING_PROMPT + "\n")
        prepared_path = job.evidence / "prepared.json"
        prepared = json.loads(prepared_path.read_text())
        prepared.update(launch_sha256=seed.sha(launch_path.read_bytes()),
                        prompt_sha256=seed.sha(prompt_path.read_bytes()))
        seed.write_json(prepared_path, prepared)


def capture(job, interruption):
    print(json.dumps({"starting": job.evidence.name}), flush=True)
    driver.capture_job(job, interruption)
    print(json.dumps({"finished": job.evidence.name,
                      "status": runtime.completion_status(job.evidence)}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("freeze", "binding", "batch", "grade", "list"))
    parser.add_argument("--side", choices=("baseline", "candidate"))
    args = parser.parse_args()
    if args.operation == "binding" and not args.side:
        parser.error("binding requires --side")
    if args.operation != "binding" and args.side:
        parser.error("--side is only valid for binding")
    frozen = configure()
    if args.operation == "freeze":
        driver.controller.freeze(frozen)
    elif args.operation == "binding":
        return runtime.run_batch([job_for(frozen, args.side, "R3", 0, binding=True)],
                                 prepare, capture)
    elif args.operation == "batch":
        return runtime.run_batch(jobs_for(frozen), prepare, capture)
    elif args.operation == "grade":
        from prepare_grades import prepare as prepare_grade
        for job in jobs_for(frozen):
            prepare_grade(job.evidence, HERE / "grading" / job.evidence.name, frozen)
    else:
        print(json.dumps([job.evidence.name for job in jobs_for(frozen)], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
