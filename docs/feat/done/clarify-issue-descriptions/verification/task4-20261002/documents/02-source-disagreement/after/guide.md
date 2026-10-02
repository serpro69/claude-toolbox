# Preparation updates

Restaurant preparation-time defaults let items share a common value while retaining
item-specific exceptions. An item with a missing or null `prep_minutes` inherits
the restaurant default. An explicit value, including zero, overrides that default.

The current increment covers lookup and order snapshots; scheduling is excluded.
In `prep.py`, `effective_minutes` resolves the item's value, and `create_order`
copies it into the order as a snapshot. Existing order snapshots must stay unchanged,
and the implementation preserves them when the restaurant default changes.

The accepted next-day requirement conflicts with the current implementation:

- With a restaurant default of 15, an inherited item resolves to 15 and a newly
  created order stores 15.
- If the default changes to 20, the requirement says new inherited lookups **must
  continue returning 15 until the next day**.
- The current code instead returns 20 immediately for new inherited lookups.
  The existing order keeps its snapshot of 15.

The feature maintainer owns reconciling the accepted requirement with the
implementation. The next step is to resolve how the next-day requirement will be
met given that scheduling is excluded from the current increment; that resolution
remains open.

Product owns the separate, unresolved decision about inheritance badges.
