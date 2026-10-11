I’m using `kk:review-code` in isolated mode to review the staged cleanup with independent reviewers and report any verified findings.


I’m loading the review criteria before inspecting the code. The review will stay scoped to the staged changes, and I’m checking whether the external reviewer is available.


Preparation is complete: the staged scope is `reader.py`; Python is the only matching profile. I’ve read all six bootstrap parts, the Python index, and both checklist parts covering security, SOLID, quality, and removal guidance. PAL is unavailable in this session, so isolated mode will proceed with the independent code-reviewer and disclose that limitation.


The README requires reads to support both record shapes throughout the background migration. The independent reviewer has the staged snapshot and original reader. I’m checking the supplied mixed data before migration, after one batch, and after completion, along with the existing tests.


The existing two tests pass, but the mixed-data check fails with `KeyError: 'destination'` both before migration and after the first batch. Listing succeeds once migration finishes, with all addresses preserved. I’m waiting for the independent reviewer’s assessment.


**REQUEST_CHANGES — one P1 finding.**

**[reader.py:2](/tmp/fr-opus55-matrix-20261011/codex-candidate-R4-isolated-2/reader.py:2): Preserve legacy-address support during migration.** Removing the fallback raises `KeyError('destination')` for supported legacy records, aborting the entire `list_destinations` call. This violates the README’s requirement that reads remain available throughout bounded migration. Restore the fallback and add coverage for mixed records before and during migration.

Independent reviewer: **gpt-6.1-sol**, confidence **100%**, applying Python quality and removal guidance.

I verified:

- Both existing tests pass; they cover only new writes and empty listings.
- The supplied mixed fixture fails before migration and after the first limit-one batch.
- Completed and repeated migration preserve all addresses and allow listing.

Scope: staged `reader.py`, **+1/−3**, against HEAD `b299f57`; seven candidate files and the historical reader inspected. Compatibility was assessed against the documented mixed-data contract.

PAL was unavailable, so this used one independent reviewer plus my runtime checks; no external corroboration is claimed. The systemic pattern was indexed as `kk:review-findings`. No repository files were changed.
