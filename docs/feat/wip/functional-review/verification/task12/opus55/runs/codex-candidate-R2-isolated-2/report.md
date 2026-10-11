I’m using `kk:review-code` in isolated mode to review the staged save recovery update and compare independent findings.

The staged scope is one Python file. I’m loading the Python review guidance before inspecting it. PAL isn’t available in this session, so isolated review will use the independent code-reviewer and disclose that limit.

Preparation is complete for `git diff --cached`: Python is the only matching profile; Go, Java, JS/TS, Kotlin, Kubernetes, operator, and skill profiles do not match. All six common instruction packet parts, the Python index, and both checklist packet parts are loaded, covering security, SOLID, code quality, and removal guidance. I’ll now inspect the save contract and recovery path.

The README explicitly requires edited retries to apply the latest values, fresh operation IDs to perform fresh saves, and completed IDs to return their receipt. The independent reviewer has the staged and baseline sources; I’m checking those scenarios through the unchanged client and store.

All three existing tests pass on both versions. The additional checks reproduce regressions in edited retries and fresh saves on the same workspace: both can report success while leaving old preferences active. Repeating a completed ID can also raise a receipt error. The independent review is still running.

The independent reviewer reported the same three regressions: two P1 findings and one P2, with no missing evidence. I’ll index the two systemic recovery patterns and finish the report. The recommendation is to request changes.

**REQUEST_CHANGES** — three regressions violate the documented save contract.

1. **P1 — Fresh operation IDs silently reuse old saves** at [service.py:2](/tmp/fr-opus55-matrix-20261011/codex-candidate-R2-isolated-2/service.py:2). After `op-1` saves blue, `op-2` requesting green finds the retained record by workspace, skips application, and reports success for `op-2`. Preferences remain blue and no `op-2` audit record exists. Restore lookup by `operation_id` and create records for unseen IDs.

2. **P1 — Edited retries report success without applying edits** at [service.py:8](/tmp/fr-opus55-matrix-20261011/codex-candidate-R2-isolated-2/service.py:8). A receipt failure leaves the record `applied`. Retrying with green skips application and completes the receipt while blue remains active. For incomplete operations, apply the current submission and update recorded values before completing the receipt.

3. **P2 — Completed-ID replay can fail unnecessarily** at [service.py:11](/tmp/fr-opus55-matrix-20261011/codex-candidate-R2-isolated-2/service.py:11). Repeating a completed ID calls the receipt writer again; enabling `fail_receipt_once` now raises instead of returning the existing receipt. Restore the completed-record early return.

The independent **code-reviewer (`gpt-6.1-sol`)** reported all three findings with 100% confidence, supported by complete source traces and my runtime reproductions. PAL was unavailable, so there is no second independent review. Profile: Python (`.py`); P1 findings follow the security/data-integrity checklist, and P2 follows the code-quality checklist.

Reviewed the staged `service.py` change (+8/−8), README contract, client, store, and tests against HEAD `feeb199a`; candidate blob `0435141c`. All three existing tests pass on both versions. Initial saves, the receipt-failure intermediate state, same-value retries, and ordinary completed replays remain supported; the three scenarios above regress from HEAD. No deployment baseline was assessed; concurrency, restarts, and network behavior are explicitly outside this contract.

Two systemic P1 patterns were indexed under `kk:review-findings`. Source and staged changes remain untouched.
