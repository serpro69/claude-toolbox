"""Freeze the authorized revision-2 metadata and capture/grading identities.

Refuses existing outputs and validates original bytes from the immutable Git
revision before creating a successor freeze. Run only before measured captures.
"""
import argparse
import json
import platform
import shutil
import subprocess
from pathlib import Path

import controller


HERE = Path(__file__).resolve().parent
V = HERE.parent
ROOT = controller.ROOT
ORIGINAL = "1c67e55b"
CASES = {case: (skill, name) for case, (skill, name, _) in controller.seed.SEEDS.items()}


def sha(path):
    return controller.seed.sha(path.read_bytes())


def main(refresh=False):
    outputs = [V / "task2-frozen-v2.json", HERE / "assertion-mapping.json",
               HERE / "grading-pin.json", HERE / "grader.md"]
    if any(path.exists() for path in outputs) and not refresh:
        raise FileExistsError("Refuse to overwrite an existing revision-2 freeze")
    if refresh and (not all(path.is_file() for path in outputs) or list(HERE.glob("codex-*/command.json"))):
        raise ValueError("Preflight refresh requires complete prior outputs and no measured attempts")
    original_revision = subprocess.check_output(["git", "rev-parse", ORIGINAL], cwd=ROOT, text=True).strip()
    original = json.loads((V / "task2-frozen.json").read_bytes())
    updated = dict(original)
    updated["original_runtime_declaration"] = updated.pop("runtimes")
    updated["fixtures"] = {}
    mapping, unchanged_subjects, unchanged_files = [], 0, 0
    for case, (skill, name) in CASES.items():
        relative = Path("klaude-plugin/skills") / skill / "evals" / name
        folder = ROOT / relative
        current = controller.seed.files(folder)
        if set(current) != set(original["fixtures"][case]):
            raise ValueError("Seed inventory changed: " + case)
        updated["fixtures"][case] = current
        for name, expected in original["fixtures"][case].items():
            old_bytes = subprocess.check_output(["git", "show", original_revision + ":" + (relative / name).as_posix()], cwd=ROOT)
            if controller.seed.sha(old_bytes) != expected:
                raise ValueError("Original Git bytes do not match revision-1 freeze")
            if current[name] == expected:
                unchanged_files += 1
            elif case not in {"R3", "I2"} or name not in {"eval.json", "oracle/expected-results.json"}:
                raise ValueError("Unauthorized fixture delta: " + str(relative / name))
            if name.startswith("test-files/"):
                if current[name] != expected:
                    raise ValueError("Subject bytes changed")
                unchanged_subjects += 1
            if name == "eval.json":
                old = json.loads(old_bytes)
                new = json.loads((folder / name).read_bytes())
                if {k: v for k, v in old.items() if k != "assertions"} != {k: v for k, v in new.items() if k != "assertions"}:
                    raise ValueError("Prompt or non-assertion metadata changed")
                if len(old["assertions"]) != len(new["assertions"]):
                    raise ValueError("Assertion count changed")
                for before, after in zip(old["assertions"], new["assertions"]):
                    if before != after:
                        if (case, before["id"]) not in {("R3", "7.5"), ("R3", "7.6"), ("I2", "9.5")} or before["id"] != after["id"]:
                            raise ValueError("Unexpected assertion change")
                        mapping.append({"case": case, "skill": skill, "eval": relative.name,
                                        "id": before["id"], "revision_1": before["text"], "revision_2": after["text"]})
    if len(mapping) != 3:
        raise ValueError("Expected three explicit assertion changes")
    current_version = subprocess.check_output(["codex", "--version"], text=True).strip()
    if current_version != "codex-cli 0.162.1":
        raise ValueError("Runtime differs from declared version")
    updated.update(revision=2, rubric_sha256=sha(V / "task2-rubric-v2.md"),
        original_freeze_sha256=sha(V / "task2-frozen.json"), original_assertion_revision=original_revision,
        controller_sha256=sha(HERE / "controller.py"), freeze_tool_sha256=sha(Path(__file__)),
        run_contract_sha256=sha(HERE / "run-contract.md"),
        retained_helper_hashes={name: sha(V / name) for name in ("capture-seeds.py", "capture-codex.py", "probe_state.py", "prepare-bundles.py")},
        runtime={"codex": current_version, "controller_python": platform.python_version(),
                 "platform": platform.system(), "capy": subprocess.check_output(["capy", "--version"], text=True).strip()},
        evidence_contract="receipt/use for R3 7.5/7.6 and I2 9.5; exact prompt text unverified",
        unchanged_subject_files=unchanged_subjects, unchanged_revision_1_files=unchanged_files,
        configuration= {"actor": "gpt-6-astra/xhigh", "named_reviewer": "gpt-6.1-sol/xhigh",
                        "pal": "gemini-3.1-pro-preview/max", "approval": "never", "sandbox": "workspace-write",
                        "history": "paginated", "marketplace": controller.MARKETPLACE},
        schema_hashes={name: sha(Path("/tmp/functional-review-2b-schema-01621/v2") / name)
            for name in ("ThreadStartParams.json", "ThreadItemsListResponse.json", "ThreadReadParams.json",
                         "SkillsListParams.json", "PluginInstallParams.json", "PluginUninstallParams.json")})
    updated["concrete_grader"] = "task2b/grading-pin.json"
    grader = ROOT / "klaude-plugin/agents/eval-grader.md"
    pin = {"grader_sha256": sha(grader), "rubric_version": 2,
           "rubric_sha256": updated["rubric_sha256"], "actor_baseline": controller.seed.BASELINE,
           "runtime": "fresh eval-grader role, declared gpt-6.1-sol/xhigh; exact service telemetry not independently exposed",
           "read_adapter": "native read-equivalent cat/sed of exact manifest-listed files only; no code execution or live fixture access",
           "limits": "instruction and manifest boundary; no OS-wide confinement claim",
           "consistency": "Use this pin for both comparison sides; regrade both if it changes."}
    mapping_record = {"original_revision": original_revision,
                      "original_freeze_sha256": updated["original_freeze_sha256"], "changes": mapping}
    if refresh:
        if (json.loads(outputs[1].read_bytes()) != mapping_record
                or json.loads(outputs[2].read_bytes()) != pin or sha(outputs[3]) != sha(grader)):
            raise ValueError("Preflight refresh may not silently change assertion/grader identity")
        archive = HERE / "preflight-freezes" / (sha(outputs[0]) + ".json")
        controller.write_json(archive, json.loads(outputs[0].read_bytes()))
        pending = outputs[0].with_suffix(".pending.json")
        controller.write_json(pending, updated)
        pending.replace(outputs[0])
    else:
        controller.write_json(outputs[1], mapping_record)
        shutil.copyfile(grader, outputs[3])
        controller.write_json(outputs[2], pin)
        controller.write_json(outputs[0], updated)
    print(json.dumps({"freeze": str(V / "task2-frozen-v2.json"), "sha256": sha(V / "task2-frozen-v2.json"),
                      "unchanged_subjects": unchanged_subjects, "changed_metadata_files": 51 - unchanged_files,
                      "grader_sha256": pin["grader_sha256"]}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-preflight", action="store_true")
    main(parser.parse_args().refresh_preflight)
