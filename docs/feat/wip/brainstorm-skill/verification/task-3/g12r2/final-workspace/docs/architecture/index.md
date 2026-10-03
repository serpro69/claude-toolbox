# Domain-reference conventions

Each bounded context has a glossary (`<context>.md`) and a companion divergences/traps page (`<context>-traps.md`). Read and review them together.

## Entries and status

Each glossary entry carries **Definition**, **Bindings**, and **Status**. Include **Aliases**, **Not to be confused with**, and **Notes** where meaningful; omit genuinely empty fields.

| Status | Meaning |
| --- | --- |
| `canonical` | Ratified by a human with authority over the domain. |
| `proposed` | An interpretation awaiting ratification; the default for reverse-engineered intent. |
| `undecided` | A domain decision remains open and appears in the decision queue. |
| `deprecated-alias` | A retained name pointing to its canonical replacement. |
| `overloaded` | A name has distinct meanings that the entry disambiguates. |

An author cannot promote a term or rule to `canonical` solely because records or code agree with it. Record the human decision that authorizes ratification.

## Evidence and citations

Definitions describe business meaning (the business clock). Bindings describe observable representation or implementation (the code clock). A code fact never ratifies business intent. A data snapshot establishes stored facts only, not runtime behavior, enforcement, or physical possession.

Cite files and symbols or record identifiers, never line numbers. Each context page ends with a **Derived-from** footer listing every source path supporting its domain claims. Business-rule tables carry a provenance banner, and enforcement pointers distinguish observed enforcement from unavailable evidence.

## Shape and freshness

The glossary has exactly one conceptual diagram, showing only relationships and attributes needed for the forcing question. The traps page adds cross-source findings, not a schema mirror. `D#` denotes a demonstrated divergence from a stated rule; `P#` denotes a cross-source hazard. Numbers remain stable and retired numbers are never reused. Each entry names its retirement condition and is removed when that condition is met. Ticket-specific notes also state what retires them.

Both context pages carry a freshness banner: they remain proposed until reviewed by a human other than their author. Re-run $kk:review-architecture against the Derived-from anchors at consumption time. Author checks do not self-certify a page or replace that review.

Decision questions name the role that can decide and the work that the answer unblocks. Unresolved policy remains explicit rather than being inferred from observed records.
