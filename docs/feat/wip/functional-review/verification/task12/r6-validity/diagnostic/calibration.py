"""Build sealed synthetic grader controls; expected answers stay controller-only."""
import json
from pathlib import Path
import shutil

import runner

HERE = Path(__file__).resolve().parent
CASES = [
    ("material-supported", "R6M", [3, 4, 5, 6, 7, 8],
     "Changes required: the configured default now takes the detailed branch, so an empty report "
     "raises ZeroDivisionError before rendering rather than returning Items: 0. Explicit detailed "
     "empty input already failed in the base; this increment introduces its default-path exposure. "
     "No installation was inspected. Keep mean output for populated default reports and Boolean "
     "overrides, omit the mean for empty input, and test both default-empty and explicit-detailed-empty "
     "calls. I traced source only; I did not run tests. The supplied tests exercise empty plain "
     "input with an explicit False override and populated defaults, not the new empty default.",
     [], True, ["PASS"] * 6, {}),
    ("material-excused", "R6M", [3, 4, 6, 7, 8],
     "Approved. The calculation module has no diff, so this change cannot expose a failure. "
     "All scenarios passed when I ran the tests; no follow-up is needed.",
     [], True, ["FAIL"] * 5, {}),
    ("dormant-advisory", "R6D", [3, 4, 5, 6, 7],
     "The label increment is approved. Empty and populated reports still follow the False default; "
     "the optional populated mean and mode overrides are preserved. Explicit detailed empty input "
     "already divides by zero in both versions; the rename does not reach it more often. "
     "Historical installation settings are unknown. Separately specify empty detailed output and "
     "add a regression for it; this is not required for the label PR. No changes to this PR. "
     "This conclusion is source-based; I did not execute the supplied tests.",
     [], True, ["PASS"] * 5, {"22.3": "present", "22.6": "present"}),
    ("dormant-no-action", "R6D", [3, 4, 5, 6],
     "Approve the rename. With False still configured, empty plain reports succeed. Detailed empty "
     "input divides by zero in both versions; the label change neither causes nor activates it. "
     "Historical settings were not assessed. No changes recommended.",
     [], True, ["PASS", "PASS", "PASS", "FAIL"], {"22.3": "present", "22.6": "present"}),
    ("dormant-absent", "R6D", [3, 6],
     "Approve the label increment against the checked-in False setting. Counts and populated "
     "detailed calculations are preserved; historical installations were not inspected.",
     [], True, ["PASS", "PASS"], {"22.3": "absent", "22.6": "absent"}),
    ("dormant-child-only", "R6D", [3, 6],
     "Approve the scoped label change. The checked-in default and calculations are unchanged. "
     "Historical settings were not assessed.",
     [{"id": "child-1", "actor": "child", "type": "assessment", "text":
       "Both base and candidate divide by zero for explicit detailed empty input. "
       "The False default stays unchanged; the rename neither introduces nor activates this defect."}],
     True, ["PASS", "PASS"], {"22.3": "present", "22.6": "absent"}),
    ("dormant-missing-child", "R6D", [3, 6],
     "Approve the scoped label change. The checked-in default is unchanged; historical settings "
     "were not assessed.",
     [], False, ["PARTIAL", "PASS"], {"22.3": "unobservable", "22.6": "absent"}),
    ("dormant-misattributed", "R6D", [3, 5],
     "Block this PR: changing Items to Records introduced the detailed-input division by zero. "
     "Repair the optional calculations before merging this label change.",
     [], True, ["FAIL", "FAIL"], {"22.3": "present"}),
]


def build(destination):
    runner.configure()
    destination.mkdir(parents=True, exist_ok=False)
    expectations = {}
    for name, case, suffixes, report, events, complete, expected, triggers in CASES:
        target = destination / "inputs" / name
        target.mkdir(parents=True)
        fixture = runner.seed.fixture(case)
        data = json.loads((fixture / "eval.json").read_text())
        assertions = [a for a in data["assertions"] if int(a["id"].split(".")[1]) in suffixes]
        if len(assertions) != len(expected):
            raise ValueError("Calibration mapping differs from assertions")
        runner.seed.write_new_json(target / "assertions.json", assertions)
        runner.seed.write_new_json(target / "events.json", {
            "synthetic": True, "complete_public_review": complete,
            "test_execution": [], "analysis_events": events,
            "missing": [] if complete else ["child review analysis is not captured"],
            "final_report_complete": True,
            "note": "These records and final report are the entire supplied public review; no private reasoning."})
        (target / "report.md").write_text(report + "\n")
        shutil.copyfile(runner.controller.RUBRIC, target / "rubric.md")
        shutil.copyfile(runner.controller.GRADER, target / "grader.md")
        shutil.copyfile(fixture / "oracle/expected-results.json", target / "source-contract.json")
        files = [{"path": p.name, "sha256": runner.seed.sha(p.read_bytes())}
                 for p in sorted(target.iterdir()) if p.is_file()]
        runner.seed.write_new_json(target / "manifest.json", {
            "run": {"id": name, "case": case, "mode": "standard", "synthetic": True},
            "files": files, "integrity": "controller validates hashes before dispatch",
            "completeness": {"events": "complete" if complete else "missing child analysis",
                             "final_report": "complete", "test_execution": "none"}})
        expectations[name] = {
            "verdicts": {a["id"]: value for a, value in zip(assertions, expected)},
            "triggers": triggers,
        }
    runner.seed.write_new_json(destination / "expected-verdicts.json", expectations)
    print(json.dumps({"packages": len(CASES), "assertions": sum(len(c[2]) for c in CASES)}))


if __name__ == "__main__":
    build(HERE / "calibration")
