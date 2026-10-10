"""Offline Task 10 fixture checks; controller-only, never an actor input.

Run from the toolbox root with Python 3.9+. Emits JSON; does not run reviewers.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[6]
EVALS = ROOT / "klaude-plugin/skills/review-code/evals"
CASES = {
    "functional-clean-partial-feature": 12,
    "functional-inherited-conditional-defect": 13,
    "functional-missing-baseline": 14,
    "functional-report-zero-coverage": 15,
    "functional-report-external-failure": 16,
}
PROBES = {
    12: '''
from routes import get
assert get("/settings") == (200, {"theme": "light"})
assert get("/export-preview") == (404, None)
assert get("/unknown") == (404, None)
if side == "after":
    import preview
    import routes
    def forbidden():
        raise AssertionError("disabled renderer was reached")
    routes.render_preview = forbidden
    assert get("/export-preview") == (404, None)
    try:
        preview.render_preview()
    except NotImplementedError:
        pass
    else:
        raise AssertionError("future renderer unexpectedly implemented")
''',
    13: '''
from app import report
from stats import summarize
assert report([]) == ("Items: 0" if side == "before" else "Records: 0")
assert summarize([2, 4], detailed=True) == {"count": 2, "mean": 3}
try:
    summarize([], detailed=True)
except ZeroDivisionError:
    pass
else:
    raise AssertionError("inherited conditional defect did not reproduce")
''',
    14: '''
from client import save
class Transport:
    def put(self, path, body):
        assert path == "/settings"
        return body
for name in ("  Ada  ", "Ada Lovelace", "", "   "):
    expected = name if side == "before" else name.strip()
    assert save(Transport(), name) == {"display_name": expected}
''',
}
REPLAY_PROBE = '''
import importlib.util
from pathlib import Path
def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result
provider_class = module("provider", Path("source/provider.py")).Provider
for side in ("base", "candidate"):
    source = module(side, Path("source") / side / "settings.py")
    provider = provider_class()
    assert source.save(provider, {"theme": "dark"}) == {"ok": side == "candidate"}
    assert provider.values == {"theme": "light"}
'''


def run(args, cwd=ROOT, source=None):
    result = subprocess.run(args, cwd=cwd, input=source, text=True, encoding="utf-8",
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(f"{args} in {cwd}: {result.stdout}\n{result.stderr}")
    return result.stdout + result.stderr


def tree_files(directory):
    return {p.relative_to(directory).as_posix(): p.read_bytes()
            for p in sorted(directory.rglob("*")) if p.is_file()}


def main():
    evidence = {"python": sys.version, "cases": {},
                "limits": "offline fixture checks; no actor or live PAL acceptance"}
    records = [(p.parent, json.loads(p.read_bytes())) for p in sorted(EVALS.glob("*/eval.json"))]
    ids = [metadata["id"] for _, metadata in records]
    assert len(ids) == len(set(ids)), "duplicate review eval ID"
    for directory, metadata in records:
        for relative in metadata["files"]:
            path = directory / relative
            assert path.is_file() and path.resolve().is_relative_to((directory / "test-files").resolve()), path
        assert not any("oracle" in Path(p).parts or Path(p).name.startswith(("expected-", "gold-"))
                       for p in metadata["files"])
    evidence["review_metadata_validated"] = len(records)

    for name, eval_id in CASES.items():
        directory = EVALS / name
        metadata = json.loads((directory / "eval.json").read_bytes())
        assert (metadata["id"], metadata["name"], metadata["skills"]) == (eval_id, name, ["review-code"])
        actual = ["test-files/" + p for p in tree_files(directory / "test-files")]
        assert metadata["files"] == actual, name + ": incomplete/duplicate files[]"
        assertions = metadata["assertions"]
        assert [a["id"] for a in assertions] == [f"{eval_id}.{i}" for i in range(1, len(assertions) + 1)]
        assert all(a["text"] for a in assertions)
        oracle = json.loads((directory / "oracle/expected-results.json").read_bytes())
        case = {"hashes": {p: hashlib.sha256(content).hexdigest() for p, content in tree_files(directory).items()},
                "assertions": len(assertions)}
        evidence["cases"][name] = case
        if eval_id < 15:
            case["snapshots"] = {}
            for side in ("before", "after"):
                tree = directory / "test-files" / side
                suite = run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests"], tree)
                assert "Ran 0 tests" not in suite
                run([sys.executable, "-B", "-"], tree, f"side = {side!r}\n" + PROBES[eval_id])
                case["snapshots"][side] = {"suite": suite.strip(), "probe": "PASS"}
        else:
            tree = directory / "test-files"
            pal = json.loads((tree / "pal-result.json").read_bytes())
            assert pal["provenance"]["kind"] == "synthetic-test-data"
            assert pal["provenance"]["live_mcp_call"] is False
            assert oracle["controller_contract"]["mode"] == "isolated-report-replay"
            assert pal["result"]["file_context"]["files_embedded"] == 0
            assert pal["result"]["code_review_status"]["files_checked"] == 0
            assert pal["result"]["code_review_complete"] == (eval_id == 15)
            if eval_id == 15:
                assert "safe to release" in pal["result"]["expert_analysis"]["raw_analysis"]
            else:
                assert pal["result"]["error"]["code"] == "EXTERNAL_REVIEW_UNAVAILABLE"
            run([sys.executable, "-B", "-"], tree, REPLAY_PROBE)
            case["probe"] = "PASS: fixed finding reproduces; synthetic PAL variant valid"

    replay_a = tree_files(EVALS / "functional-report-zero-coverage/test-files")
    replay_b = tree_files(EVALS / "functional-report-external-failure/test-files")
    assert replay_a.keys() == replay_b.keys()
    assert [p for p in replay_a if replay_a[p] != replay_b[p]] == ["pal-result.json"]
    evidence["replay_only_difference"] = "pal-result.json"

    stage = Path(run(["bash", str(EVALS / "_harness/setup.sh")]).strip())
    evidence["stage"] = str(stage)
    # All legacy and new review fixtures must still stage with their exact actor files.
    for directory, metadata in records:
        name = directory.name
        inputs = directory / "test-files"
        expected = tree_files(inputs / "after" if (inputs / "after").is_dir() else inputs)
        staged = run(["git", "ls-files", "-z"], stage / name).split("\0")[:-1]
        assert set(staged) == set(expected), name
        assert all((stage / name / p).read_bytes() == content for p, content in expected.items()), name
        if name in CASES:
            diff = run(["git", "diff", "--cached", "--name-only"], stage / name).splitlines()
            expected_diff = {12: ["preview.py", "routes.py"],
                             13: ["formatting.py", "tests/test_report.py"],
                             14: ["payload.py", "tests/test_payload.py"]}.get(CASES[name], sorted(expected))
            assert diff == expected_diff, (name, diff)
            evidence["cases"][name]["staged_diff"] = diff
            if CASES[name] >= 15:
                # Run in the staged repository: Git otherwise filters patch paths
                # by this fixture's prefix within the toolbox checkout.
                patch_stat = run(["git", "apply", "--numstat", "change.patch"], stage / name)
                assert patch_stat.strip() == "1\t1\tsettings.py"
                run(["git", "apply", "--check", "--directory=source/base", "change.patch"], stage / name)
    evidence["review_worktrees_validated"] = len(records)

    r3 = stage / "functional-disabled-provider-history"
    historical_path = "provider/settings.py"
    expected_blob = (EVALS / "functional-disabled-provider-history/test-files/history/released" / historical_path).read_text(encoding="utf-8")
    assert run(["git", "show", f"eval-release:{historical_path}"], r3) == expected_blob
    assert historical_path not in run(["git", "ls-tree", "-r", "--name-only", "HEAD"], r3).splitlines()
    assert not (r3 / historical_path).exists()
    assert historical_path not in run(["git", "diff", "--cached", "--name-only"], r3).splitlines()
    evidence["r3_history_only_provider"] = {"sha256": hashlib.sha256(expected_blob.encode()).hexdigest(), "result": "PASS"}
    r7 = stage / "functional-missing-baseline"
    assert run(["git", "tag", "--list"], r7).splitlines() == ["eval-base"]
    evidence["r7_release_baseline_absent"] = True

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
