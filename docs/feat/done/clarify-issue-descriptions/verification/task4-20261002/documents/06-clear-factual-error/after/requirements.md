# Accepted requirements
Purpose: restaurant owners need one default preparation time and item exceptions.
The current increment resolves preparation minutes and snapshots them when an order
is created. A missing or null item value inherits the restaurant default at lookup
time; zero is an explicit override. Changing the default affects the next lookup
for inherited items, but cannot alter existing orders. Scheduling is outside this
increment. The product owner still needs to decide whether to show inheritance
badges in the menu editor. All files in this workspace may be shared with maintainers.
The maximum accepted default MUST be 90 minutes.
