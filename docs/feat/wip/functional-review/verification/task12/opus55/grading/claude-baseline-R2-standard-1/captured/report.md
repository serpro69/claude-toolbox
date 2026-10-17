# Code review: staged save-recovery change in `service.py`

I recommend requesting changes before merging. All 3 tests pass, but the change breaks two promises in the README and loses user data without any error. I checked each problem by running it against the real `Store`.

**Scope:** `service.py`, 8 lines added and 8 removed. I also read `store.py`, `client.py`, `tests/test_save.py` and `README.md`, which is where the save rules are written down. The Python profile's four checklists were applied (security, SOLID, code quality, removal); they're under `plugins/kk/profiles/python/review-code/`. I wasn't allowed to read `$TOOLBOX_PLUGIN_ROOT`, so I assumed the plugin folder is `plugins/kk`, the folder that contains this skill.

## P0: Critical

**1. A new operation ID on the same workspace saves nothing (`service.py:2`)**
- Profile: python · Checklist: `security-checklist.md` (data integrity) · Triggered by: file extension `.py`
- The code now finds the recovery record by workspace instead of by operation ID. The README says finished records are kept for audit, so the next save on that workspace always finds the old finished record. It then skips `store.apply` and returns `ok: True` with the new ID.
- This breaks the README rule that "a fresh operation ID must perform a fresh save, even for the same workspace." No recovery record is created for the new ID either.
- What happened when I ran it: I saved `op-1` with `{"color": "blue"}`, then `op-2` with `{"color": "red"}`. `op-2` returned `{'ok': True, 'operation_id': 'op-2'}`, but the stored preference stayed `{'color': 'blue'}` and `recovery` only held `['op-1']`.
- Confidence: 98%. I reproduced it, and the README states the rule directly.
- Fix: go back to `store.recovery.get(operation_id)`.

**2. Retrying with edited values keeps the old values (`service.py:6`, `:8`)**
- Profile: python · Checklist: `security-checklist.md` (data integrity, idempotency) · Triggered by: file extension `.py`
- Values are now stored only when the record is first created. Also, `apply` only runs while the status is `"pending"`. If the receipt fails after the values were applied, the status is already `"applied"`, so a retry never applies again. Even if it did, it would use the stale values from the first attempt.
- This breaks the README rule that a failed save "can be retried with the same ID and edited values; success means the latest submitted values are active."
- What happened when I ran it: the first save of `blue` failed at the receipt step. Retrying `op-1` with `green` returned `ok: True`, but the stored preference stayed `{'color': 'blue'}`.
- Confidence: 97%. I reproduced it. The old code handled this correctly.
- Fix: on any retry that hasn't finished, set `record["values"] = dict(values)` and call `apply` again. The README says applying the same values twice is safe, so the `"pending"` check isn't needed.

## P1: High

**3. Repeating a finished ID now calls the receipt store again and can fail (`service.py:11`)**
- Profile: python · Checklist: `code-quality-checklist.md` (error handling) · Triggered by: file extension `.py`
- The old code returned right away for a finished ID. The new code calls `store.receipt` every time, so if the receipt store is down, repeating a finished operation raises an error.
- What happened when I ran it: `op-1` finished, then I turned on the receipt failure and repeated `op-1`. It raised `ReceiptUnavailable`, which breaks the README rule that "repeating a completed ID returns its receipt."
- Confidence: 92%. I reproduced it, but whether it shows up in practice depends on how often the receipt store fails.
- Fix: return early when the status is `"completed"`, as the old code did.

## P2: Medium

**4. The function ignores the receipt and builds its own result (`service.py:12`)**
- Profile: generic · Checklist: — · Triggered by: —
- What `store.receipt()` returns is thrown away, and the result is built from the caller's `operation_id`. Combined with finding 1, this reports success for an ID that was never recorded. It also means the reply no longer matches whatever the receipt store returns.
- Confidence: 85%.
- Fix: `return store.receipt(record)`.

**5. Every save now scans all recovery records (`service.py:2`)**
- Profile: python · Checklist: `code-quality-checklist.md` (performance) · Triggered by: file extension `.py`
- Records are kept for audit, so this list keeps growing, and each save now walks through all of it. Before, finding a record was a single direct lookup by ID. The fix for finding 1 also fixes this.
- Confidence: 90%.

## P3: Low

**6. The tests miss the cases that broke**
- Profile: generic · Checklist: — · Triggered by: —
- None of the 3 tests covers a new ID on the same workspace, a retry with edited values, or repeating a finished ID while the receipt store is down. That's why all three regressions pass.
- Fix: add one test for each, using the three runs above.

## Suggested fix

The previous version already met every README rule. The smallest correct change is to restore it and keep values set on each retry:

```python
def save(store, workspace, operation_id, values):
    record = store.recovery.get(operation_id)
    if record is not None and record["status"] == "completed":
        return {"ok": True, "operation_id": operation_id}
    if record is None:
        record = {"operation_id": operation_id, "workspace": workspace,
                  "status": "pending"}
        store.recovery[operation_id] = record
    record["values"] = dict(values)
    store.apply(workspace, record["values"])
    record["status"] = "applied"
    return store.receipt(record)
```

There was no code to remove. I saved findings 1 and 2 to the `kk:review-findings` knowledge base as repeat-worthy patterns: finding saved records by the wrong key, and retries keeping the first attempt's values.

---

## Next steps

I found 6 issues (P0: 2, P1: 1, P2: 2, P3: 1). I recommend fixing all of them; the suggested fix plus three new tests covers everything.

**How would you like to proceed?**
1. **Fix all**: apply the suggested fix and add the three tests
2. **Fix P0/P1 only**
3. **Fix specific items**
4. **No changes**
