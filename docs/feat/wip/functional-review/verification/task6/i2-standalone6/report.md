Cleanup was denied by the sandbox — the harmless scratch file `/tmp/kk-review-code-task6.patch` remains; it's outside the repo and can be deleted manually if desired.

## Done — `patch_settings` updated

**Change** (`settings.py`):
```python
-        result[key] = value or current.get(key)
+        result[key] = value
```
Since `patch` holds only explicitly-supplied keys, assigning each value unconditionally gives exactly the required semantics: **omitted keys keep current values; supplied values — including `None`, `""`, `False` — replace them.** The old `or` fallback was the bug.

**Requirements met:**
- ✅ Omitted keys preserved; falsey supplied values now replace.
- ✅ Caller-owned inputs preserved — `dict(current)` copies; `patch` untouched (verified by test + both reviewers).
- ✅ Existing export preserved — `patch_settings(current, patch)` name/signature unchanged; `cli.py`/`api.py` imports unaffected (now correct).
- ✅ No dependencies added — stdlib only, Python 3.9+ compatible.

**Verification** (`/kk:test`, python profile): added 5 regression tests (falsey-replace subtests, omitted-key preservation, non-mutation, `clear_note`, `update_preferences` disable). `python3 -B -m unittest discover -s tests -v` → **6 tests, OK**. The three falsey-value tests fail against the old `or` logic, so they genuinely guard the fix.

**Review** (`/kk:review-code:isolated`): two independent reviewers → **APPROVE**, no correctness/security/contract issues; one corroborated optional LOW style suggestion (idiomatic dict-merge), declined to keep the diff minimal. No findings to index.

No release/migration/activation prerequisites — this is a pure in-process function; code is complete. The only open item is your call on whether to adopt the one-liner `return {**current, **patch}`.
