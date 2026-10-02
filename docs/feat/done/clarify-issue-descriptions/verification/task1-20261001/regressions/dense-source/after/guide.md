# Preparation settings

Set one default preparation time for your restaurant, with a different time for
individual menu items when needed. This update determines which time applies to
each item and saves that time when an order is created.

An item without its own preparation time uses the restaurant's current default.
This is called **inheritance**. An item set to **0 minutes** has its own time: zero
does not mean “use the default.”

For example, suppose your restaurant's default is 15 minutes:

- An item with no preparation time of its own uses 15 minutes.
- An item set to 0 minutes uses 0 minutes.
- An order created for the first item saves 15 minutes.

If you later change the restaurant default to 20 minutes, the first item uses
20 minutes the next time its preparation time is looked up. New orders for that
item save 20 minutes. The existing order keeps its saved 15 minutes, and the item
with a zero-minute override continues to use 0 minutes.

Scheduling is outside this update. The product owner still needs to decide whether
the menu editor should show inheritance badges—labels indicating that an item uses
the restaurant default.

## Technical reference

The restaurant, menu item and order each store preparation time in `prep_minutes`.
For an item, a missing value or `null` means “inherit the restaurant default”; zero
is an explicit override. `effective_minutes` determines the applicable time at
each lookup. `create_order` copies that number into the new order. This copy is
called **materialization**: later changes to the restaurant default do not update
the order's saved value.
