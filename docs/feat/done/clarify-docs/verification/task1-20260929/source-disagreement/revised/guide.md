# Preparation updates

Restaurant owners need a default preparation time with exceptions for individual
items. An item inherits the restaurant default when its `prep_minutes` is null or
missing; an explicit value, including zero, overrides the default. The current
increment covers lookup and order snapshots; scheduling is excluded.

In [prep.py](prep.py), `effective_minutes` resolves the preparation time, and
`create_order` records that value in the order's `prep_minutes` snapshot. With a
restaurant default of 15, an item without an override resolves to 15. Existing
order snapshots MUST remain unchanged, as required by
[the accepted requirements](requirements.md).

Default activation has an unresolved requirement/implementation conflict. The
accepted requirement says a changed restaurant default MUST wait until the next
day for new inherited lookups: changing 15 to 20 should leave those lookups at 15
until tomorrow. The current lookup reads the restaurant's value directly, so once
that value changes to 20, a new inherited lookup returns 20 immediately. The
supplied implementation does not provide the required delay.

The feature maintainer owns reconciliation. The next step is to resolve how the
required next-day activation fits the increment's exclusion of scheduling, then
identify the implementation work or approved requirement change needed. Until that
is resolved, next-day activation must not be described as implemented.

Product still owns the unresolved decision on inheritance badges; the next step is
for Product to decide whether and how inherited preparation times are labelled.
