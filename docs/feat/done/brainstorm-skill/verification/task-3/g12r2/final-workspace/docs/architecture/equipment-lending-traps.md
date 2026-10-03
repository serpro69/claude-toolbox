# Equipment lending — divergences and traps

> **Freshness:** This page is `proposed` until reviewed by a human other than its author; it is not self-certified. Check staleness by re-running $kk:review-architecture against the Derived-from anchors at consumption time. Freshness is a verification run, not a standing promise.

Read with [the glossary and decision queue](equipment-lending.md) under [the shared conventions](index.md).

No violation of an approved single-active-loan rule is established: `requirements.md` says that rule is unresolved, and no runtime implementation is supplied. The finding below concerns the interaction between the brief and the snapshot.

## P1 — Stored multiplicity can be mistaken for policy or a proven defect

`requirements.md` says: “Before we add checkout validation, determine whether one physical item may have multiple active loans.” It explicitly identifies this as an unresolved business decision, not an approved uniqueness rule. It also defines a loan without `returned_at` as currently active.

Applying that definition to `records.json` gives two active loans for `CAM-7`: `L1` for Mira and `L2` for Ola, both with `returned_at: null`. Together the sources establish observed multiplicity while leaving its legitimacy unsettled. Inferring either permission or a policy violation would close a decision that belongs to the operations owner.

The snapshot cannot establish that checkout allows these records, that runtime validation is absent, or that one record is newer or more authoritative. A future feature that requires a single current borrower must resolve the policy and existing records explicitly; choosing an array entry would not establish physical custody.

**Related rule:** L4. **Decision route:** RQ-1 to the operations owner; if exclusivity is chosen, RQ-2 determines treatment of the supplied records using operational evidence.

**Retires when:** The operations owner records the allowed active-loan cardinality, the supplied multiplicity is explicitly classified or reconciled under that decision, and both kit pages are updated to cite that evidence. Any remaining implementation question must be assessed against actual implementation sources, not this snapshot.

---

**Derived-from:** `requirements.md` · `records.json`
