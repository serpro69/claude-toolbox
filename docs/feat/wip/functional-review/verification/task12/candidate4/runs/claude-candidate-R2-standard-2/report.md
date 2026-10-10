Both systemic findings indexed. Here is the review.

## Code Review Summary

**Files reviewed**: 1 file (`service.py`), 8 insertions / 8 deletions (whole function rewritten)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: Staged "save recovery update" to `save()`. Authoritative contract is `README.md` (workspace-preferences save: caller-supplied operation ID, idempotent retry with edited values, fresh ID = fresh save). Selected diff = `git diff --staged` (no unstaged changes). Candidate = index blob of `service.py`.
**Baselines**: Review base `feeb199` → staged candidate. In-memory store only; README explicitly disclaims threads/process-restart/network, so cross-restart recovery and concurrency are out of scope.
**Profiles**: `python` (active, all 4 checklists applied). No other profile matched.

## Behavior and Compatibility

I traced `save()` through `store.py` (`apply`, `receipt`) and the README invariants, and exercised the README's named scenarios by static trace (ad-hoc exec was denied; the existing `unittest` suite runs and passes — 3/3 OK, but it covers none of the broken scenarios below).

- **Fresh-ID / same-workspace** (README: *"A fresh operation ID must perform a fresh save, even for the same workspace"*): **Blocked.** The lookup now scans `store.recovery.values()` by `workspace`, so a second distinct `operation_id` on the same workspace matches the first record, skips create+apply, and returns `ok: True` with the caller's new id while the new values are silently dropped.
- **Retry with edited values** (README: *"retried with the same ID and edited values; success means the latest submitted values are active"*): **Blocked.** Apply is gated on `status == "pending"` and replays `record["values"]` captured at creation; the `values` parameter is ignored on every retry, so edited values after a receipt failure never become active.
- **Repeat completed ID returns receipt** (README): **Supported** — hardcoded `{"ok": True, "operation_id": operation_id}` happens to match the receipt shape for the same-id case.
- **Receipt-fail-after-apply retry** (same values): **Supported** — the one scenario the tests cover.

## Findings

### P0 - Critical

(none — impact is severe but scoped to an in-memory preferences store; see P1)

### P1 - High

- **[service.py:2-3]** Recovery lookup keyed by `workspace` instead of `operation_id` → silent data loss for fresh operation IDs
  - Profile: python · Checklist: security-checklist.md (Data Integrity — lost updates) + functional-review
  - Triggered by: content — `.py` extension
  - Trigger/path: `save(store, "w", "op-1", blue)` then `save(store, "w", "op-2", red)`. The second call's `next(... if item["workspace"]=="w")` finds op-1's record → `record is not None` skips creation → `status` is `completed`/`applied` so apply is skipped → returns `{"ok": True, "operation_id": "op-2"}`. Expected: `preferences["w"] == red` and an op-2 record. Actual: `preferences["w"]` stays `blue`, no op-2 record, false success. Every subsequent fresh ID on that workspace is permanently dropped.
  - Consequence: directly violates README (*"fresh operation ID must perform a fresh save, even for the same workspace"*) and (*"latest submitted values are active"*); silent write loss with a success acknowledgement.
  - Confidence: 96% — direct spec contradiction, verified by static trace against `store.py`; the hardcoded return masks it and no test covers it.
  - Suggested fix: revert to `record = store.recovery.get(operation_id)`. This also removes the O(n) scan over the audit-retained (unbounded) recovery table.

- **[service.py:8-9]** `values` parameter ignored on retry → edited values never applied
  - Profile: python · Checklist: security-checklist.md (Data Integrity) + code-quality-checklist.md (boundary) + functional-review
  - Triggered by: content — `.py` extension
  - Trigger/path: with `fail_receipt_once=True`, `save("w","op-1",blue)` applies blue then raises; retry `save("w","op-1",green)` finds the record at `status="applied"`, the `if status=="pending"` guard is false, apply is skipped. Expected `preferences["w"]==green`; actual stays `blue`. Even on the `pending` branch it applies `record["values"]` (original), never the new `values` arg.
  - Consequence: violates README (*"retried with the same ID and edited values; success means the latest submitted values are active"*); silent loss of the user's edited values with a success response. Independent of the first finding — fixing the lookup key alone does not fix this.
  - Confidence: 94% — spec-level contradiction; the `values` argument is provably unused on any existing-record path.
  - Suggested fix: on retry, apply the freshly-submitted `values` (provider is idempotent per README) and update `record["values"]`; don't gate apply solely on `pending`.

### P2 - Medium

(none)

### P3 - Low

- **[service.py:11-12]** `store.receipt(record)` return value discarded; function returns a hardcoded dict built from the `operation_id` parameter rather than the record acted upon
  - Profile: generic · Checklist: —
  - `receipt()` is still called for its side effect (`status="completed"`), so it is not dead code, but discarding its return narrows the contract (the base version returned `store.receipt(record)`), and returning the *parameter* id is what lets the P1 lookup bug report a success for a record it never touched. Also, `receipt()` is now re-invoked on a repeat of an already-completed ID (the base version returned early), which would re-raise if `fail_receipt_once` were set again.
  - Confidence: 70% — partly robustness/style; relevant mainly as the masking mechanism for the P1.
  - Suggested fix: once the lookup is corrected, return `store.receipt(record)` (or return it only when freshly produced) so the response reflects the actual record.

## Areas Not Covered / Residual Risks

- **Mixed-version pending record without a `"values"` key** → `record["values"]` would `KeyError`. Considered and treated as **Not applicable**: README disclaims process restart/persistence, so no pre-change record survives into new code within the modeled in-memory lifecycle.
- **Concurrency / races**: Not applicable — README states the operation is serialized with no threads.
- I did not execute a dynamic repro (ad-hoc Python exec was denied); findings rest on static tracing plus the passing-but-non-covering unit suite.

## Next Steps

I found 3 issues (P0: 0, P1: 2, P2: 0, P3: 1).

Actionable items I recommend fixing:
1. **P1** — `service.py:2-3`: look up the recovery record by `operation_id`, not by scanning for `workspace`.
2. **P1** — `service.py:8-9`: apply the freshly-submitted `values` on retry so the latest edited values win.
3. **P3** — `service.py:11-12`: return the actual receipt instead of a hardcoded dict built from the parameter id.

Items to keep as-is:
- The `"values"`-missing `KeyError` path: false concern under the in-memory, no-restart contract.
- The completed-ID repeat returning `{"ok": True, "operation_id": ...}`: correct per README for the same-id case (once the lookup is fixed).

I'd also suggest adding two regression tests (fresh ID on same workspace; retry with edited values) — the current suite passes while both bugs are present.

**How would you like to proceed?**

1. **Fix all** — implement all three fixes
2. **Fix P1 only** — the two data-integrity bugs
3. **Fix specific items** — tell me which
4. **No changes** — review complete

Please choose an option or provide specific instructions. (I won't change anything until you confirm.)
