"""Offline fixture validation/reproduction; never supply this file to actors.

Run from the toolbox root with Python 3.9+. Prints JSON evidence; no actor runs.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[6]
EVALS = ROOT / "klaude-plugin/skills/review-code/evals"
CASES = {
    "functional-retry-lifecycle": 8,
    "functional-stored-data-compatibility": 9,
    "functional-intent-mismatch": 10,
    "functional-justified-recovery": 11,
}

RETRY = '''
from client import submit
from store import ReceiptUnavailable, Store
store = Store()
store.fail_receipt_once = True
try:
    submit(store, "w", "op-1", {"color": "blue"})
except ReceiptUnavailable:
    pass
else:
    raise AssertionError("partial failure was not exercised")
assert store.preferences["w"] == {"color": "blue"}
assert submit(store, "w", "op-1", {"color": "green"})["ok"]
assert store.preferences["w"] == {"color": "green" if side == "before" else "blue"}
store = Store()
submit(store, "w", "op-1", {"color": "blue"})
assert submit(store, "w", "op-2", {"color": "green"}) == {"ok": True, "operation_id": "op-2"}
assert store.preferences["w"] == {"color": "green" if side == "before" else "blue"}
assert ("op-2" in store.recovery) == (side == "before")
'''

PERSISTED = '''
import json
from pathlib import Path
from api import list_destinations
from migration import migrate_batch
expected = [{"id": key, "address": address} for key, address in
            [("legacy-a", "a@example.test"), ("current-b", "b@example.test"), ("legacy-c", "c@example.test")]]
for limit in (0, 1, 3):
    rows = json.loads(Path("data/records.json").read_bytes())
    assert migrate_batch(rows, limit) == min(limit, 2)
    if side == "after" and limit < 2:
        try:
            list_destinations(rows)
        except KeyError as exc:
            assert exc.args == ("destination",)
        else:
            raise AssertionError("legacy row did not fail")
    else:
        assert list_destinations(rows) == expected
'''

READS = '''
from preferences import Preferences
from repository import MissingPreference, Repository, ScriptedBackend, TransientRead
broken = case == "functional-intent-mismatch" and side == "after"
key = "w" if side == "before" else " w "
for failures in (0, 1, 2, 3):
    backend = ScriptedBackend([TransientRead("busy") for _ in range(failures)] + [{"color": "blue"}])
    try:
        result = Preferences(Repository(backend)).read(key)
    except TransientRead:
        assert failures == 3 or (broken and failures > 0)
    else:
        assert failures < 3 and not (broken and failures > 0)
        assert result == {"color": "blue"}
    expected_attempts = 1 if broken else min(failures + 1, 3)
    assert backend.keys == ["w"] * expected_attempts
backend = ScriptedBackend([MissingPreference("missing")])
try:
    Preferences(Repository(backend)).read(key)
except MissingPreference:
    assert backend.keys == ["w"]
else:
    raise AssertionError("permanent failure was swallowed")
'''


def run(args, cwd=ROOT, source=None):
    result = subprocess.run(args, cwd=cwd, input=source, text=True, encoding="utf-8",
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(f"{args} in {cwd}: {result.stdout}\n{result.stderr}")
    return result.stdout + result.stderr


def main():
    evidence = {"python": sys.version, "cases": {}, "limits": "offline fixture checks, not workflow acceptance"}
    all_ids = [json.loads(p.read_bytes())["id"] for p in EVALS.glob("*/eval.json")]
    assert len(all_ids) == len(set(all_ids)), "duplicate review eval ID"
    for case, eval_id in CASES.items():
        directory = EVALS / case
        metadata = json.loads((directory / "eval.json").read_bytes())
        assert metadata["id"] == eval_id and metadata["name"] == case
        assert metadata["skills"] == ["review-code"]
        actual = sorted(p.relative_to(directory).as_posix() for p in (directory / "test-files").rglob("*") if p.is_file())
        assert metadata["files"] == actual, case + ": files[] is incomplete or duplicated"
        assert [a["id"] for a in metadata["assertions"]] == [f"{eval_id}.{i}" for i in range(1, len(metadata["assertions"]) + 1)]
        assert all(a["text"] for a in metadata["assertions"])
        assert not any("oracle" in Path(p).parts or Path(p).name.startswith(("expected-", "gold-")) for p in actual)
        json.loads((directory / "oracle/expected-results.json").read_bytes())
        evidence["cases"][case] = {"hashes": {p.relative_to(directory).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(directory.rglob("*")) if p.is_file()}, "snapshots": {}}
        probe = RETRY if eval_id == 8 else PERSISTED if eval_id == 9 else READS
        for side in ("before", "after"):
            tree = directory / "test-files" / side
            suite = run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests"], tree)
            assert "Ran 0 tests" not in suite
            run([sys.executable, "-B", "-"], tree, f"side = {side!r}\ncase = {case!r}\n" + probe)
            evidence["cases"][case]["snapshots"][side] = {"suite": suite.strip(), "probe": "PASS"}

    stage = Path(run(["bash", str(EVALS / "_harness/setup.sh")]).strip())
    evidence["stage"] = str(stage)
    for case in CASES:
        tree = stage / case
        expected = {p.relative_to(EVALS / case / "test-files/after").as_posix(): p.read_bytes()
                    for p in (EVALS / case / "test-files/after").rglob("*") if p.is_file()}
        staged = run(["git", "ls-files", "-z"], tree).split("\0")[:-1]
        assert set(staged) == set(expected)
        assert all((tree / p).read_bytes() == content for p, content in expected.items())
        diff = run(["git", "diff", "--cached", "--name-only"], tree).splitlines()
        expected_diff = ["service.py"] if CASES[case] == 8 else ["reader.py"] if CASES[case] == 9 else ["reader.py", "tests/test_reads.py"]
        assert diff == expected_diff, (case, diff)
        evidence["cases"][case]["staged_diff"] = diff

    seeds = {"R1": "review-code/evals/functional-cleanup-ownership", "R3": "review-code/evals/functional-disabled-provider-history",
             "I1": "implement/evals/functional-plan-delivery-conflict", "I2": "implement/evals/functional-standalone-patch-contract"}
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
