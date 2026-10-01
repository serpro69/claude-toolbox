# Preparation settings
Set one default preparation time for your restaurant, with separate times for
individual menu items when needed. This change adds the rules for choosing each
item's preparation time and saving that time when an order is created.

An item with no preparation-time value, or a value of `null` (unset), uses the
restaurant's current default each time its preparation time is looked up. This is
called inheritance. A value of zero is an explicit item setting: its preparation
time is zero, even when the restaurant default is different.

For example, suppose your restaurant default is 15 minutes. An item set to `null`
uses 15 minutes, while an item set to zero uses zero minutes. An order created for
the inherited item saves 15 minutes. If you later change the default to 20 minutes,
the inherited item's next lookup uses 20 minutes, and new orders for it save 20
minutes. The existing order keeps its saved 15 minutes. The item set to zero still
uses zero minutes.

Scheduling is outside this change. The product owner still needs to decide whether
the menu editor should show badges identifying items that inherit the default.

Technical reference: restaurant, item and order records use the field
`prep_minutes`. The function `effective_minutes` chooses the item's preparation
time. The function `create_order` copies that number into the new order; this copy
is called materialization. Later changes to the restaurant default do not update
the number saved in an existing order.
