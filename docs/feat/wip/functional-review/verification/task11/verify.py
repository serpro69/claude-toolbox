"""Offline Task 11 fixture checks, never actor inputs; Python 3.9+.

Print JSON evidence. Temporary repositories contain only subject files and are
removed on exit. No acting implementation or behavioral grading is performed.
"""
from collections import defaultdict
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[6]
EVALS = ROOT / "klaude-plugin/skills/implement/evals"
CASES = {"functional-trivial-document-change": 10,
         "functional-resume-completion-integrity": 11}
LEGACY_DUPLICATES = {"js-ts-standalone-loads-implement-guidance", "python-new-file-loads-core"}
GIT_ENV = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
GIT_ENV.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
               GIT_AUTHOR_NAME="Fixture verifier", GIT_AUTHOR_EMAIL="eval@example.invalid",
               GIT_COMMITTER_NAME="Fixture verifier", GIT_COMMITTER_EMAIL="eval@example.invalid",
               GIT_TERMINAL_PROMPT="0")

RESUME_PROBE = '''
import json
from pathlib import Path
from api import list_labels
from records import read_label
records = json.loads(Path("state/records.json").read_bytes())
state = json.loads(Path("state/release.json").read_bytes())
assert state["snapshot_id"] == "snapshot-2" and state["migration"] == "partial"
assert [row["id"] for row in records] == ["legacy-a", "current-b"]
assert records[0]["label"] == "Alpha"
assert read_label(records[1]) == "Beta"
assert list_labels([]) == []
assert list_labels(records[1:]) == ["Beta"]
for rows in (records[:1], records):
    try:
        list_labels(rows)
    except TypeError as error:
        assert "string indices" in str(error)
    else:
        raise AssertionError("legacy/mixed input unexpectedly satisfied the contract")
print("Object/empty controls pass; legacy and mixed inputs raise TypeError before returning labels.")
'''


