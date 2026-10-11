I’m using `kk:review-code` in isolated mode to review the staged save recovery update. I’ll load the review guidance, run the independent reviewers, and verify their findings against the code.

The staged diff is limited to `service.py`. PAL is unavailable in this session, so the review will use the independent code-reviewer, with that coverage limitation noted in the report.

Preparation is complete: all six common instruction parts and both checklist parts are loaded. `service.py` activates the Python profile; Go, Java, JS/TS, Kotlin, Kubernetes, operator, and skill profiles do not match. The review will apply all four Python checklists: security, SOLID, code quality, and removal guidance.

The README explicitly requires edited-value retries, receipt replay for completed IDs, and fresh saves for new IDs. The independent reviewer has the staged source and base revision. I’m checking those lifecycle cases alongside the existing tests.

All three existing tests pass. The lifecycle checks found regressions: an edited retry reports success with the old values still active, and a new operation ID reuses the previous save. A completed-ID repeat can also fail by attempting another receipt write. Each case behaves correctly at the review base; the independent review is still in progress.

The staged files are unchanged. The reproduced failures point to three targeted corrections: look up recovery by operation ID, apply current values on incomplete retries, and return completed receipts without another write. I’m waiting for the independent reviewer’s assessment before finalizing the report.

**REQUEST_CHANGES** — two P1 regressions and one P2 regression.

1. **P1: Edited retries silently retain old values** — [service.py:8](/tmp/fr-opus55-matrix-20261011/codex-candidate-R2-isolated-1/service.py:8)  
   Save blue, let receipt creation fail, then retry the same ID with red. The record is already `applied`, so the retry skips application and reports success while blue remains active. Apply the latest submitted values for every incomplete operation.

2. **P1: Fresh operation IDs reuse earlier saves** — [service.py:2](/tmp/fr-opus55-matrix-20261011/codex-candidate-R2-isolated-1/service.py:2)  
   After completing `op-1`, submitting different values under `op-2` selects the retained record by workspace. Nothing is applied or recorded for `op-2`, yet success is returned for it. Restore operation-ID lookup and retain separate audit records.

3. **P2: Completed-operation replay can now fail** — [service.py:11](/tmp/fr-opus55-matrix-20261011/codex-candidate-R2-isolated-1/service.py:11)  
   Repeating a completed ID calls the receipt writer again. If receipt creation is unavailable, the repeat raises instead of returning its completed receipt. Restore the completed-record early return.

These are independent **code-reviewer (`gpt-6.1-sol`)** findings, each with 100% reviewer confidence. I also reproduced all three against the staged candidate; the base handles them correctly. Python’s security checklist applies to the P1 findings; its code-quality checklist applies to P2.

Reviewed the staged `service.py` change against `feeb199a`, plus README contracts, client, store, tests, and historical service source. Normal saves, the applied state after receipt failure, unchanged-value retries, and completed repeats with an available receipt writer remain supported. The failures above violate the README’s recovery contract.

**Validation:** all three existing tests pass, but omit these failing scenarios. PAL was unavailable, so this is a single-reviewer isolated review without dual-reviewer corroboration. No deployed-environment assessment was made.

Both systemic P1 patterns were indexed as `kk:review-findings`. No repository files were changed.
