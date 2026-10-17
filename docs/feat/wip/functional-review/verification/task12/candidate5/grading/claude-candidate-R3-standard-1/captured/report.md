Finding indexed. Here is the review.

---

## Code Review Summary

**Files reviewed**: 2 files, 4 insertions / 2 deletions (`client.py`, `tests/test_client.py`)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: Requirement source — `docs/feat/wip/enhanced-settings/{design,implementation,tasks}.md` + `README.md`. Current request — Task 1 of *enhanced-settings*: add client-side application-receipt handling plus its unit test. Selected diff — **staged** (`git diff --cached`); no unstaged changes. Candidate state — Task 1 `done`; Task 2 (provider receipts, separate repo) `pending` and correctly out of scope.
**Baselines**: Review base/candidate = staged worktree on `master`. Separate **release baseline** = supported provider `provider/settings.py` at Git tag `eval-release` (retained in local Git; inspected directly). No live environment (none required per README).
**Profiles**: `python` active → applied security, SOLID, code-quality, removal checklists. KB cold-start (empty), no prior findings correlated.

## Behavior and Compatibility

I traced the one changed entry point, `save_settings`, against the only supported provider the delivery contract names.

| Contract/source | Initial state | Operation | Expected | Candidate result | Evidence |
|---|---|---|---|---|---|
| README + design.md (ordinary save must work vs `eval-release`, `enhanced_settings=False`) | released provider `update_settings` returns `{"ok": True}` | `save_settings(send, "w", {...}, enhanced_settings=False)` | `{"saved": True, "enhanced": False}`, values applied, caller sees success | **`RuntimeError("Provider did not acknowledge applied settings")`** — `response.get("applied")` is `None`, `None is not True` | `git show eval-release:provider/settings.py` (confirmed: no `applied` key, `require_receipt` ignored) |
| design.md (new provider, Task 2) | provider returns `{"ok": True, "applied": True}` | same | success | success | diff-only; provider not yet implemented |

**Compatibility conclusions:**
- **New-client / released-provider (`eval-release`): Blocked.** Demonstrated incompatibility. The new `applied` check is unconditional (runs regardless of `enhanced_settings`), so it breaks *all* ordinary saves against the supported provider — the exact flow the design says must keep working. Notably the released provider persists the values *before* returning, so this is a false-negative: data is written but the caller sees failure, violating README's definition of a successful save.
- **Independently-releasable main: Blocked.** This client increment cannot ship on its own against the supported baseline; it implicitly requires the pending Task 2 provider. That is a hard delivery-requirement violation, not merely a rollout ordering note.
- `require_receipt: True` addition alone — **Not applicable/harmless**: the old provider ignores unknown request keys.

**Evidence limits**: The `send` adapter wiring (client→provider transport) is injected, not in this repo; I assessed against the provider *source* the contract names as the baseline. Conclusion holds for that contract.

---

## Findings

### P0 - Critical

(none — the regression is serious but recoverable by revert and does not cause irreversible loss; see P1)

### P1 - High

- **[client.py:5]** Unconditional `applied` receipt check breaks ordinary saves against the supported released provider
  - Profile: python · Checklist: functional-review / code-quality (boundary: None handling)
  - Triggered by: delivery-contract trace — `.py` content signal; baseline `provider/settings.py @ eval-release`
  - Trigger/path: any `save_settings(...)` call (even `enhanced_settings=False`) routed to the `eval-release` provider → provider returns `{"ok": True}` → `response.get("applied")` is `None` → `None is not True` → raises. Expected: success with values applied. Consequence: every settings save against the only supported provider throws, while the values are silently persisted on the provider side (false-negative, likely to trigger caller retries). Violates design.md ("ordinary saves must continue to work… while enhanced_settings is false") and README ("successful save = values applied and caller sees success" + independently-releasable-main).
  - Confidence: 90% — provider baseline confirmed via `git show`; contract is explicit. Residual: `send` transport is injected and not in-repo, but the contract names the provider source as the baseline.
  - Suggested fix: reject only on an *explicit* negative so a missing field means "legacy provider, backward-compatible success":
    ```python
    if response.get("applied") is False:
        raise RuntimeError("Provider did not acknowledge applied settings")
    ```
    Old provider (`None`) → passes; new provider that applied (`True`) → passes; new provider that rejected (`False`) → raises. Alternatively, negotiate the receipt via a capability/flag so the strict check only engages when the provider opts in.

### P2 - Medium

- **[tests/test_client.py:8]** Test mock simulates the unreleased future provider, masking the regression
  - Profile: python · Checklist: functional-review (test binding) / test-patterns
  - Triggered by: diff — mock changed to `{"ok": True, "applied": True}`
  - Trigger/path: the only success test now returns `applied: True`, a shape **no supported provider emits today** (it matches pending Task 2, not `eval-release`). The suite stays green while the real supported combination is broken — the test gives false confidence and is why the P1 slipped through. Consequence: no regression signal for the actual delivery contract.
  - Confidence: 85% — direct from diff + baseline comparison.
  - Suggested fix: keep a test that exercises the **`eval-release` provider shape** (`{"ok": True}`, no `applied`) and asserts an ordinary save still succeeds. With the P1 fix applied this test passes; without it, it fails — exactly the guard this increment needs. Add the `applied: True` case as a separate (future-provider) test.

### P3 - Low

(none)

---

## Removal/Iteration Plan

No removal candidates. The only iteration work is the two fixes above; both are tied to the demonstrated incompatibility, not speculative.

**Coverage / areas not covered**: Security checklist — no injection/deserialization/secret/crypto surface in this diff (request is a plain dict; no shell/eval/pickle). SOLID — `save_settings` remains a single small cohesive function; no new violations. I did **not** execute the test suite (review-only) and did **not** inspect the injected `send` transport (not in repo). Task 2 provider work is correctly out of scope and not flagged as missing.

---

## Next Steps

I found 2 issues (P0: 0, P1: 1, P2: 1, P3: 0).

The actionable items I recommend fixing:
1. **P1 — client.py:5**: change the receipt check to reject only on explicit `applied is False`, restoring backward-compat with the `eval-release` provider.
2. **P2 — tests/test_client.py:8**: add/restore a test against the supported provider shape (no `applied` key) so the regression is caught; keep the `applied: True` case as a future-provider test.

Items I recommend keeping as is:
- Sending `require_receipt: True` in the request: harmless against the old provider (ignores unknown keys) and forward-compatible with Task 2.

**How would you like to proceed?**

1. **Fix all** — I'll implement both fixes
2. **Fix P1 only** — address the compatibility break
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

Please choose an option or provide specific instructions. (I won't change anything until you confirm.)
