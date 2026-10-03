# Equipment lending — divergences and traps

Companion to the [equipment lending glossary](equipment-lending.md). These entries distinguish observed records from the business policy needed before checkout validation.

> **Freshness:** This page is `proposed` until reviewed by a human other than its author; it is not self-certified. Check staleness by re-running $kk:review-architecture against the Derived-from anchors at consumption time. Freshness is a review run, not a standing promise.

## P1 — Stored overlap is not an approved policy

`requirements.md` defines a loan without a return as active and explicitly says that permitted active-loan multiplicity is unresolved. `records.json` contains loans `L1` (Mira) and `L2` (Ola), both for `CAM-7` and both with `returned_at: null`. Together these sources establish two active records for one physical item under the stated definition.

They do not establish whether overlap is legitimate, an error, or an exception. Declaring the records invalid would invent a uniqueness rule; declaring overlap permitted would turn stored data into business authority. A lookup or validation design that assumes at most one active loan would therefore depend on an unratified decision. No such runtime lookup, write path, constraint, or enforcement implementation is supplied here.

**Decision:** Glossary L4 and RQ-1 belong to the operations owner. If overlap is prohibited, RQ-2 asks how the existing overlap should be treated; the snapshot supplies no basis to choose a loan to close or delete. It contains no checkout timestamps or event history establishing which loan came first or who currently possesses the item.

**Retires when:** The operations owner records the allowed active-loan cardinality and the disposition of the observed overlap is documented, and the glossary is updated to reflect those decisions. Any later discrepancy between that decision and inspected implementation requires its own divergence entry; policy ratification alone does not prove enforcement.

No `D#` divergence is asserted: an approved uniqueness rule and runtime implementation have not been supplied. Do not reuse retired identifiers.

---
**Derived-from:** `requirements.md` · `records.json`.
