Both independent reviewers confirmed the finding against the actual released-provider source. Indexing done. Here is the merged report.

---

## Review Summary (Isolated Mode)

**Reviewers**: `kk:code-reviewer` sub-agent (Opus) and PAL `codereview` (gemini-3.1-pro-preview). Both succeeded. PAL continuation embedded **13 files (fully_embedded)**; the sub-agent inspected the released-provider blob directly — source receipt verified for both, so corroboration is real, not assumed.
**Files reviewed**: `client.py` (+3/−1), `tests/test_client.py` (+1/−1) — staged index blobs.
**Overall assessment**: **REQUEST_CHANGES** (release-blocking).
**Intent and scope**: Task 1 "Client receipt handling" (status: done). Design intent (authoritative): *"Ordinary saves must continue to work with the supported provider at eval-release… Add an application receipt… while preserving independently releasable main."* Task 2 (provider receipts, separate repo, pending) is correctly **out of scope** and not flagged as missing.
**Baselines**: Review base = HEAD `ac09e55`. Compatibility baseline = released provider `provider/settings.py` @ `2214073` (blob `a6aeedb`, complete file) — returns `{"ok": True}`, **no `applied` key**. (Provider source was removed at review base to simulate the separate repo; retrieved from history as evidence.)

### Behavior and Compatibility
Traced `save_settings` with the released provider as the `send` implementation:
- Client now sends `require_receipt: True` (harmless — old provider ignores unknown keys) and then raises `RuntimeError` unless `response.get("applied") is True`.
- Released provider returns `{"ok": True}` → `response.get("applied")` is `None` → `None is not True` → **raises every time**.
- The check is **unconditional** — not gated by `enhanced_settings`, so even with the enhanced UI off (the default ordinary-save path) it fails.

| Combination | Verdict |
|---|---|
| new client / **old released provider**, ordinary saves (enhanced off) | **Blocked** — demonstrated incompatibility vs. baseline `2214073` |
| new client / new provider (Task 2) | Not applicable — out of scope; cannot excuse the current regression |

### Corroborated Findings

- **[client.py:5-6]** Unconditional `applied` receipt check breaks all ordinary saves against the released provider ⟨**corroborated — P0 / CRITICAL**⟩
  - Profile: python · Checklist: code-quality (Boundary Conditions — None-vs-missing) · Triggered by: `.py`
  - **code-reviewer (P0, 99%)**: With the released provider's `{"ok": True}`, `response.get("applied") is not True` → raises `RuntimeError("Provider did not acknowledge applied settings")`. Not gated by `enhanced_settings`, so 100% of ordinary saves fail if this ships on main before Task 2. Directly violates the hard *independently-releasable-main* requirement (also cited README: *"Every merged client increment must support the released provider at tag `eval-release`… while `enhanced_settings` is false"*).
  - **PAL (CRITICAL, client:5)**: "Deploying this client to `main` before the provider will crash all ordinary saves… directly violates… preserving independently releasable main." Suggested gating the check behind `enhanced_settings`.
  - **Fix direction**: treat a missing `applied` as "provider predates receipts → success" (reject only on explicit `applied is False`), or gate the strict assertion behind the feature capability Task 2 introduces. Sending `require_receipt` is itself safe; the hard client-side assertion is the breaking element.

- **[tests/test_client.py:8]** Edited test uses the *future* provider shape, masking the regression ⟨**corroborated — P2 / MEDIUM**⟩
  - **code-reviewer (P2, 95%)**: Fake `send` now returns `{"ok": True, "applied": True}` — the Task 2 shape. Green here does not prove the required old-provider combination (which fails). No test covers `{"ok": True}` or the new `RuntimeError` path.
  - **PAL (MEDIUM, test:7)**: Same — add a test mocking the legacy `{"ok": True}` response with `enhanced_settings=False` to guarantee backward compatibility.

### External Review Findings (PAL, native — not independently corroborated)
- **[client.py:2] LOW** — `require_receipt: True` is sent unconditionally. Harmless (provider ignores unknown keys) but cleaner to include only when `enhanced_settings` is on, to isolate the feature's behavior.
  - *Author context (from code-reviewer):* confirmed harmless against the released snapshot; the breaking element is the client-side assertion, not this payload key.
- PAL positive notes: strict `is not True` avoids truthiness bugs; existing `ok` error-handling preserved; `enhanced_settings` default is a safe foundation for flag-gating.

### Outstanding Evidence and Prerequisites
- The hard requirement *independently releasable main / ordinary saves must keep working with the supported provider at `eval-release`* is **unmet** by this increment. A pending Task 2 provider does **not** satisfy it (README: *"a pending provider task cannot change the supported baseline"*). Must be fixed in the client increment itself before main is independently releasable, unless you record an explicit exception to the delivery constraint.
- No evidence requests outstanding — the decisive baseline (`provider/settings.py` @ `2214073`) was supplied and is sufficient. No runtime execution performed (none available/required); conclusions are deterministic at source level.

**Indexed**: one systemic `kk:review-findings` entry (backward-incompatible unconditional contract enforcement vs. independently-releasable-main; missing-key-treated-as-false; test masking via future provider shape).

---

### Next steps — how would you like to proceed?
1. **Fix the P0** (make missing `applied` a success / gate the strict check behind `enhanced_settings`) + add the legacy-provider regression test — I can draft it.
2. Fix P0 + both corroborated findings and the LOW payload-gating cleanup.
3. Record an explicit exception to the independently-releasable-main constraint (not recommended) and leave as-is.
4. No changes — review only.

I haven't modified any source. The temp evidence bundle is at `/tmp/kk-review-enhsettings.ZYSga0/` — I'll remove it once you've decided (retaining it in case you want a fix drafted against the same baseline).
