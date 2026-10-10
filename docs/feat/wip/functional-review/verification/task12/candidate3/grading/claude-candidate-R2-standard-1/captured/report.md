Findings indexed. Here is the review.

## Code Review Summary

**Files reviewed**: 1 file (`service.py`), 8 insertions / 8 deletions
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: Commit "save recovery update" reworks the `save()` recovery/idempotency logic. Spec source is `README.md` (the behavioral contract); current request is to review the staged change. Selected diff = **staged** (`git diff --cached`); no unstaged changes. No `docs/feat/wip/` → reviewed on its own merits (Task Scope shape 3).
**Baselines**: Review base = commit `feeb199` (`:service.py` ← HEAD `062b8a6`); candidate = staged index blob `0435141`. No separate release baseline. Consumers: `client.submit` → `save`; store contract in `store.py`; tests in `tests/test_save.py`.

## Behavior and Compatibility

The README defines five contracts. I traced each through the candidate against `store.py`:

| Contract | Result |
|---|---|
| #1 Operation identified by caller-supplied `operation_id` | **Blocked** — lookup now keyed by `workspace`, not `operation_id` |
| #2 Failed save retried with **edited** values → latest values active | **Blocked** — apply skipped on retry; edited values lost |
| #3 Repeating a completed ID returns its receipt | Supported (but now re-invokes `receipt`; see P2) |
| #4 A fresh ID performs a fresh save, even for the same workspace | **Blocked** — fresh ID silently ignored; no apply, no record, false success |
| #5 Recovery records remain for audit after completion | **Blocked** — second+ ops on a workspace are never inserted |

The three existing tests (`test_save`, `test_retry_same_values`, `test_completed_id_returns_receipt`) **all pass under the candidate** — but they only exercise a single operation_id per workspace and retry with *identical* values. They do not cover contract #4 (fresh ID, same workspace) or contract #2 with *edited* values, which is exactly where the regressions live. Green tests give false confidence here. *(Source-traced only; I did not execute the suite — Bash is disabled in this session.)*

The review base (`service.py` at `feeb199`) satisfied all five contracts, so every issue below is **introduced** by this diff, not inherited.

---

## Findings

### P0 - Critical

- **[service.py:2-4, 11]** Lookup by `workspace` instead of `operation_id` → silent data loss + false success
  - Profile: python · Checklist: code-quality-checklist.md (Data Integrity / Boundary) + functional-review
  - Triggered by: content — `.py` extension (service.py)
  - **Trigger/path**: Any second, *fresh* operation ID submitted for a workspace that already has a recovery record.
    ```
    save(store, "w", "op-1", {"color":"blue"})   # applies blue, op-1 -> completed
    save(store, "w", "op-2", {"color":"red"})    # BUG
    ```
    In the second call, `next((item ... if item["workspace"] == "w"), None)` returns **op-1's completed record**. `record is None` is false → op-2 is **never inserted**. `record["status"] == "pending"` is false → `store.apply` is **never called**, so `preferences["w"]` stays `{"blue"}`. The function then returns `{"ok": True, "operation_id": "op-2"}`.
  - **Expected vs actual**: Spec #4 — a fresh ID must perform a fresh save. Actual — `{red}` is discarded, op-2 is absent from recovery (violates #5), and the caller is told op-2 succeeded (false success). Also violates identity contract #1.
  - **Consequence**: Silent, unrecoverable preference data loss with a success receipt handed back to the client. High exploitability (ordinary second save) × high impact (lost writes).
  - Confidence: 97% — direct trace against `store.py`; the generator unambiguously filters by workspace.
  - **Suggested fix**: Restore id-keyed lookup: `record = store.recovery.get(operation_id)`. (This also removes the O(n) scan — see P3.)

### P1 - High

