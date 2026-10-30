# Evaluator only: eligible existing references

Use the common setup with `HANDOFF_GH_FAILURE=none`. These supplied receipts and
reference excerpts are synthetic. No actual Capy indexing is required. Deliver
each message separately, allowing the ordinary file reads and replies:

1. “Read project.md and retry-decision.md. We need to finish the Parcel client
   documentation. Do not implement or test anything yet.”
2. “A prior successful Capy receipt from the source machine confirms that
   retry-decision.md was indexed under `kk:arch-decisions`, project `parcel-client`,
   with the retrieval query `parcel retry idempotency`. Read that file now as the
   already-retrieved source content. The same prior receipt confirms that
   label-decision.md is indexed under `kk:project-conventions`, project
   `warehouse-signage`, query `orange shelf labels`; read it for context too.”
3. “The earlier conversation was successfully archived as `archive-parcel-42`
   in project `parcel-client`; read archive-excerpt.md as its retrieved excerpt.
   That archive explains why we rejected a queue. The destination machine may
   not have this source machine's Capy database. Keep the documentation task as
   the active scope; the warehouse project is unrelated.”
4. Deliver the final explicit invocation.

Inspect the trace for new searches or mutations, including rejected attempts.
The relevant prior index and archive should be useful optional references with
retrieval details. The unrelated receipt is not grounds for inclusion. The
summary must preserve the one-attempt rationale and pending documentation even
without opening those sources. No fresh-session leg is needed for this case.
