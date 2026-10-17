## Code Review Summary

**Files reviewed**: 1 file (`service.py`), 16 lines changed (+8/−8)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: The README defines what save must do. Save is keyed by operation ID. A failed save can be retried with the same ID and edited values, and success means the latest values are active. Repeating a completed ID returns its receipt. A fresh ID must do a fresh save. Recovery records stay for audit. There are no feature docs or task files, so there's no task scope. I reviewed the diff on its own merits against the README.
**Baselines**: The base is `HEAD` (`feeb199`). The candidate is the staged `service.py`; there are no unstaged changes, so the working tree matches it. There's no separate release baseline.

## Behavior and Compatibility

I read `README.md`, `store.py`, `client.py` (calls `save` directly), `tests/test_save.py` and the base `service.py`. **Executed:** `python3 -B -m unittest discover -s tests` passed all 3 tests. **Not executed:** my scenario script was denied permission, so the rows below come from reading the code, not from running it.

| Scenario (README) | Base `HEAD` | Candidate |
| --- | --- | --- |
| First save of `op-1` | applies the values, ok | applies the values, ok (tested) |
| Receipt fails, retry `op-1` with the same values | re-applies, ok | ok (tested) |
| Receipt fails, retry `op-1` with **edited** values | applies the new values | **old values stay active, returns ok** |
| Repeat a completed `op-1` | returns the receipt without side effects | calls `store.receipt` again; **raises if the receipt store is down** |
| Fresh `op-2` on the same workspace after `op-1` completed | fresh save | **no save, no `op-2` record, returns ok** |

- **Version compatibility:** Not applicable. The store is in memory only and the README promises no restart or mixed-version records.
- **Existing tests:** none of the three cover the failing rows.

---

## Findings

### P0 - Critical
(none)

### P1 - High

- **[service.py:2]** A fresh operation ID reuses the workspace's old record, so the new values are dropped
  - Profile: python · Checklist: security-checklist.md (Data Integrity)
  - Triggered by: content — `.py` extension
  - **Trigger:** `save(s,"w","op-1",{c:blue})`, then `save(s,"w","op-2",{c:red})`.
  - **What happens:** line 2 searches by workspace and finds the completed `op-1` record, which is kept for audit. That record isn't `pending`, so the apply is skipped and the old record is passed to `store.receipt`. The call returns `{"ok": True, "operation_id": "op-2"}` while the preferences are still `blue`, and no `op-2` record is created.
  - **Expected:** a fresh save that applies `red`, as the base does via `store.recovery.get(operation_id)`.
  - **Also:** reusing an ID on another workspace overwrites the earlier workspace's audit record at line 6.
  - Confidence: 95% — the path is straightforward and the README states the rule outright. The script that would have demonstrated it was denied.
  - **Fix:** look the record up by `operation_id`, as the base does.

- **[service.py:7-10]** Retrying after a receipt failure ignores edited values but reports success
  - Profile: python · Checklist: security-checklist.md (Data Integrity / idempotent retry)
  - Triggered by: content — `.py` extension
  - **Trigger:** set `fail_receipt_once`, then `save(op-1, blue)` raises `ReceiptUnavailable` with the status left at `applied`. Then retry `save(op-1, red)`.
  - **What happens:** the status is `applied`, so the apply is skipped. The receipt then completes and the call returns ok, but `blue` is still active. If the status were still `pending`, line 8 would apply the stored first-attempt values, also ignoring `red`.
  - **Expected:** the README requires that "success means the latest submitted values are active". The base re-applies `values` and updates `record["values"]` on every attempt that isn't complete, which is safe because the provider is idempotent.
  - Confidence: 95% — this is exactly the failure boundary the README describes.
  - **Fix:** on any attempt that isn't complete, apply the incoming `values` and update `record["values"]`. Don't skip the apply because the status is `applied`.

### P2 - Medium

- **[service.py:11-12]** Repeating a completed ID now goes through `store.receipt` again
  - Profile: generic · Checklist: —
  - Triggered by: —
  - **What happens:** the base returned early for completed records. The candidate calls `store.receipt(record)` every time and then discards its return value. If the receipt store is unavailable, repeating a completed `op-1` raises `ReceiptUnavailable` instead of returning its receipt.
  - **Consequence:** it can be recovered by retrying, but it breaks the documented completed-ID behavior and adds an unneeded write.
  - Confidence: 85% — the path is clear. Real-world impact depends on how often the receipt store is down.
  - **Fix:** restore the early `completed` return.

---

## Removal/Iteration Plan

The base `service.py` already meets every README row above, as far as I could trace it. The simplest fix is to unstage this change, or keep the base's structure. If the update was meant to address something else, that goal isn't documented and I couldn't confirm it. Whichever fix you choose, add tests for:
- a fresh ID on the same workspace
- an edited-value retry after a receipt failure
- a repeated completed ID while the receipt store is down

**Coverage limits:**
- The scenario script was denied permission, so those rows come from reading the code.
- The knowledge base had no earlier findings.
- I didn't assess concurrency, because the README rules out threads.

**Indexed:** two systemic P1 patterns under `kk:review-findings`: looking up the idempotency record by the wrong key, and a retry that keeps the first attempt's values.

I haven't changed anything, since this was a review only. Should I apply the fixes, or restore the base logic and add those three tests?