- **[service.py:8-10]** Edited-values retry after a failed receipt never re-applies → latest values not active
  - Profile: python · Checklist: code-quality-checklist.md (Error Handling / Data Integrity) + functional-review
  - Triggered by: content — `.py` extension (service.py)
  - **Trigger/path**: First attempt applies values then `receipt` raises `ReceiptUnavailable` (store models exactly this boundary), leaving `status == "applied"`. Retry with the same ID and *edited* values:
    ```
    store.fail_receipt_once = True
    try: save(store, "w", "op-1", {"color":"blue"})   # applies blue, receipt raises
    except ReceiptUnavailable: pass
    save(store, "w", "op-1", {"color":"green"})        # edited retry
    ```
    Retry finds the record, `status == "applied"` (not `"pending"`) → `store.apply` is skipped; `record["values"]` was captured as `{blue}` at creation and is never updated. `preferences["w"]` stays `{blue}`.
  - **Expected vs actual**: Spec #2 — "success means the latest submitted values are active." Actual — `{green}` is silently dropped; the stale `{blue}` remains while the call reports success.
  - **Consequence**: The core retry-with-edits promise is broken; silently wrong persisted state. `test_retry_same_values` passes only because it retries with identical values.
  - Confidence: 95% — two interacting defects: the `status == "pending"` apply-gate (a failed attempt leaves `"applied"`) and applying stored `record["values"]` rather than the freshly submitted `values`.
  - **Suggested fix**: On retry, apply the freshly submitted `values` (the provider is idempotent) and update the stored values, rather than gating on a terminal status. E.g. apply whenever status is not `"completed"`, using the incoming `values`.

### P2 - Medium

- **[service.py:10-11]** `store.receipt()` return value discarded; hardcoded return + receipt re-invoked on completed repeats
  - Profile: python · Checklist: solid-checklist.md (DIP / intent) + functional-review
  - Triggered by: content — `.py` extension (service.py)
  - The base returned `store.receipt(record)` (receipt keyed to `record["operation_id"]`). The candidate ignores that return and emits `{"ok": True, "operation_id": operation_id}` using the *passed-in* id — which, combined with the P0 lookup, can name an operation that was never processed. Additionally, repeating a completed ID now calls `receipt()` again (base returned early without re-calling it); if `fail_receipt_once` were re-armed, a completed-ID repeat would raise `ReceiptUnavailable` instead of returning the receipt (contract #3 edge).
  - Confidence: 88% — behavior change is clear from the diff; the re-arm edge is a secondary scenario.
  - **Suggested fix**: Return the receipt produced by `store.receipt(record)` so the response reflects the record actually acted upon.

### P3 - Low

- **[service.py:2-3]** O(n) linear scan over `store.recovery` replaces O(1) dict lookup
  - Profile: python · Checklist: code-quality-checklist.md (Performance)
  - The `next(... for item in store.recovery.values() ...)` scan is O(recovery size) per save and is also the wrong key. Fixing P0 (`store.recovery.get(operation_id)`) resolves both correctness and performance.
  - Confidence: 92%.

---

## Removal/Iteration Plan

No dead/removable code introduced. The net effect of P0+P1 fixes is essentially to restore the base's id-keyed lookup and unconditional-apply structure while keeping any intended recovery-record retention.

## Additional Suggestions

- Add regression tests for the two uncovered contracts: (a) fresh ID on an already-saved workspace applies the new values and records the new op; (b) failed-receipt retry with **edited** values makes the edited values active. Both currently pass vacuously because they aren't tested.

**Coverage & limits**: Reviewed `service.py` against `README.md`, `store.py`, `client.py`, and `tests/test_save.py`. Traced all five README contracts by hand. I did **not execute** the test suite (Bash disabled this session) — findings are source-trace-based; the traces are deterministic against the in-memory store. No concurrency assessed (README explicitly scopes out threads/restart/network).

**Indexed**: 2 systemic P0/P1 patterns recorded to `kk:review-findings` (wrong-key idempotency lookup; apply-gated-by-terminal-status breaking retry).

---

## Next Steps

I found 4 issues (P0: 1, P1: 1, P2: 1, P3: 1).

Actionable items I recommend fixing:
1. **P0** — restore `store.recovery.get(operation_id)` as the lookup key (fixes data loss, false success, missing audit records, and the O(n) scan).
2. **P1** — re-apply the freshly submitted `values` on retry instead of gating on `status == "pending"`.
3. **P2** — return `store.receipt(record)` rather than a hardcoded dict.
4. Add the two missing regression tests.

Items to keep as-is:
- P3 is subsumed by the P0 fix — no separate work needed.

**How would you like to proceed?**

1. **Fix all** — implement all suggested fixes
2. **Fix P0/P1 only** — address the critical and high-priority data bugs
3. **Fix specific items** — tell me which
4. **No changes** — review complete

Note: given how close the candidate is to the (correct) review base, the simplest safe fix for P0+P1 is largely a revert of the lookup and apply-gating changes. I won't change anything until you confirm.
