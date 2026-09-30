# Preparation updates

Restaurant owners need a default preparation time with exceptions for individual
items. An item with a null or missing `prep_minutes` inherits the restaurant default;
any explicit value, including zero, overrides it. The current increment delivers
lookup and order snapshots; scheduling is excluded.

An order snapshot stores the effective preparation time when the order is created.
Existing snapshots MUST remain unchanged when the restaurant default changes.
The implementation in `prep.py` preserves this behavior.

Default-change timing remains unresolved: the accepted requirement says a changed
restaurant default MUST wait until the next day for new inherited lookups, but
`prep.py` reads the changed default immediately. For example, with a default of 15,
an inherited item resolves to 15 and a new order stores 15. After the default changes
to 20, the implementation returns 20 for a new inherited lookup while the existing
order keeps 15. The requirement instead calls for that new lookup to remain 15
until the next day.

The feature maintainer owns reconciliation of this disagreement. The next step is
to reconcile the immediate lookup behavior with the accepted next-day requirement
and clarify how that requirement fits the increment's exclusion of scheduling.
The requirement remains accepted; the implementation does not yet satisfy it.

Product owns the unresolved inheritance-badge decision. The next step is for
Product to decide whether and how inherited values should be indicated.