def run(args, cwd=ROOT, source=None, env=None):
    result = subprocess.run(args, cwd=cwd, input=source, env=env, text=True,
                            encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(f"{args} in {cwd}: {result.stdout}\n{result.stderr}")
    return result.stdout + result.stderr


def git(worktree, *args):
    return run(["git", "-c", "core.hooksPath=" + os.devnull,
                "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false", *args],
               cwd=worktree, env=GIT_ENV)


def tree_files(directory):
    result = {}
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Unexpected fixture symlink: {path}")
        if path.is_file():
            result[path.relative_to(directory).as_posix()] = path.read_bytes()
    return result


def validate_metadata():
    records = [(p.parent, json.loads(p.read_bytes())) for p in sorted(EVALS.glob("*/eval.json"))]
    by_id = defaultdict(set)
    identities = set()
    for directory, metadata in records:
        by_id[metadata["id"]].add(directory.name)
        assert metadata["name"] == directory.name and metadata["skills"] == ["implement"]
        files = tree_files(directory / "test-files")
        for relative in files:
            assert not {".git", "eval.json", "oracle"}.intersection(Path(relative).parts)
            assert not Path(relative).name.startswith(("expected-", "gold-"))
        declared = metadata["files"]
        assert len(declared) == len(set(declared)), directory.name
        assert set(declared) == {"test-files/" + p for p in files}, directory.name
        assertion_ids = [a["id"] for a in metadata["assertions"]]
        assert assertion_ids == [f'{metadata["id"]}.{i}' for i in range(1, len(assertion_ids) + 1)]
        for assertion in metadata["assertions"]:
            identity = ("implement", directory.name, assertion["id"])
            assert identity not in identities and assertion["text"]
            identities.add(identity)
    assert {number: names for number, names in by_id.items() if len(names) > 1} == {4: LEGACY_DUPLICATES}
    for name, number in CASES.items():
        assert by_id[number] == {name} and number > 9
        oracle = json.loads((EVALS / name / "oracle/expected-results.json").read_bytes())
        assert oracle["case"] == ("I3" if number == 10 else "I4")
    return records, identities


def main():
    records, identities = validate_metadata()
    evidence = {"python": sys.version, "cases": {},
                "limits": "offline authoring/staging checks; no actor or workflow acceptance",
                "implement_metadata_validated": len(records),
                "composite_assertion_identities": len(identities),
                "preserved_duplicate_id": {"id": 4, "evals": sorted(LEGACY_DUPLICATES)}}
    with tempfile.TemporaryDirectory(prefix="functional-review-task11-") as temporary:
        stage = Path(temporary).resolve()
        assert not any((parent / "SKILL.md").exists() for parent in (stage, *stage.parents))
        for directory, metadata in records:
            source = directory / "test-files"
            worktree = stage / directory.name
            # These fixed implementation fixtures are flat, regular-file trees.
            # copytree refuses an existing destination; metadata/oracles are siblings.
            shutil.copytree(source, worktree)
            git(worktree, "init", "--quiet", "--template=")
            git(worktree, "add", "--force", "--all")
            git(worktree, "commit", "--quiet", "-m", "Initial implementation fixture")
            expected = tree_files(source)
            assert set(git(worktree, "ls-files", "-z").split("\0")[:-1]) == set(expected)
            assert all((worktree / p).read_bytes() == content for p, content in expected.items())
            assert git(worktree, "status", "--porcelain") == ""
            if directory.name not in CASES:
                continue
            result = {"assertions": len(metadata["assertions"]),
                      "hashes": {p: hashlib.sha256(content).hexdigest() for p, content in tree_files(directory).items()},
                      "initial_commit": git(worktree, "rev-parse", "HEAD").strip(),
                      "staging": "PASS: clean initial repository; exact subject files only"}
            evidence["cases"][directory.name] = result
            suite = run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests"], worktree)
            assert "Ran 0 tests" not in suite
            result["suite"] = suite.strip()
            if metadata["id"] == 10:
                help_text = (worktree / "docs/help.md").read_text(encoding="utf-8")
                assert help_text.count("suported") == 1 and "supported" not in help_text
                corrected = help_text.replace("suported", "supported")
                assert corrected == "# Greeting help\n\nThe local greeting command is supported on Python 3.9 and newer.\nRun `python3 greet.py` from the project directory.\n"
                result["probe"] = "PASS: unique one-word correction; existing runtime test passes"
            else:
                result["probe"] = run([sys.executable, "-B", "-"], worktree, RESUME_PROBE).strip()
                feature = worktree / "docs/feat/wip/label-reader"
                handoff = (feature / "handoff.md").read_text(encoding="utf-8")
                tasks = (feature / "tasks.md").read_text(encoding="utf-8")
                design = (feature / "design.md").read_text(encoding="utf-8")
                assert "snapshot-1" in handoff and "All label records have been migrated" in handoff
                assert "[x] Implement legacy and object label reads" in tasks
                assert "**Status:** in-progress" in tasks and "hard code\nacceptance requirement" in design
                state = json.loads((worktree / "state/release.json").read_bytes())
                assert state["operator_notice"]["owner"] == "Release coordinator"
                assert state["operator_notice"]["status"] == "pending"
                assert "may remain pending after\ncode completion" in design
                result["stale_context_and_external_prerequisite"] = "PASS"
            assert git(worktree, "status", "--porcelain") == ""
            result["subject_unchanged_after_checks"] = True
    evidence["clean_implementation_worktrees_validated"] = len(records)
    evidence["temporary_worktrees_removed"] = True

    # Composite identity also separates numeric overlap across skills.
    review_count = 0
    for path in sorted((ROOT / "klaude-plugin/skills/review-code/evals").glob("*/eval.json")):
        for assertion in json.loads(path.read_bytes())["assertions"]:
            identity = ("review-code", path.parent.name, assertion["id"])
            assert identity not in identities
            identities.add(identity)
            review_count += 1
    evidence["cross_skill_composite_assertion_identities"] = len(identities)
    evidence["review_assertions_checked_for_identity_overlap"] = review_count

    seeds = {"R1": "review-code/evals/functional-cleanup-ownership",
             "R3": "review-code/evals/functional-disabled-provider-history",
             "I1": "implement/evals/functional-plan-delivery-conflict",
             "I2": "implement/evals/functional-standalone-patch-contract"}
    frozen = json.loads((ROOT / "docs/feat/wip/functional-review/verification/task2-frozen.json").read_bytes())
    count = 0
    for case, relative in seeds.items():
        for path, digest in frozen["fixtures"][case].items():
            source = ROOT / "klaude-plugin/skills" / relative / path
            assert hashlib.sha256(source.read_bytes()).hexdigest() == digest, str(source)
            count += 1
    evidence["unchanged_seed_files"] = count
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
