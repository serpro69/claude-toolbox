I’m using `kk:review-code` to review the staged cleanup, trace affected reader contracts, and verify any findings. I’ll leave the code unchanged.

Preparation is complete: the staged diff changes only `reader.py` (+1/−3). All six common instruction parts, the Python index, and both checklist parts are loaded. Python matched; Go, Java, JS/TS, Kotlin, Kubernetes, operator, and skill profiles did not. I’m now checking the reader’s documented contract and callers against `HEAD`.

The cleanup breaks the documented mixed-format contract. I reproduced `KeyError('destination')` when listing the supplied snapshot both before migration and after one batch; the `HEAD` reader succeeds in both states. The two existing tests pass because they cover only new writes and an empty list. Fully migrated records still work.

**REQUEST_CHANGES — one P1 regression.**

**P1: Restore legacy-address support in [reader.py:2](/tmp/fr-opus55-matrix-20261011/codex-candidate-R4-standard-1/reader.py:2).** Removing the fallback makes `api.list_destinations()` raise `KeyError('destination')` on legacy records, aborting the entire listing. The [documented contract](/tmp/fr-opus55-matrix-20261011/codex-candidate-R4-standard-1/README.md:5) requires both formats to remain readable throughout background migration.

I reproduced this with `data/records.json` before migration and after one batch. The `HEAD` reader succeeds in both states. Restore the fallback and add coverage for these mixed-format states.

- **Confidence:** 100%; reproduced against both baseline and staged source.
- **Profile:** Python · `code-quality-checklist.md` · triggered by `.py`.

Reviewed the staged cleanup against `HEAD` (`b299f57`): one file, +1/−3, including its listing consumer, writer, migration, and fixture. Both existing tests pass, but cover only new writes and empty input. Fully migrated records and repeated migration completion preserve addresses; compatibility during migration is **blocked**.

Validation used the repository’s local JSON model; no separate deployed baseline was assessed. The systemic finding was indexed as `kk:review-findings`. No repository files were changed.
