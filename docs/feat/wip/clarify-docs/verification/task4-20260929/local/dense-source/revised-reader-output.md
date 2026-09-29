1. **Why this exists:** To support a restaurant-wide preparation-time default with item-specific exceptions, and preserve the applicable time when an order is created. The guide does not state a broader business motivation. [Guide, lines 3–5](revised/guide.md#L3)

2. **Representative case:** With a 15-minute default, an item without a value uses 15; an item explicitly set to zero uses zero. Changing the default to 20 affects future lookups and new orders for the inherited item, while its earlier order keeps 15. [Guide, lines 12–19](revised/guide.md#L12)

3. **Current increment:** Resolve each item’s preparation time and save that resolved number on order creation. Missing or null values inherit the current default; explicit values override it. [Guide, lines 3–10](revised/guide.md#L3), [technical reference, lines 28–31](revised/guide.md#L28)

4. **Outside the increment:** Scheduling. Existing orders also retain their saved times after default changes. [Guide, lines 21–23](revised/guide.md#L21)

5. **Decision still needed:** The product owner must decide whether the menu editor displays badges identifying items that inherit the default. [Guide, lines 25–26](revised/guide.md#L25)
