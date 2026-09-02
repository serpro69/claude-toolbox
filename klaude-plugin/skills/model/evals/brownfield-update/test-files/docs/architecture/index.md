# Domain-reference kits — conventions index

Every `<context>.md` / `<context>-traps.md` pair in this directory reads under this contract.

## Per-term entry fields

**Definition** (business clock) / **Bindings** (code clock) / **Status** / **Aliases** / **Not to be confused with** / **Notes**.

## Status markers

| Marker | Meaning |
| --- | --- |
| `canonical` | Ratified by a human with authority over the domain. |
| `proposed` | Author's best reading; awaiting ratification. Default for anything reverse-engineered from code. |
| `undecided` | The domain itself has not settled this. |
| `deprecated-alias` | A name kept for recognition; points at the canonical term. |
| `overloaded` | One name carrying two meanings; the entry disambiguates them. |

## Two-clock rule

Definitions track the business clock; Bindings track the code clock. A code fact never ratifies a business intent.

## Citations

File or symbol only — never line numbers.

## Freshness

A page is `proposed` until reviewed by a human other than its author. Staleness is checked by re-running `/kk:review-architecture` against the page's Derived-from anchors at consumption time.
