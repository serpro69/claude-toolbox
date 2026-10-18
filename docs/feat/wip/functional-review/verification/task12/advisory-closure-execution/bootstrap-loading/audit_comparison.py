"""Read-only reconciliation of the completed comparison; no actor or grading writes."""
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

import listing_guard

s = listing_guard.successor
HERE = s.HERE


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def main():
    listing_guard.Adapter().preflight()
    matrix = read(HERE / "../../advisory-closure/matrix.json")
    plan = read(HERE / "grading-dispatch/plan.json")
    jobs = matrix["jobs"]
    reassessments = HERE / "grading-reassessments"
    require({p.stem for p in reassessments.glob("*.json")} ==
            {p.stem for p in reassessments.glob("*.md")}, "Incomplete reassessment request/return pair")
    for response in reassessments.glob("*.md"):
        match = re.fullmatch(r"(\d{2})-(\d+\.\d+)", response.stem)
        require(match is not None and 1 <= int(match[1]) <= 64,
                "Reassessment outside the declared matrix")
    require(len(jobs) == len(plan) == 64, "Audit check failed: len(jobs) == len(plan) == 64")
    require({p.name for p in (HERE / "runs").iterdir()} == {j["id"] for j in jobs}, "Audit check failed: {p.name for p in (HERE / \"runs\").iterdir()} == {j[\"id\"] for j in jobs}")
    require(len(list((HERE / "grading-returns").glob("*.md"))) == 64, "Audit check failed: len(list((HERE / \"grading-returns\").glob(\"*.md\"))) == 64")
    rows, agents, corrections, access_flags = [], set(), [], []
    counts = Counter()
    original = defaultdict(Counter)
    effective = defaultdict(Counter)
    case_original = defaultdict(lambda: defaultdict(Counter))
    case_effective = defaultdict(lambda: defaultdict(Counter))
    access_needles = [
        "/home/sergio/Projects/personal/claude-toolbox",
        "fr-advisory-execution-inputs-20261017",
        "grading-dispatch", "grading-returns", "oracle/expected",
    ]
    for sequence, job in enumerate(jobs, 1):
        name = job["id"]
        planned = plan[name]
        require(planned["sequence"] == sequence, "Audit check failed: planned[\"sequence\"] == sequence")
        run = HERE / "runs" / name
        packet = HERE / "grading" / name
        capture_manifest = read(run / "manifest.json")
        s.runner.checked_files(run, capture_manifest)
        completion, launch = read(run / "completion.json"), read(run / "launch.json")
        require(completion["exit_code"] == 0, "Audit check failed: completion[\"exit_code\"] == 0")
        require(not completion.get("timed_out") and not completion.get("interrupted_by"), "Audit check failed: not completion.get(\"timed_out\") and not completion.get(\"interrupted_by\")")
        require(completion["final_files"] == launch["initial_files"], "Audit check failed: completion[\"final_files\"] == launch[\"initial_files\"]")
        require((run / "initial.patch").read_bytes() == (run / "final.patch").read_bytes(), "Audit check failed: (run / \"initial.patch\").read_bytes() == (run / \"final.patch\").read_bytes()")
        require(launch["actor"]["revision"] == job["actor_revision"], "Audit check failed: launch[\"actor\"][\"revision\"] == job[\"actor_revision\"]")
        require(launch["fixture_manifest_sha256"] == sha(s.host.FROZEN), "Audit check failed: launch[\"fixture_manifest_sha256\"] == sha(s.host.FROZEN)")
        require(launch["initial_knowledge"] == "empty; database absent", "Audit check failed: launch[\"initial_knowledge\"] == \"empty; database absent\"")
        manifest = read(packet / "manifest.json")
        s.runner.checked_files(packet, {v["path"]: v["sha256"] for v in manifest["files"]})
        require(manifest["original_manifest_sha256"] == sha(run / "manifest.json"), "Audit check failed: manifest[\"original_manifest_sha256\"] == sha(run / \"manifest.json\")")
        actual = read(HERE / "grading-dispatch" / f"actual-{sequence:02}.json")
        require(actual["run"] == name and actual["sequence"] == sequence, "Audit check failed: actual[\"run\"] == name and actual[\"sequence\"] == sequence")
        require(actual["manifest_sha256"] == sha(packet / "manifest.json"), "Audit check failed: actual[\"manifest_sha256\"] == sha(packet / \"manifest.json\")")
        require(actual["controller_sha256"] == sha(HERE / "grading-dispatch" / f"{sequence:02}.md"), "Audit check failed: actual[\"controller_sha256\"] == sha(HERE / \"grading-dispatch\" / f\"{sequence:02}.md\")")
        require(actual["prompt_sha256"] == hashlib.sha256(actual["request"]["message"].encode()).hexdigest(), "Audit check failed: actual[\"prompt_sha256\"] == hashlib.sha256(actual[\"request\"][\"message\"].encode()).hexdigest()")
        require(actual["role_configuration"] == planned["role_configuration"], "Audit check failed: actual[\"role_configuration\"] == planned[\"role_configuration\"]")
        require(actual["grader_sha256"] == planned["grader_sha256"] == sha(packet / "grader.md"), "Audit check failed: actual[\"grader_sha256\"] == planned[\"grader_sha256\"] == sha(packet / \"grader.md\")")
        require(actual["execution_freeze_sha256"] == sha(s.host.FROZEN), "Audit check failed: actual[\"execution_freeze_sha256\"] == sha(s.host.FROZEN)")
        require(actual["agent_id"] not in agents, "Audit check failed: actual[\"agent_id\"] not in agents")
        agents.add(actual["agent_id"])
        if sequence == 56:
            require(actual["planned_request"] == planned["request"], "Audit check failed: actual[\"planned_request\"] == planned[\"request\"]")
            expected = dict(planned["request"])
            expected["message"] = expected["message"].replace("/verification/task12/", "/task12/")
            require(actual["request"] == expected, "Audit check failed: actual[\"request\"] == expected")
            correction = actual["dispatch_correction"]
            require(correction["sha256"] == hashlib.sha256(correction["message"].encode()).hexdigest(), "Audit check failed: correction[\"sha256\"] == hashlib.sha256(correction[\"message\"].encode()).hexdigest()")
            require(str(HERE / "grading-dispatch/56.md") in correction["message"], "Audit check failed: str(HERE / \"grading-dispatch/56.md\") in correction[\"message\"]")
            corrections.append({"sequence": 56, "type": "controller locator",
                                "record": "grading-dispatch/actual-56.json"})
        else:
            require(actual["request"] == planned["request"], "Audit check failed: actual[\"request\"] == planned[\"request\"]")
        grade_path = HERE / "grading-returns" / f"{sequence:02}.md"
        grade = grade_path.read_text()
        parsed = re.findall(r"^\|\s*(\d+\.\d+)\s*\|\s*(PASS|FAIL|PARTIAL)\s*\|", grade, re.M)
        assertions = read(packet / "assertions.json")
        require(len(parsed) == len(assertions), "Audit check failed: len(parsed) == len(assertions)")
        require(sorted(k for k, _ in parsed) == sorted(v["id"] for v in assertions), "Audit check failed: sorted(k for k, _ in parsed) == sorted(v[\"id\"] for v in assertions)")
        verdicts = dict(parsed)
        revised = dict(verdicts)
        for reassessment in sorted((HERE / "grading-reassessments").glob(f"{sequence:02}-*.md")):
            assertion_id = reassessment.stem.split("-", 1)[1]
            require(assertion_id in verdicts, "Unknown reassessed assertion")
            request_path = reassessment.with_suffix(".json")
            request = read(request_path)
            require(request["assertion"] == assertion_id and request.get("sequence", sequence) == sequence,
                    "Reassessment sequence/assertion mismatch")
            require(request["run"] == name, "Reassessment names a different packet")
            require(request["manifest_sha256"] == actual["manifest_sha256"], "Reassessment packet changed")
            require(request.get("grader", request.get("agent_id")) == actual["agent_id"],
                    "Reassessment was not returned by the original grader")
            require(request["original_return"] == str(grade_path.relative_to(HERE)),
                    "Reassessment original-return reference differs")
            matching = [line for line in reassessment.read_text().splitlines()
                        if line.startswith("| " + assertion_id + " |")]
            require(len(matching) == 1, "Expected one reassessed assertion row")
            cells = [c.strip() for c in matching[0].split("|")[2:-1]]
            decisions = [c for c in cells if c in ("PASS", "FAIL", "PARTIAL")]
            require(len(decisions) in (1, 2), "Expected effective verdict with optional original verdict")
            if len(decisions) == 2:
                require(decisions[0] == verdicts[assertion_id], "Reassessment misstates original grade")
            revised[assertion_id] = decisions[-1]
            corrections.append({"sequence": sequence, "run": name, "assertion": assertion_id,
                                "grader": actual["agent_id"], "manifest_sha256": actual["manifest_sha256"],
                                "original": verdicts[assertion_id], "effective": decisions[-1],
                                "record": str(reassessment.relative_to(HERE)),
                                "sha256": sha(reassessment), "request_sha256": sha(request_path)})
        for version, totals, cases in [(verdicts, original, case_original),
                                      (revised, effective, case_effective)]:
            totals[job["side"]].update(version.values())
            cases[job["case"]][job["side"]].update(version.values())
        trigger = None
        if job["case"] == "R6D":
            trigger_rows = [line for line in grade.splitlines()
                            if re.match(r"^\|\s*22\.6\s*\|", line)]
            triggers = set(re.findall(r"trigger\s*=\s*(present|absent|unobservable)",
                                     "\n".join(trigger_rows), re.I))
            require(len(triggers) == 1, "Audit check failed: len(triggers) == 1")
            trigger = next(iter(triggers))
        for entry in read(packet / "event-index.json"):
            event = read(packet / entry["artifact"])
            item, block = event.get("item", {}), event.get("block", {})
            inspected = None
            if item.get("type") == "commandExecution":
                counts["shell_commands"] += 1
                inspected = item.get("command") or ""
            elif block.get("type") == "tool_use":
                tool, args = block.get("name", ""), block.get("input", {})
                if tool == "Bash":
                    counts["shell_commands"] += 1
                    inspected = args.get("command", "")
                elif tool in ("Read", "Glob", "Grep"):
                    counts["direct_file_search_calls"] += 1
                    inspected = json.dumps(args)
                elif tool.startswith("mcp__capy__"):
                    counts["capy_calls"] += 1
                    inspected = json.dumps(args)
                if tool.startswith("mcp__pal__"):
                    counts["pal_calls"] += 1
            elif item.get("type") == "mcpToolCall":
                if item.get("server") == "pal":
                    counts["pal_calls"] += 1
                elif item.get("server") == "capy":
                    counts["capy_calls"] += 1
                    inspected = json.dumps(item.get("arguments"))
            if inspected:
                matches = [needle for needle in access_needles if needle in inspected]
                if matches:
                    access_flags.append({"run": name, "event": entry["artifact"], "matches": matches})
        rows.append({**job, "sequence": sequence, "original": verdicts, "effective": revised,
                     "final_advisory_trigger": trigger, "grade_sha256": sha(grade_path),
                     "capture_manifest_sha256": sha(run / "manifest.json"),
                     "grading_manifest_sha256": sha(packet / "manifest.json"),
                     "actual_dispatch_sha256": sha(HERE / "grading-dispatch" / f"actual-{sequence:02}.json")})
    require(sum(sum(x.values()) for x in original.values()) == 464, "Audit check failed: sum(sum(x.values()) for x in original.values()) == 464")
    require(all(sum(x.values()) == 232 for x in original.values()), "Audit check failed: all(sum(x.values()) == 232 for x in original.values())")
    require(counts["pal_calls"] == 0, "Audit check failed: counts[\"pal_calls\"] == 0")
    print(json.dumps({
        "captures": len(rows), "original_assertion_rows": 464, "fresh_grader_identities": len(agents),
        "original_totals": original, "effective_totals": effective,
        "original_case_totals": case_original, "effective_case_totals": case_effective,
        "integrity": {"all_capture_and_grading_seals_verified": True,
                      "subjects_unchanged": True, "source_and_execution_identities_verified": True,
                      "empty_initial_knowledge_declared_in_all_launches": True,
                      "actual_grader_requests_and_roles_verified": True},
        "access_screen": {"counts": counts, "literal_needles": access_needles, "flags": access_flags,
                          "limits": "Visible command/file/search/Capy arguments only; no shell interpretation or OS-wide confinement proof."},
        "corrections": corrections, "runs": rows,
        "audit_tool_sha256": sha(Path(__file__)),
    }, indent=2))


if __name__ == "__main__":
    main()

