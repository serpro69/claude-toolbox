# Preparation settings
Set one default preparation time for your restaurant, with exceptions for individual
menu items. This increment determines which preparation time applies and saves a
copy when an order is created.

An item with no preparation time of its own uses the restaurant default. This is
called inheritance: the default is read each time the item's preparation time is
looked up. An item set to zero uses zero minutes; it does not inherit the default.

For example, suppose your restaurant default is 15 minutes:

- An item with no preparation time of its own uses 15 minutes. An order created for
  it saves 15 minutes.
- An item explicitly set to zero uses zero minutes, and an order for it saves zero.
- If you later change the restaurant default to 20 minutes, the next lookup for the
  inherited item returns 20, and a new order for it saves 20. The earlier order keeps
  its saved 15 minutes. The item set to zero still uses zero.

Scheduling is outside this increment. The product owner has not yet decided whether
the menu editor should show badges identifying items that inherit the default. The
next step is for the product owner to record whether those badges should be shown.

For maintainers: the preparation-time field is `prep_minutes` on the restaurant,
item and order. A missing or `null` item value inherits the restaurant default;
zero is an explicit override. `effective_minutes` determines the value to use.
`create_order` copies that value into the new order, so later changes to the
restaurant default do not change existing orders.
