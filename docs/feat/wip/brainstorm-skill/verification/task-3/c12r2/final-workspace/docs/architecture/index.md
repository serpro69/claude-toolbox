# Domain-reference conventions

Each bounded context has two sibling pages: `<context>.md` for its glossary and business rules, and `<context>-traps.md` for divergences and cross-file hazards. Read and review the pair together.

## Entry fields

Each term carries **Definition**, **Bindings**, and **Status**. Include **Aliases**, **Not to be confused with**, and **Notes** when they contain useful information. Omit empty fields; do not invent aliases.

## Status markers

| Marker | Meaning |
| --- | --- |
| `canonical` | Ratified by a human with authority over the domain. |
| `proposed` | The author's reading, awaiting human ratification. |
| `undecided` | An unresolved domain decision that belongs in the decision queue. |
| `deprecated-alias` | A retained historical name pointing to the canonical term. |
| `overloaded` | A name with multiple meanings that the entry disambiguates. |

Documenting a requirement or observing stored data does not itself ratify this kit. Never promote `proposed` to `canonical` without a recorded human decision.

## Two clocks and evidence

Definitions track the business clock: what concepts mean. Bindings track the code clock: where those concepts appear in implementation or data. A code fact never ratifies business intent. A data snapshot establishes only the supplied records; it does not establish runtime behavior, constraints, or enforcement.

Cite files, fields, and symbols, never line numbers. Each kit page ends with a Derived-from footer covering every source of its domain facts. Ticket notes state the condition that retires them.

The glossary includes exactly one conceptual diagram and a numbered business-rules table with a provenance banner. Relationship multiplicity must distinguish historical records from simultaneous active records.

## Traps and freshness

Traps record facts requiring multiple sources, not schema inventories. Use stable `D#` identifiers for established divergences and `P#` identifiers for cross-file hazards. Every entry states what retires it; delete resolved entries in the same change and never reuse their identifiers.

Each glossary and traps page carries a freshness banner: the page remains proposed until reviewed by a human other than its author, and consumption-time freshness is checked by re-running `/kk:review-architecture` against its Derived-from anchors. Author self-checks do not confer approval or continuing freshness.

## Contexts

- Equipment lending: [glossary](equipment-lending.md) and [divergences and traps](equipment-lending-traps.md).
