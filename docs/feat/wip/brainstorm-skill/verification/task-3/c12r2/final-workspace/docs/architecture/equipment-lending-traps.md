# Equipment lending — divergences and traps

Read this page with the [glossary and rules](equipment-lending.md) and [conventions](index.md).

> **Freshness:** This page is `proposed` until reviewed by a human other than its author; it is not self-certified. Check staleness by re-running `/kk:review-architecture` against the Derived-from anchors at consumption time. Freshness is a verification run, not a standing promise.

### P1 — Stored multiplicity does not establish checkout policy

`records.json` contains loans `L1` and `L2` for item `CAM-7`, with different borrower values and `returned_at: null` on both. Read with the active-loan definition in `requirements.md`, these are two active loan records for one physical item.

The same brief explicitly says whether this may occur is "an unresolved business decision, not an approved uniqueness rule." Neither interpretation is established: the records do not authorize simultaneous loans, and no approved rule establishes that the records violate policy. The snapshot also cannot show whether runtime code permits, prevents, or otherwise handles another checkout; no implementation was supplied.

Neither source supplies checkout times or a precedence rule for these records. Their array order and identifiers therefore do not establish which loan came first or which, if either, should be corrected. Both supplied return fields are explicitly `null`; no absent-field example establishes how a runtime implementation would handle that representation.

**Consequence:** Implementing an at-most-one-active-loan check now would select business policy without the required decision. Treating stored multiplicity as permission would make the same mistake in the opposite direction. See glossary rule L3 and decision RQ-1. If the owner prohibits multiplicity, also resolve RQ-2 before treating an existing loan as invalid.

**Retires when:** The operations owner's decision is recorded in the glossary, the handling of the supplied overlapping loans is settled where necessary, and the applicable checkout behavior is established from implementation evidence. At that point remove P1 and update its glossary references; never reuse its identifier.

No `D#` divergence is asserted: the supplied sources establish neither a settled active-loan limit nor runtime behavior to compare against one.

---

**Derived-from:** `requirements.md` · `records.json` (`loans`, records `L1` and `L2`).
