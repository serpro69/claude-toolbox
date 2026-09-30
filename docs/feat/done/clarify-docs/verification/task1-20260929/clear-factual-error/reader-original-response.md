1. **Why:** Let restaurant owners set a shared preparation time with item overrides, while preserving each order’s resolved time when defaults change. (“Preparation defaults,” paragraph 1.)

2. **Representative case:** With a 15-minute default, missing or null `prep_minutes` inherits 15; explicit zero stays 0. Changing the default to 20 changes the inherited item’s next lookup to 20, while an earlier order retains 15. (“Preparation defaults,” paragraph 2.)

3. **Current increment:** Adds lookup and an order snapshot. `effective_minutes` resolves the current value; `create_order` copies it into a new order. (“Preparation defaults,” paragraphs 1 and 3.)

4. **Outside scope:** Scheduling. Other exclusions are not specified. (“Preparation defaults,” paragraph 3.)

5. **Pending decision:** The product owner must decide inheritance badges for the menu editor. The badge options and exact decision are not specified. (“Preparation defaults,” paragraph 3.)
