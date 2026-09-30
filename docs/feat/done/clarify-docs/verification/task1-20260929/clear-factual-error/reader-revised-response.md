1. **Why this exists:** Restaurant owners need one preparation-time default with per-item overrides. New orders store the resolved minutes so later default changes cannot alter them. (“Preparation defaults,” paragraph 1.)

2. **Representative case:** With a 15-minute default, missing or null `prep_minutes` inherits 15; explicit zero remains 0. Changing the default to 20 changes the inherited item’s next lookup to 20, while an earlier order retains 15. (“Preparation defaults,” paragraph 2.)

3. **Current increment:** Adds current-value lookup through `effective_minutes` and an order snapshot through `create_order`. The storage field is `prep_minutes`. (“Preparation defaults,” paragraphs 1 and 3.)

4. **Outside this increment:** Scheduling is explicitly excluded. The guide does not identify any other exclusions. (“Preparation defaults,” paragraph 3.)

5. **Decision still needed:** The product owner must decide inheritance badges for the menu editor. The guide does not specify the available choices. (“Preparation defaults,” paragraph 3.)
