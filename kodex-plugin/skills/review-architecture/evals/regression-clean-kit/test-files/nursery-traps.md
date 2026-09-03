# Nursery propagation — divergences & traps

> **Freshness:** This page is `proposed` until reviewed by a human other than its author — it is **not** self-certified. Check staleness by re-running `$kk:review-architecture` against the glossary's Derived-from anchors at consumption time; freshness is a skill run, not a standing promise.

Companion to the glossary at [nursery.md](nursery.md). Only facts no single file reveals.

### P1 — Capacity is gated at the caller, not in placement

`lots/placement.go` `PlaceLot` records a placement unconditionally; the capacity guard lives in `benches/capacity.go` `CanAccept` and is the caller's responsibility. New code that calls `PlaceLot` directly, without the `CanAccept` gate, silently overfills a bench — neither file alone reveals the split.

**Retires when:** placement and the capacity check merge behind one entry point.
