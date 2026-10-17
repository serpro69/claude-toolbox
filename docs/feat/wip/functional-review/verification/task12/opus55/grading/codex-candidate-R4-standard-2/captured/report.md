I’m using `kk:review-code` to review the staged cleanup, trace affected behavior, and check for regressions.

Preparation is complete for `git diff --cached`: one changed Python file. All six bootstrap parts, the Python index, and both checklist parts are loaded, including security, SOLID, quality, and removal guidance. Python matched; Go, Java, JS/TS, Kotlin, Kubernetes, operator, and skill profiles did not. I’ll now check the reader’s contract and callers.

The cleanup breaks the documented mixed-record migration flow. I reproduced `KeyError: 'destination'` before migration and after the first bounded batch; the baseline reads both states successfully. Fully migrated records still work. The two existing tests pass because they cover only new writes and an empty list.

**REQUEST_CHANGES — one P1 regression.**

::code-comment{file="reader.py" line="2" severity="P1"}
Removing the legacy fallback makes `api.list_destinations` raise `KeyError: 'destination'` whenever any record still has a top-level `address`, failing the entire listing. This violates the [documented requirement](/tmp/fr-opus55-matrix-20261011/codex-candidate-R4-standard-2/README.md:5) to keep both shapes readable throughout bounded migration.

Restore the fallback and add regression coverage for the mixed snapshot before migration, between batches, and after completion.
::

Profile: Python · Checklist: `code-quality-checklist.md` · Trigger: `.py` extension. Confidence: **100%**—reproduced against the exact staged candidate and confirmed the baseline succeeds.

Reviewed staged `reader.py` against HEAD `b299f57` (one file, +1/−3), including its API caller, writer, migration, fixtures, and tests. The cleanup must preserve the README’s compatibility contract.

| Scenario | HEAD | Staged candidate |
|---|---|---|
| Legacy or initial mixed records | Pass | `KeyError` |
| Mixed records after one migration batch | Pass | `KeyError` |
| Completed migration and repeated migration | Pass | Pass; addresses preserved |
| New writes, current-only records, empty list | Pass | Pass |

Both existing tests pass on both revisions; neither exercises legacy records. Compatibility during migration is **blocked**. Verification used isolated local snapshots; the documented contract requires no external environment.

Indexed the systemic migration-compatibility finding under `kk:review-findings`. No repository files changed.
