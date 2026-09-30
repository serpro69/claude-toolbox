1. **Why it exists:** To support restaurant preparation defaults with item overrides, while preserving each order’s resolved time against later default changes. (“Preparation defaults,” paragraph 1.)

2. **Representative case:** With a 15-minute default, missing or null `prep_minutes` inherits 15; explicit zero stays 0. Changing the default to 20 changes the inherited item’s next lookup to 20, while the zero remains 0 and an earlier order keeps 15. (Paragraph 2.)

3. **Current increment:** Adds lookup and an order snapshot. `effective_minutes` resolves the current value; `create_order` copies it into a new order. (Paragraphs 1 and 3.)

4. **Outside it:** Scheduling is explicitly excluded. The document does not identify other exclusions. (Paragraph 3.)

5. **Decision still needed:** The product owner must decide inheritance badges for the menu editor. The specific choices are not stated. (Paragraph 3.)
