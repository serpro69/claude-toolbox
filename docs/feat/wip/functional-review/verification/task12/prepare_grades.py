"""Seal matrix grading inputs after capture; never repair or reinterpret events."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil

import controller

spec = importlib.util.spec_from_file_location("task8_grading", controller.VERIFICATION / "task8/prepare_grading.py")
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)


def prepare(source, destination, frozen):
    inputs = controller.verify_frozen(frozen)
    if destination.exists():
        raise FileExistsError(destination)
    seal = json.loads((source / "manifest.json").read_bytes())
    for relative, digest in seal.items():
        previous.checked_file(source, relative, digest)
    launch = json.loads(previous.checked_file(source, "launch.json", seal["launch.json"]).read_bytes())
    workspace = Path(launch["workspace"]).resolve()
    for boundary in (workspace, source.resolve()):
        if destination == boundary or destination.is_relative_to(boundary) or boundary.is_relative_to(destination):
            raise ValueError("Grading destination must be disjoint from actor and original evidence")
    if launch["purpose"] != "measured workflow" or launch["fixture_manifest_sha256"] != previous.digest(frozen):
        raise ValueError("Not a measured run under this freeze")
    case, provider = launch["case"], launch["provider"]
    skill, name, _ = controller.CASES[case]
    fixture = controller.seed.fixture(case)
    events = previous.observable_events(source, provider, seal)
    destination.mkdir(parents=True, exist_ok=False)
    for relative in seal:
        target = destination / "captured" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / relative, target)
    shutil.copyfile(source / "manifest.json", destination / "original-manifest.json")
    shutil.copyfile(controller.GRADER, destination / "grader.md")
    shutil.copyfile(controller.RUBRIC, destination / "rubric.md")
    assertions = json.loads((fixture / "eval.json").read_bytes())["assertions"]
    controller.seed.write_json(destination / "assertions.json", assertions)
    for relative, digest in inputs["fixtures"][case].items():
        if relative.startswith("oracle/"):
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(previous.checked_file(fixture, relative, digest), target)
    index = []
    for number, event in enumerate(events, 1):
        relative = f"events/{number:04d}.json"
        controller.seed.write_json(destination / relative, event)
        block = event.get("item", event.get("block", {}))
        index.append({"id": event["id"], "actor": event.get("actor"),
                      "type": block.get("type"), "tool": block.get("name", block.get("tool")),
                      "artifact": relative})
    controller.seed.write_json(destination / "event-index.json", index)
    (destination / "events.txt").write_text("\n\n".join(
        "EVENT " + event["id"] + "\n" + json.dumps(event, indent=2) for event in events) + "\n")
    controller.seed.write_json(destination / "captured-path-map.json", {p: "captured/" + p for p in seal})
    files = [{"path": str(p.relative_to(destination)), "sha256": previous.digest(p), "role": p.name}
             for p in sorted(destination.rglob("*")) if p.is_file()]
    manifest = {
        "run": {"id": source.name, "skill": skill, "eval": name, "case": case,
                "provider": provider, "mode": launch["mode"], "side": launch["side"]},
        "identity": {"actor": launch["actor"], "grader": inputs["grader_sha256"],
                     "rubric": inputs["rubric_sha256"], "rubric_version": 2,
                     "fixture_freeze": previous.digest(frozen), "adapter": previous.digest(Path(__file__))},
        "evidence_root": ".", "files": files,
        "original_manifest_sha256": previous.digest(source / "manifest.json"),
        "completeness": {
            "events": "all retained observable events; inspect actual results for missing/truncated evidence",
            "ordering": "original sequence and actual parent-child edges; no total order across actors",
            "dispatches": "actual calls retained; receipt/use applies only to selected R3/I2 assertions",
            "user_decisions": "ordinary prompt only; no controller requirement waivers",
            "snapshots": "initial/final tracked and unignored subject files; ignored runtime files excluded",
        },
        "actor_grading_material_access": "requires event audit; no OS-wide read confinement",
        "exact_submitted_prompt_parity": "unverified",
        "redactions": ["original private reasoning excluded and configured credentials redacted; no invented events"],
        "integrity": "all original capture hashes and derived listed files verified by controller",
    }
    controller.seed.write_new_json(destination / "manifest.json", manifest)
    for entry in files:
        previous.checked_file(destination, entry["path"], entry["sha256"])
    print(json.dumps({"run": source.name, "events": len(events), "files": len(files),
                      "manifest_sha256": previous.digest(destination / "manifest.json")}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("freeze", type=Path)
    args = parser.parse_args()
    prepare(args.source.resolve(), args.destination.resolve(), args.freeze.resolve())
