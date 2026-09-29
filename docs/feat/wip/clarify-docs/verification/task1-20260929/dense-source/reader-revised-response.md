1. **Why it exists:** To support a restaurant-wide preparation time with item-specific exceptions, determine which time applies, and preserve it when an order is created. A broader business motivation is not stated. (“Preparation settings,” opening paragraph.)

2. **Representative case:** With a 15-minute default, an item without its own time uses 15, and its order saves 15. Changing the default to 20 makes subsequent lookups and new orders use 20; the earlier order retains 15. An explicit zero remains zero. (“Preparation settings,” example and its three bullets.)

3. **Current increment:** Resolve preparation times through inheritance or explicit overrides, then copy the resolved value into each new order. The maintainer paragraph identifies `prep_minutes`, `effective_minutes`, and `create_order`. Previous implementation behavior is not provided, so the precise change from that baseline is uncertain. (“Preparation settings,” opening, inheritance, and final maintainer paragraphs.)

4. **Outside it:** Scheduling is explicitly outside this increment. No other definite exclusions are stated. (“Preparation settings,” paragraph beginning “Scheduling is outside this increment.”)

5. **Decision needed:** The product owner must decide and record whether the menu editor should display badges identifying items that inherit the restaurant default. (“Preparation settings,” scheduling and decision paragraph.)
