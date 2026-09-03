# Marina berthing — divergences & traps

> **Freshness:** This page is `proposed` until reviewed by a human other than its author — it is **not** self-certified. Check staleness by re-running `/kk:review-architecture` against the glossary's Derived-from anchors at consumption time; freshness is a skill run, not a standing promise.

Companion to the glossary at [marina.md](marina.md). Only facts no single file reveals.

### D1 — Maintenance rule declared but unenforced

Rule L2 says a berth flagged for maintenance cannot be assigned. `moorings/assign.go` `AssignBerth` checks only the single-active rule and never reads `Berth.Maintenance`. The rule is intent; the code does not implement it.

**Retires when:** `AssignBerth` gains a maintenance check, or L2 is withdrawn.

### P1 — Name lookup assumes a uniqueness nothing enforces

`berths/registry.go` `FindByName` returns the first berth whose name matches, while `Register` accepts duplicate names without complaint. Two berths sharing a name make every lookup result registration-order-dependent — the write side and the read side disagree about whether names are keys.

**Retires when:** `Register` rejects duplicate names, or lookups key on a unique identifier.
