"""Offline R6M/R6D checks; controller-only, never stage with actor inputs."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[7]
EVALS = REPO / "klaude-plugin/skills/review-code/evals"
CASES = {
    "functional-inherited-defect-exposed": (21, {"config.py", "tests/test_report.py"}),
    "functional-inherited-defect-dormant": (22, {"formatting.py", "tests/test_report.py"}),
}
PROBE = """
import json
from app import report
from stats import summarize

def observe(call):
    try:
        return {"value": call()}
    except ZeroDivisionError:
        return {"error": "ZeroDivisionError"}

print(json.dumps({
    "default_empty": observe(lambda: report([])),
    "default_populated": observe(lambda: report([2, 4])),
    "plain_empty": observe(lambda: report([], detailed=False)),
    "plain_populated": observe(lambda: report([2, 4], detailed=False)),
    "detailed_empty": observe(lambda: report([], detailed=True)),
    "detailed_populated": observe(lambda: report([2, 4], detailed=True)),
    "calculation_empty": observe(lambda: summarize([], detailed=True)),
    "calculation_populated": observe(lambda: summarize([2, 4], detailed=True)),
}))
"""


def run(*args, cwd):
    env = {key: value for key, value in os.environ.items()
           if not key.startswith(("PYTHON", "GIT_"))}
    env.update(PYTHONDONTWRITEBYTECODE="1", GIT_CONFIG_NOSYSTEM="1",
               GIT_CONFIG_GLOBAL=os.devnull)
    return subprocess.run(args, cwd=cwd, env=env, text=True, check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def tree(path):
    return {p.relative_to(path).as_posix(): p.read_bytes()
            for p in path.rglob("*") if p.is_file()}


class FixtureTests(unittest.TestCase):
    def test_case_identity_and_complete_actor_manifests(self):
        all_ids = [json.loads(p.read_text())["id"] for p in EVALS.glob("*/eval.json")]
        for name, (number, _) in CASES.items():
            with self.subTest(case=name):
                case = EVALS / name
                data = json.loads((case / "eval.json").read_text())
                self.assertEqual(all_ids.count(number), 1)
                self.assertEqual(data["id"], number)
                self.assertEqual(data["name"], name)
                self.assertEqual(len(data["files"]), len(set(data["files"])))
                self.assertEqual(set(data["files"]), {
                    "test-files/" + p for p in tree(case / "test-files")})
                self.assertEqual([a["id"] for a in data["assertions"]],
                                 [f"{number}.{i}" for i in range(1, len(data["assertions"]) + 1)])
                self.assertTrue((case / "oracle/expected-results.json").is_file())
                for path in data["files"]:
                    self.assertNotIn("oracle", Path(path).parts)
                    self.assertNotIn("eval.json", Path(path).parts)

    def test_only_intended_increment_changes(self):
        for name, (_, expected_changes) in CASES.items():
            with self.subTest(case=name):
                case = EVALS / name / "test-files"
                before, after = tree(case / "before"), tree(case / "after")
                self.assertEqual(before.keys(), after.keys())
                self.assertEqual({p for p in before if before[p] != after[p]}, expected_changes)

    def test_pair_uses_same_reporting_implementation(self):
        material, dormant = [EVALS / name / "test-files" for name in CASES]
        for snapshot in ("before", "after"):
            for filename in ("app.py", "stats.py"):
                with self.subTest(snapshot=snapshot, file=filename):
                    self.assertEqual((material / snapshot / filename).read_bytes(),
                                     (dormant / snapshot / filename).read_bytes())
        self.assertEqual((material / "before/formatting.py").read_bytes(),
                         (dormant / "before/formatting.py").read_bytes())

    def test_supplied_snapshot_suites(self):
        for name in CASES:
            for snapshot in ("before", "after"):
                with self.subTest(case=name, snapshot=snapshot):
                    result = run(sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests",
                                 cwd=EVALS / name / "test-files" / snapshot)
                    self.assertIn("Ran 4 tests", result.stderr)
                    self.assertIn("OK", result.stderr)

    def test_default_exposure_and_dormant_control(self):
        for name, (number, _) in CASES.items():
            for snapshot in ("before", "after"):
                with self.subTest(case=name, snapshot=snapshot):
                    result = run(sys.executable, "-B", "-c", PROBE,
                                 cwd=EVALS / name / "test-files" / snapshot)
                    actual = json.loads(result.stdout)
                    label = "Records" if number == 22 and snapshot == "after" else "Items"
                    exposed = number == 21 and snapshot == "after"
                    self.assertEqual(actual, {
                        "default_empty": {"error": "ZeroDivisionError"} if exposed else {"value": f"{label}: 0"},
                        "default_populated": {"value": f"{label}: 2" + ("; Mean: 3" if exposed else "")},
                        "plain_empty": {"value": f"{label}: 0"},
                        "plain_populated": {"value": f"{label}: 2"},
                        "detailed_empty": {"error": "ZeroDivisionError"},
                        "detailed_populated": {"value": f"{label}: 2; Mean: 3"},
                        "calculation_empty": {"error": "ZeroDivisionError"},
                        "calculation_populated": {"value": {"count": 2, "mean": 3}},
                    })

    def test_real_staging_preserves_both_trees_and_excludes_grading(self):
        with tempfile.TemporaryDirectory(prefix="r6-fixture-check-") as scratch:
            scratch = Path(scratch)
            sources = scratch / "evals"
            harness = sources / "_harness/setup.sh"
            harness.parent.mkdir(parents=True)
            shutil.copy2(EVALS / "_harness/setup.sh", harness)
            for name in CASES:
                shutil.copytree(EVALS / name, sources / name)
            stage = scratch / "staged"
            run("bash", str(harness), str(stage), cwd=scratch)
            self.assertFalse(any((p / "SKILL.md").exists() for p in (stage, *stage.parents)))
            for name, (_, expected_changes) in CASES.items():
                with self.subTest(case=name):
                    subject = stage / name
                    self.assertEqual(set(run("git", "diff", "--cached", "--name-only", cwd=subject).stdout.splitlines()), expected_changes)
                    actual_paths = set(run("git", "ls-files", cwd=subject).stdout.splitlines())
                    before = tree(EVALS / name / "test-files/before")
                    after = tree(EVALS / name / "test-files/after")
                    self.assertEqual(actual_paths, set(after))
                    for path in actual_paths:
                        self.assertEqual((subject / path).read_bytes(), after[path])
                        base = run("git", "show", f"HEAD:{path}", cwd=subject).stdout.encode()
                        self.assertEqual(base, before[path])
                    self.assertEqual({p.relative_to(subject).as_posix() for p in subject.rglob("*")
                                      if p.is_file() and ".git" not in p.relative_to(subject).parts}, actual_paths)


if __name__ == "__main__":
    unittest.main(verbosity=2)
