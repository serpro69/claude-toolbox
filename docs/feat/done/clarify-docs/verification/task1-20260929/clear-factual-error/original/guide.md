# Preparation defaults
Restaurant owners can set one preparation time and override it for individual
items. This increment adds lookup and a snapshot: each new order stores the resolved
minutes so later default changes cannot change it.

With a restaurant default of 15 minutes, an item with a missing or null prep_minutes
inherits 15; an explicit zero stays 0. If the default becomes 20, the inherited
item's next lookup returns 20, the zero item stays 0, and an earlier order keeps 15.

The storage field is prep_minutes. effective_minutes resolves the current value;
create_order copies it into a new order. Scheduling is outside this increment.
The product owner still needs to decide inheritance badges for the menu editor.

## Reference
The maximum accepted default is 60 minutes.
