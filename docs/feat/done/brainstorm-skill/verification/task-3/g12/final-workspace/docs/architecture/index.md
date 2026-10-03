# Domain-reference conventions

Each bounded context has a glossary and a companion divergences/traps page. Read and review them together.

- [Equipment lending glossary](equipment-lending.md)
- [Equipment lending divergences and traps](equipment-lending-traps.md)

Each term has **Definition**, **Bindings**, and **Status** fields, plus **Aliases**, **Not to be confused with**, and **Notes** when applicable. Definitions describe business meaning; bindings point to evidence in source files or symbols. Cite files or symbols, never line numbers.

Status markers:

- `canonical`: ratified by a human with domain authority.
- `proposed`: the author's reading, awaiting ratification.
- `undecided`: an unresolved domain decision.
- `deprecated-alias`: a retained old name pointing to its replacement.
- `overloaded`: a name with multiple meanings that must be distinguished.

The **two-clock rule** separates business intent from observed implementation. Code establishes what runs, never what the business intends. A data snapshot establishes only which records it contains; it proves neither implementation behavior nor permission. Inferred intent remains `proposed`; human ratification is required to make it `canonical`.

Each glossary has one conceptual diagram and a numbered business-rules table with provenance. Both pages carry freshness banners and Derived-from footers. Trap identifiers remain stable and are never reused. Each trap states its retirement condition; remove it when that condition is met. Ticket-specific notes also require retirement conditions.

Pages are `proposed` until reviewed by a human other than their author. Check freshness at consumption time by running $kk:review-architecture against the Derived-from anchors. Author checks do not self-certify the kit.
