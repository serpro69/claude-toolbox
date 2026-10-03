# Domain-reference conventions

The equipment-lending kit consists of the [glossary](equipment-lending.md) and [divergences and traps](equipment-lending-traps.md). Read and update them together.

Term entries carry Definition, Bindings, Status, Aliases, Not to be confused with, and Notes; omit genuinely empty fields. Definitions express business meaning; bindings identify evidence in source files or symbols. A stored record or code fact never ratifies business intent. Cite paths and symbols without line numbers.

Status markers:

- `canonical`: ratified by a human with domain authority.
- `proposed`: an interpretation awaiting ratification; the default for inferred intent.
- `undecided`: a business question awaiting a decision.
- `deprecated-alias`: a retained name pointing to the preferred term.
- `overloaded`: a name with distinct meanings that the entry disambiguates.

Each glossary contains one conceptual diagram, a numbered business-rules table with provenance, and a Derived-from footer. Bindings to snapshots identify evidence, not runtime enforcement. Each traps entry captures a cross-source hazard or evidenced divergence and states its retirement condition. D/P identifiers are stable and never reused after retirement.

Pages remain proposed until another human reviews them. At consumption time, re-run `/kk:review-architecture` against the Derived-from anchors; author self-checks do not certify freshness. Keep unresolved decisions visible until a person with authority records their resolution.
