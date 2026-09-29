# Preparation updates

Restaurant owners need a default preparation time with item-specific exceptions.
The current increment covers preparation-time lookup and order snapshots;
scheduling is excluded. An item with a null or missing `prep_minutes` inherits the
restaurant default. An explicit value overrides the default, including zero.
When an order is created, it stores the resolved preparation time as a snapshot.
Later default changes leave that snapshot unchanged.

The accepted requirement and the implementation disagree on when a changed default
affects inherited lookups. [The requirements](requirements.md) mandate waiting
until the next day. [The current implementation](prep.py) reads the restaurant's
current default immediately, with no next-day delay.

For example, with a default of 15 minutes, an inherited item resolves to 15 and a
new order stores 15. If the default changes to 20, the requirement says new
inherited lookups must remain at 15 until the next day. The implementation instead
returns 20 immediately. The existing order retains 15 in both cases.

The feature maintainer owns reconciliation of this timing mismatch. The next step
is to bring the implementation into agreement with the accepted next-day
requirement, or obtain an explicit requirements decision, while resolving how that
timing requirement fits the increment's exclusion of scheduling. The requirement
remains in force until such a decision changes it.

Product owns the unresolved decision about badges that indicate inheritance.
