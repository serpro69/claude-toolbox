# Preparation settings
The prep_minutes member participates in late resolution on the item side in the
absence of a non-null value, with zero representing presence, and materialization
occurs at order creation through create_order; writes to the restaurant member are
not reflected in that materialized member. Inherited menu-item reads therefore
reflect changed restaurant values. This increment introduces resolution and order
materialization for owners needing a restaurant-wide default plus item exceptions.
Here materialization means copying the resolved number into a new order, so later
default changes do not update existing orders. The default may be 15, with one item
null and another zero, and it may later become 20. Scheduling is excluded. The
product owner has not decided whether the menu editor should show inheritance
badges. Storage uses prep_minutes on restaurant, item and order; the functions are
effective_minutes and create_order.
