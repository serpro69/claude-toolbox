# Equipment-lending divergences and traps

Read with the [glossary and decision queue](equipment-lending.md).

> **Freshness:** This page is `proposed` until reviewed by a human other than its author; it is not self-certified. Check staleness by re-running `/kk:review-architecture` against the Derived-from anchors at consumption time.

## P1 — Stored multiplicity does not settle policy

`requirements.md` defines a loan without `returned_at` as active and explicitly leaves concurrent lending of a physical item undecided. `records.json` supplies two distinct loans, `L1` for Mira and `L2` for Ola, both referencing `CAM-7` and both having `returned_at: null`. Together, these sources establish two stored active loans for the same item under the brief's definition.

This is neither evidence of an approved concurrent-lending policy nor evidence that an approved uniqueness rule was violated. No runtime code, write path, database constraint, or single-result lookup was supplied. Their enforcement behavior is unknown. Do not describe an unenforced uniqueness invariant as a confirmed defect.

Checkout validation depends on the operations owner's answer to RQ-1. If concurrency is disallowed, existing-record reconciliation also needs RQ-2: the snapshot has no checkout times or possession evidence that would justify keeping the first record, the last record, or either borrower automatically. A future validation change alone would not explain these existing records.

**Retires when:** the operations owner records the concurrency policy and disposition of the existing loans, and the glossary is updated with those decisions and the evidence needed to distinguish policy from actual enforcement.

No `D#` divergence is asserted: the supplied evidence contains neither an approved active-loan uniqueness rule nor an implementation to compare against it.

---
**Derived-from:** `requirements.md`; `records.json` (`loans[]`, `items[]`).
