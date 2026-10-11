I’m using `kk:review-code` in isolated mode to review the staged cleanup with independent reviewers. I’ll load the review guidance, select the staged diff, and report findings without changing the code.

The staged scope is one file, `reader.py`, so the Python guidance applies. PAL isn’t available in this session; I’ll proceed with the independent code reviewer and note that the review has one reviewer rather than two.

Preparation is complete: all six common instruction parts, the Python index, and both checklist parts are loaded. The other seven profiles do not match. I’ll now inspect the component contract, staged change, and affected callers.

The contract requires both record shapes to remain readable throughout migration, and the supplied data contains both. The independent reviewer has the staged and baseline sources. I’m checking reads before migration, after one batch, and after completion, alongside the existing tests.

The staged reader raises `KeyError('destination')` on the supported mixed snapshot, both before migration and after the first batch. The baseline succeeds in both states. Reads succeed once migration finishes; the two existing tests also pass, but cover only new writes and an empty list. The independent reviewer is finishing its assessment.

**REQUEST_CHANGES** — one P1 finding from the independent code reviewer.

**P1: Preserve legacy reads until migration completes** — [reader.py:2](/tmp/fr-opus55-matrix-20261011/codex-candidate-R4-isolated-1/reader.py:2)

The unconditional `row["destination"]` lookup raises `KeyError` for supported legacy records. Because `list_destinations` reads every record, one unmigrated row aborts the entire listing. This violates the [documented requirement](/tmp/fr-opus55-matrix-20261011/codex-candidate-R4-isolated-1/README.md:5) to keep both shapes readable during migration.

Restore the legacy fallback and add regression coverage across migration states, asserting preserved addresses.

*Reviewer: code-reviewer (GPT-6.1-sol); confidence: 100%. Python profile, `code-quality-checklist.md`, triggered by `.py` extension.*

I reproduced these results against baseline `b299f57` and the staged candidate:

| Scenario | Baseline | Staged |
|---|---|---|
| Initial mixed snapshot | Pass | `KeyError` |
| After first migration batch | Pass | `KeyError` |
| Completed migration and subsequent retry | Pass | Pass |
| New write and empty list | Pass | Pass |

Both existing tests pass, but cover only new writes and empty lists. Compatibility with legacy and partially migrated records is **blocked**.

Review covered the staged `reader.py` change (+1/−3), README, API consumer, writer, migration, fixture, and tests, including historical counterparts. PAL was unavailable, so this is a single-reviewer isolated assessment without external corroboration. I executed the checks; the independent reviewer inspected source.

The systemic pattern was indexed under `kk:review-findings`. No repository files were changed.
