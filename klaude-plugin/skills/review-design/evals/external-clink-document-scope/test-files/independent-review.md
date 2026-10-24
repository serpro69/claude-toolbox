## Design Review Findings

Provenance: fixed synthetic design-reviewer result for a reporting checkpoint.

**Feature**: settings-sync
**Docs reviewed**: design.md, implementation.md
**Scope**: default; tasks.md was requested but missing and was not reviewed
**Overall assessment**: CONCERNS_FOUND

---

### P0 - Critical

(none)

### P1 - High

- **[INCONSISTENT]** Retry policy contradicts between design and implementation
  - **Section:** design.md:Architecture vs implementation.md:Task 2
  - **Confidence:** 9/10 — both statements are explicit and mutually exclusive
  - **Description:** design.md retries a failed push up to 3 times with exponential backoff and then drops it with a warning; implementation.md Task 2 step 2 retries until the push succeeds with a fixed 30-second sleep "so no change is ever lost". An implementer cannot satisfy both.
  - **Evidence:** design.md "retried up to 3 times with exponential backoff; after the third failure the push is dropped"; implementation.md "retry until the push succeeds, sleeping 30 seconds between attempts".
  - **Recommendation:** choose one policy, state it in both documents, and say what happens to pending pushes on shutdown.

### P2 - Medium

- **[MISSING]** No behavior defined for a provider that is unreachable at startup
  - **Section:** design.md:Architecture
  - **Confidence:** 7/10 — the design covers push failures but not registration or initial state
  - **Description:** the documents describe pushes after saves but not what `SettingsSync` does when the provider is unavailable when the application starts, or whether values saved while offline are queued.
  - **Evidence:** design.md Architecture covers only "a failed push"; implementation.md Task 2 step 3 registers at startup without a failure path.
  - **Recommendation:** state whether offline saves are queued and how the queue is bounded.

### P3 - Low

(none)

---

### Areas Not Covered

- `src/settings_sync.py` is planned and does not exist; the plan was assessed, not code.
- tasks.md was requested but missing, so task-format checks were not performed.
- `src/settings.py` exists and matches the contract the design describes (`save()` returns ok only when applied).
