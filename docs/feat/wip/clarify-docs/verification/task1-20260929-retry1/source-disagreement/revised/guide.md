# Preparation updates

Restaurant owners need a default preparation time with exceptions for individual
items. The current increment covers looking up the effective time and storing it
in an order snapshot; scheduling is excluded.

In `prep.py`, `effective_minutes` uses the restaurant default when an item's
`prep_minutes` is null or missing. Any other item value overrides the default,
including zero. For example, with a default of 15, an item without an override
resolves to 15, while an item with an override of zero resolves to zero.

Default changes expose an unresolved difference between accepted intent and current
behavior:

- **Accepted requirement:** a changed restaurant default MUST wait until the next
  day for new inherited lookups. Changing 15 to 20 should therefore leave those
  lookups at 15 until tomorrow.
- **Current implementation:** `effective_minutes` reads the restaurant's current
  default directly. Once that value changes from 15 to 20, new inherited lookups
  return 20 immediately; the supplied code has no next-day activation mechanism.

`create_order` stores the effective preparation time at order creation as a
snapshot. Existing order snapshots MUST stay unchanged when the restaurant default
changes. The supplied source shows snapshot creation but does not establish how
existing orders are handled elsewhere.

The **feature maintainer** owns reconciliation of intent and implementation. The
next step is to resolve how to meet the next-day requirement given that scheduling
is excluded from this increment, or obtain an explicit change to the accepted
requirement or scope. The discrepancy remains unresolved.

The **product owner** still needs to decide whether items display inheritance
badges.
