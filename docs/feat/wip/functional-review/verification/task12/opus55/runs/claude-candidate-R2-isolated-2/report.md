## Isolated review: save recovery update (staged `service.py`)

**Verdict: changes requested.** The staged `save()` breaks two of the README's recovery rules (README.md:5-9). In both cases the caller gets `ok: True` but the new preferences are never applied.

**Review limits:**
- **Only one reviewer ran.** The PAL server failed to connect this session, so there was no external second opinion, and none of the findings below count as corroborated by two reviewers. I traced both main bugs through the source myself and they hold up. If you want the second opinion, reconnect PAL and rerun.
- **No diff or tests.** Bash was denied, so I couldn't produce the diff, read the HEAD (`feeb199`) version of `service.py`, or run the tests. Everything below comes from reading the current 12-line `service.py`, which matches what you staged, against `client.py`, `store.py`, `tests/test_save.py` and the README. I can't say whether these bugs were introduced by this change or already existed; the verdict doesn't depend on that.

### What works and what doesn't
| Scenario (README) | Result |
|---|---|
| First save | Works (`test_save`) |
| Receipt fails, then retry with the same ID and same values | Works (`test_retry_same_values`) |
| Retry with the same ID and **edited** values | **Fails**: old values stay active |
| Fresh operation ID for the same workspace | **Fails**: the save is silently dropped |
| Repeat a completed ID | Returns its receipt, but raises if the receipt store is down |
| Audit records kept after completion | Partly fails: new IDs get no record |
| Callers (`client.submit`, tests) | Signature and return shape unchanged |

### Findings

**P1: records are looked up by workspace but stored by operation ID** (`service.py:2-3, 7, 12`, 95% confidence)
- **What happens:** after the first save to a workspace, a call like `submit(w, "op-2", red)` finds op-1's record, so it never calls `apply`. It writes op-1's receipt again and returns `ok` with `operation_id: "op-2"`. Preferences stay blue and no op-2 record exists.
- **Same thing when op-1's receipt failed:** op-2's values are dropped and op-1 gets marked completed.
- **Reusing an ID for a different workspace** overwrites the existing audit record.
- **Fix:** look up with `store.recovery.get(operation_id)` and return what `store.receipt(record)` returns.

**P1: retrying with edited values reports success but keeps the original values** (`service.py:8-9`, 95% confidence)
- After a receipt failure the record is left as `"applied"`, so a retry skips `apply`.
- Even while a record is pending, it applies the values stored on the first attempt and ignores the new ones.
- The only retry test resubmits identical values, so it can't catch this.

**P3: repeating a completed ID writes the receipt again** (`service.py:11`, 70% confidence)
- If the receipt store is down, that repeat raises instead of just returning the receipt.

**Suggested fix (the reviewer traced it against every scenario above):**
```python
record = store.recovery.get(operation_id)
if record is not None and record["status"] == "completed":
    return {"ok": True, "operation_id": record["operation_id"]}
if record is None:
    record = {"operation_id": operation_id, "workspace": workspace,
              "status": "pending", "values": dict(values)}
    store.recovery[operation_id] = record
else:
    record["values"] = dict(values)  # latest submitted values win
store.apply(workspace, record["values"])
record["status"] = "applied"
return store.receipt(record)
```
The provider's write is an idempotent replace (README:11), so re-applying any record that isn't completed is safe. That makes the `"applied"` check unnecessary. Tests are also needed for:
- a fresh ID on the same workspace;
- a fresh ID after a failed receipt;
- a retry with edited values.

### Other notes
- I added both P1 patterns to the `kk:review-findings` knowledge base, which was empty before this review.
- No temporary files were created, so there was nothing to clean up.

Do you want me to apply the fix and add the three tests? You'll need to run the test suite yourself or allow Bash, because I can't run it with Bash denied.
