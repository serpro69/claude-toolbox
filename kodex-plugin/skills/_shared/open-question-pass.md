# Open-question verification pass

A shared producer guard. Any producer skill whose verification phase re-reads a source to check its own claims runs at least one open-question pass, not confirm-passes alone.

## Motivating failure (F4 — invisible invariant)

In the field, a load-bearing hidden invariant — a single-result lookup at read time against unenforced multiplicity at write time — **survived four separate walks of the same file**. Each walk re-confirmed the claims already written and moved on. The invariant was never written down, so there was nothing to confirm, and confirmation-seeking verification never asked the question that would have surfaced it.

The lesson: **confirmation-seeking verification finds staleness, never omissions.** Re-reading a source to check what you already wrote can only tell you whether the written claims still hold. It is structurally blind to the load-bearing fact you never thought to write. Omissions are found only by asking new questions of the source.

## The rule — alternate confirm-passes with new-question passes

Verification is **not complete after a confirm-pass**. It requires **at least one open-question pass**, executed as a distinct step:

1. **Confirm-pass (necessary, not sufficient).** Re-read the source and check that each drafted claim still holds. This catches drift and staleness.
2. **Open-question pass (the guard).** Re-walk the same source asking **new questions** — deliberately *not* re-reading the claims you wrote. Interrogate the source for what it silently assumes and what no single claim yet captures.

Run the open-question pass with the confirm-pass results **out of view** so they cannot anchor the questioning back onto already-written claims.

## The question checklist

At minimum, ask of each source:

- **Cardinalities** — is a relationship assumed one-to-one, one-to-many, or many-to-many, and is that assumption enforced or merely expected?
- **Single-result lookups** — does a read expect exactly one result where the write path does not guarantee uniqueness?
- **Unchecked writes** — is anything written without validating a precondition the readers rely on?
- **Silent defaults** — what value or branch is taken when input is absent, and does any consumer depend on it without knowing it is a default?
- **Time and ordering** — does correctness depend on an ordering or a moment that nothing enforces?

Anything this pass surfaces that is not already a written claim is a finding — record it (as a new claim, a divergence, or an open question for a human), never discard it.

## Self-check

- Did I run a pass that asked **new questions**, or only re-confirmed existing claims?
- Did I work the checklist against the source, not against my notes?
- Is every surfaced invariant/omission recorded rather than silently dropped?
