Both independent reviewers (Claude `code-reviewer` sub-agent and pal `gemini-3.1-pro-preview`) completed and converged on the same three issues. Here's the consolidated report.

---

## Review Summary (Isolated Mode)

**Reviewers**: code-reviewer (Claude sub-agent), pal codereview (`gemini-3.1-pro-preview`)
**Files reviewed**: 2 files, 6 lines changed (`client.py`, `tests/test_client.py`)
**Scope**: mid-implementation — Task 1 *(Client receipt handling, done)* in scope; Task 2 *(Provider receipts, pending, separate repo)* out of scope
**Note on method**: Bash is disabled in this session, so I captured the staged diff with a single read-only `git` call and wrote the patch file for pal via the Write tool instead of the usual `mktemp` pipeline. Both reviewers ran normally. (The temp patch `/tmp/kk-review-code-isolated2.patch` could not be auto-removed — delete it at your leisure.)

All three findings were flagged independently by **both** reviewers — highest signal.

---

### Corroborated Findings

**1. [client.py:5-6] Unconditional receipt enforcement breaks ordinary saves against the deployed provider** ⟨corroborated⟩ — **P0 / CRITICAL**
- Profile: generic (spec-contract) · also code-quality error-handling
- `save_settings` now raises `RuntimeError("Provider did not acknowledge applied settings")` whenever `response.get("applied") is not True`. The provider that *emits* `applied` is **Task 2 — pending, separate repo, not yet released**. The provider deployed today returns `{"ok": True}` with no `applied` key → `None is not True` → `True` → **every ordinary save fails**.
- Directly violates two design constraints: *"Ordinary saves must continue to work with the supported provider at eval-release"* and *"preserving independently releasable main."* As written, this increment is **not independently releasable** — merging to `main` breaks production until Task 2 ships.
- In scope per the scope protocol (a client change that breaks the deployed contract), **not** an out-of-scope "Task 2 missing" finding.
- code-reviewer: P0, 95% confidence
- pal: CRITICAL — *"unconditionally requires `response.get("applied") is True`… all ordinary saves will fail… violates the explicit design constraint."*
- Suggested fix (both agree): gate the check behind the rollout capability. Minimal form: `if enhanced_settings and response.get("applied") is not True:` — treat an absent key as the legacy provider (succeed), only reject an explicit negative ack.

**2. [tests/test_client.py:8] Regression masked by the mutated test; new branches untested** ⟨corroborated⟩ — **P2 / MEDIUM**
- Profile: python · Checklist: code-quality-checklist.md
- The one existing test was edited to add `"applied": True` to the stub, turning the suite green while *hiding* the P0 break. No coverage for: legacy response `{"ok": True}`, `applied: False` rejection, or the `ok: False` path.
- A test asserting `{"ok": True}` still succeeds would have caught the P0.
- code-reviewer: P2, 90% · pal: MEDIUM
- Suggested fix: restore a legacy-provider test (`{"ok": True}` succeeds) and add dedicated enhanced-path cases (success + failure).

**3. [client.py:2] `require_receipt` sent unconditionally + magic-string protocol keys** ⟨corroborated⟩ — **P3 / LOW**
- Profile: python · Checklist: solid-checklist.md
- `"require_receipt": True` is added to every request regardless of `enhanced_settings` (which defaults `False` — "enhanced UI disabled by default"), and protocol keys (`require_receipt`, `applied`, `ok`, `settings`) are inline literals.
- code-reviewer: P3, 60% · pal: LOW
- Suggested fix: only add `require_receipt` when the rollout flag/capability is active; extract keys to named constants.

*No divergence in severity between reviewers on any finding.*

---

### Notes / Areas Not Covered
- Neither reviewer could verify the deployed provider's exact response shape (it lives in the separate Task 2 repo). The P0 rests on the design's stated fact that receipts are *added* by the pending provider increment — consistent across design.md and implementation.md. If some adapter outside this diff already injects `applied` for the legacy provider, severity would drop; no such code exists in the reviewed files.
- `send` callable contract (can it return `None`? → `.get` would `AttributeError`) is defined by callers outside this diff; pre-existing, not introduced here.

**Indexed**: the P0 pattern (backward-incompatible protocol enforcement in a split client/provider rollout, masked by a mutated test) → `kk:review-findings`.

---

## Next Steps

I found **3 issues, all corroborated** (P0 ×1, P2 ×1, P3 ×1).

Items I recommend fixing:

1. **P0 (corroborated)** — Gate the `applied` receipt check so legacy/ordinary saves keep working (e.g. only enforce under `enhanced_settings`, treat a missing key as legacy success). This is a merge blocker.
2. **P2 (corroborated)** — Restore a legacy-provider test asserting `{"ok": True}` still succeeds, and add enhanced-path success/failure tests (plus the untested `ok: False` path).
3. **P3 (corroborated)** — Make `require_receipt` conditional on the same flag/capability, and extract protocol keys to constants.

Items to keep as-is:
- Task 2 (provider receipts) absence — correct: it's pending and out of scope by design.
- Using `.get()` with `is not True` — safely avoids `KeyError`; the problem is the *gating*, not the access style.

**How would you like to proceed?**

1. **Fix all** — implement all three fixes
2. **Fix corroborated + high severity** — P0 + P2 (the merge-blockers)
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

Pick an option or give specific instructions. I won't change anything until you confirm.
