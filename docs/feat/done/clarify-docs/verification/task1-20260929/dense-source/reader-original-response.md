1. **Why it exists:** Owners need a restaurant-wide preparation-time default with exceptions for individual items. (§ “Preparation settings,” paragraph 1, sentence 4.)

2. **Representative case:** With a restaurant default of 15, an item whose `prep_minutes` is null inherits 15; an item with zero uses zero. Creating an order copies the resolved number into it. If the restaurant default later becomes 20, inherited menu-item reads reflect 20, while existing orders keep their copied values. (§ “Preparation settings,” paragraph 1, sentences 1–6.)

3. **Current increment:** Introduces preparation-time resolution and copying the resolved value into new orders. Storage uses `prep_minutes` on restaurants, items and orders; the named functions are `effective_minutes` and `create_order`. The artifact does not specify whether those storage fields are newly added or already exist. (§ “Preparation settings,” paragraph 1, sentences 4–5 and 9.)

4. **Outside it:** Scheduling is explicitly excluded. Later restaurant-default changes also do not update existing orders. No other exclusions are stated. (§ “Preparation settings,” paragraph 1, sentences 2, 5 and 7.)

5. **Decision still needed:** The product owner has not decided whether the menu editor should display inheritance badges. No other unresolved decision is stated. (§ “Preparation settings,” paragraph 1, sentence 8.)
