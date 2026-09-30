# Preparation settings

Use a restaurant-wide default preparation time, in minutes, with exceptions for
individual menu items. This increment determines which preparation time applies to
an item and saves that number when an order is created.

An item with a missing or null preparation-time value uses the restaurant's current
default whenever its preparation time is looked up. This is called inheritance.
An item with its own value uses that value instead. Zero is an explicit item value;
it does not mean “use the default.”

For example, suppose the restaurant default is 15 minutes:

- An item with no preparation-time value uses 15 minutes. A new order for it saves
  15 minutes.
- An item set to zero uses zero minutes, and a new order for it saves zero.
- If the restaurant default later changes to 20 minutes, the next lookup for the
  inherited item returns 20, and a new order for it saves 20. The earlier order
  keeps its saved 15 minutes. The item set to zero still uses zero.

Each order keeps the preparation time saved at creation, so later changes to the
restaurant default cannot alter existing orders. Scheduling is outside this
increment.

The product owner still needs to decide whether the menu editor should show badges
identifying items that inherit the restaurant default.

For technical reference, the stored field is `prep_minutes` on the restaurant,
item and order. `effective_minutes` resolves the item's preparation time;
`create_order` copies that resolved number into a new order. This copy is the order's
snapshot, also called materialization.
