# Preparation settings

Set one default preparation time for your restaurant and give individual menu
items their own times when needed. This update determines which preparation time
applies to each item and saves that time when an order is created.

An item with no preparation time set uses the restaurant default. This is called
**inheritance**: the item uses the current default each time its preparation time
is looked up. Both a missing value and `null` mean no time is set. An item set to
**0 minutes** has its own preparation time of zero and does not inherit the default.

Each new order keeps a copy of the preparation time that applied when it was
created. Changing the restaurant default affects the next lookup for items that
inherit it; existing orders keep their saved time.

For example, suppose your restaurant default is **15 minutes**. An item with no
time set uses 15 minutes, while an item explicitly set to zero uses 0 minutes.
An order created for the first item saves 15 minutes. If you then change the
default to **20 minutes**, that item's next lookup returns 20 minutes, and a new
order for it saves 20 minutes. The earlier order still has 15 minutes, and the
item set to zero still uses 0 minutes.

Scheduling is outside this update. The product owner still needs to decide
whether the menu editor should show inheritance badges to identify items that
use the restaurant default.

For technical reference, the preparation-time field is named `prep_minutes` on
restaurants, items and orders. `effective_minutes` determines the applicable time;
`create_order` copies it into a new order.
