I'm requesting changes: the staged `service.py` change breaks the save contract described in the README in two serious ways.

**Scope and how I checked it**
- **What was reviewed:** the staged diff only (`git diff --cached`): 1 file, 8 lines added and 8 removed. I compared it with `HEAD` (`feeb199`). There were no unstaged changes.
- **Requirements used:** `README.md` defines the save contract. There are no task documents, so there was no task scope to apply.
- **Checklists:** Python was the only profile that matched. I applied its four review checklists plus the general method.
- **Tests:** the existing suite passes (3 tests, OK).
- **Scenarios:** I asked to run a script exercising the scenarios below and the request was denied. Every scenario result here comes from reading the code, not from running it.
- **Other files read:** `store.py`, `client.py` and `tests/test_save.py`, all unchanged.

## How each README requirement fares

| README requirement | Before | After |
|---|---|---|
| A new save works | ✅ | ✅ |
| A retry with the same ID and same values succeeds after the receipt write fails | ✅ | ✅ |
| A retry with the same ID and **edited** values makes the latest values active | ✅ re-applies the new values | ❌ the original values stay active |
| A fresh operation ID performs a fresh save on the same workspace | ✅ | ❌ the save is skipped but success is returned |
| Repeating a completed ID returns its receipt | ✅ no write | ⚠️ writes the receipt again, so it can fail |
| Recovery records remain available for audit | ✅ | ❌ reusing an ID on another workspace overwrites the old record |

- **Data compatibility:** not applicable. The store is in-memory and the README promises no restart or persistence, so no older records can be in a different shape.
- **Test coverage:** none of the 3 tests covers edited-value retries, fresh IDs on a used workspace, or reusing an ID on a different workspace. That is why the suite still passes.

---

## Findings

### P1: Lookup by workspace instead of operation ID silently drops later saves (`service.py:2`)
- **What happens:** the record is now found by matching the workspace. Completed records are kept for audit, so after the first save, every later save to that workspace finds the old record. Its status is `completed`, so the apply step is skipped.
- **Example:** save `op-1` with `{"color": "blue"}` on workspace `w`, then save `op-2` with `{"color": "red"}`. The second call returns `{"ok": True, "operation_id": "op-2"}`, but the preferences stay blue and no `op-2` record is created. Each workspace effectively accepts only one save, and the client is told the later ones succeeded.
- **Second example:** reuse the completed `op-1` for workspace `x`. Nothing matches `x`, so the code writes a new record under `op-1`, which overwrites `w`'s audit record and applies new values. The old code returned the existing receipt.
- **Confidence:** 95%. I traced each step against `store.py` (records are never removed). I didn't run it because the reproduction was denied.
- **Fix:** go back to `record = store.recovery.get(operation_id)`, and return the existing receipt without writing when its status is `completed`.

### P1: Retrying with edited values keeps the first attempt's values (`service.py:6`, `service.py:8`)
- **What happens:** the values are stored only when the record is created, and the apply step only runs while the status is `pending`. The case the README describes is a receipt write that fails after the values were applied. That leaves the record at `applied`, so a retry skips the apply step.
- **Example:** with the receipt write set to fail once, `op-1` saves blue and raises `ReceiptUnavailable`. Retrying `op-1` with red returns ok, but the preferences stay blue. The README says success means "the latest submitted values are active."
- **This stays broken after fixing the lookup:** the stale values and the `pending`-only check cause it on their own.
- **Confidence:** 95%. I traced it through `Store.apply` and `Store.receipt`.
- **Fix:** for any record that isn't `completed`, set `record["values"] = dict(values)` and call `store.apply(workspace, values)` every time. The README says the provider applies values idempotently, so applying them again is safe.

### P2: Repeating a completed ID writes the receipt again and can now fail (`service.py:11`)
- **What happens:** `store.receipt(record)` now runs on every call, including for completed records. Before, a completed ID returned its receipt without touching the receipt store.
- **Example:** after `op-1` completes, set the receipt write to fail once and repeat `op-1`. The call raises `ReceiptUnavailable` instead of returning the receipt the README promises.
- **Confidence:** 85%. This is a narrower availability problem and doesn't corrupt any data.
- **Fix:** return early for completed records, as the old code did. Then return the result of `store.receipt(record)` rather than building the response by hand.

The simplest correct version is essentially the code before this change. If the update was meant to achieve something the old code doesn't, that goal isn't stated in the README or anywhere else in the repo.

Add tests for:
- a retry with edited values after a receipt failure
- a fresh ID on an already-used workspace
- a repeated completed ID while the receipt write is failing
- reusing an ID on a different workspace

---

- **Knowledge base:** no earlier review notes were found. I saved both P1 issues as general patterns for future reviews.
- **Not covered:** I couldn't run the scenarios, so the examples above haven't been executed. The README promises no concurrency, so I didn't assess it.

I haven't edited anything. Want me to apply these fixes and add the tests?
