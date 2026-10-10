"""Create sealed revision-2 grader inputs from retained or new baseline captures.

No actors run here. Original seals are validated and never changed. The grader
gets copied evidence, current assertions and the selected rubric, not live files.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil

import controller


HERE = Path(__file__).resolve().parent
V = HERE.parent
ROOT = controller.ROOT
spec = importlib.util.spec_from_file_location("grade_adapter_v1", V / "task8/prepare_grading.py")
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)


def prepare(source, destination, case, provider, repetition):
    if destination.exists():
        raise FileExistsError(destination)
    frozen = controller.verify_v2(V / "task2-frozen-v2.json")
    seal = json.loads((source / "manifest.json").read_bytes())
    for relative, digest in seal.items():
        previous.checked_file(source, relative, digest)
    events = previous.observable_events(source, provider, seal)
    skill, name, _ = controller.seed.SEEDS[case]
    fixture = controller.seed.fixture(case)
    meta = json.loads((fixture / "eval.json").read_bytes())
    destination.mkdir(parents=True)
    for relative in seal:
        target = destination / "captured" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / relative, target)
    shutil.copyfile(source / "manifest.json", destination / "original-manifest.json")
    shutil.copyfile(HERE / "grader.md", destination / "grader.md")
    shutil.copyfile(V / "task2-rubric-v2.md", destination / "rubric.md")
    shutil.copyfile(fixture / "oracle/expected-results.json", destination / "expected-results.json")
    controller.write_json(destination / "assertions.json", meta["assertions"])
    index = []
    for number, event in enumerate(events, 1):
        relative = f"events/{number:04d}.json"
        controller.write_json(destination / relative, event)
        value = event.get("item", event.get("block", {}))
        tool = value.get("name", value.get("tool", value.get("type", "")))
        command = value.get("command", "")
        index.append({"event": event["id"], "actor": event.get("actor"),
                      "type": value.get("type"), "tool": tool,
                      "command_preview": command[:240], "artifact": relative})
    controller.write_json(destination / "event-index.json", index)
    (destination / "events.txt").write_text("\n\n".join(
        "EVENT " + event["id"] + "\n" + json.dumps(event, indent=2) for event in events) + "\n")
    # Paths in captured payload-event records are relative to the original run;
    # their exact copies now live beneath captured/. Preserve both mappings.
    mapping = {relative: "captured/" + relative for relative in seal}
    controller.write_json(destination / "captured-path-map.json", mapping)
    launch = json.loads((source / "launch.json").read_bytes())
    files = [{"path": str(p.relative_to(destination)), "sha256": previous.digest(p), "role": p.name}
             for p in sorted(destination.rglob("*")) if p.is_file()]
    manifest = {"run": {"id": source.name, "skill": skill, "eval": name, "case": case,
                "provider": provider, "mode": "isolated" if case == "R3" else "standalone", "repetition": repetition},
        "identity": {"actor": controller.seed.BASELINE, "grader": previous.digest(HERE / "grader.md"),
                     "rubric": previous.digest(V / "task2-rubric-v2.md"), "rubric_version": 2,
                     "fixture_manifest": previous.digest(V / "task2-frozen-v2.json"),
                     "adapter_sha256": previous.digest(Path(__file__)),
                     "original_launch_fixture_manifest": launch.get("fixture_manifest_sha256")},
        "evidence_root": ".", "files": files,
        "completeness": {"events": "all public per-actor items/blocks from the validated original seal; inspect actual returned content for gaps/truncation",
            "ordering": "original sequence/timestamps preserved; index file order is not a total order between actors",
            "dispatches": "receipt/use selected for changed R3/I2 assertions; exact child prompt content unverified",
            "snapshots": "copied sealed initial/final subject files", "user_decisions": "ordinary prompt only; no supplemental waiver supplied"},
        "original_manifest_sha256": previous.digest(source / "manifest.json"),
        "integrity": "controller validated every original and derived listed file hash",
        "actor_grading_material_access": "requires read audit; no OS-wide confinement claim",
        "redactions": ["original sanitizer excludes private reasoning and configured credential values; no invented receipt events"],
        "exact_submitted_prompt_content": "unverified", "initial_knowledge": launch.get("initial_knowledge")}
    controller.write_json(destination / "manifest.json", manifest)
    for entry in files:
        previous.checked_file(destination, entry["path"], entry["sha256"])
    print(json.dumps({"run": source.name, "manifest": str(destination / "manifest.json"),
                      "sha256": previous.digest(destination / "manifest.json"), "events": len(events), "files": len(files)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--case", choices=("R3", "I2"), required=True)
    parser.add_argument("--provider", choices=("claude", "codex"), required=True)
    parser.add_argument("--repetition", type=int, choices=(1, 2), required=True)
    args = parser.parse_args()
    prepare(args.source.resolve(), args.destination.resolve(), args.case, args.provider, args.repetition)
