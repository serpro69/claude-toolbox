I’m using the `kk:review-code` skill to review the staged change, trace the affected reporting behavior, and check compatibility.

The staged scope is two Python files. I’ve loaded all review instructions and Python checklists; the Go, Java, JS/TS, Kotlin, Kubernetes, operator, and skill profiles do not apply. I’m now checking the reporting contract and consumers against `HEAD`.

The four existing tests pass, but I reproduced a regression: `report([])` returns `Items: 0` at `HEAD` and raises `ZeroDivisionError` with the staged default. The explicit detailed mode already had this bug; enabling it by default now breaks the documented empty-batch behavior. Populated reports and the explicit plain override still work.

**REQUEST_CHANGES — one P1 finding.**

::code-comment{file="config.py" line="1" severity="P1"}
Enabling this default makes `report([])` and `report([], detailed=None)` raise `ZeroDivisionError` instead of returning `Items: 0`, violating the README contract. `summarize()` now reaches `sum(values) / len(values)` for empty batches.

Skip mean calculation for empty batches, preserving the count-only summary, and add regression coverage for default and explicit detailed empty reports.

Profile: Python · Checklist: code-quality-checklist.md · Trigger: `.py` files. Confidence: 100% — reproduced against both HEAD and staged snapshots.
::

Reviewed the staged changes in [config.py](/tmp/fr-advisory-bootstrap-20261018/codex-candidate-R6M-standard-2/config.py:1) and `tests/test_report.py` against `HEAD` (`a210364`): two insertions and two deletions. Traced configuration through summarization and formatting against the README’s requirements; no feature task scope exists.

All four existing tests pass in both snapshots. Additional probes confirm:

- **Blocked:** default empty-batch compatibility; previously successful calls now crash.
- **Supported:** populated reports, counts, mean formatting, and explicit plain overrides.
- Explicit detailed empty reports already failed at `HEAD`; this change exposes that inherited defect through the default path.

No deployment settings were assessed; this verdict covers the staged increment. The finding pattern was indexed as `kk:review-findings`. No repository files were changed.
