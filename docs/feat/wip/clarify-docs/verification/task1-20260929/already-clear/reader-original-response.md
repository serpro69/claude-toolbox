1. **Why this work exists:** Restaurant owners need a preparation-time default with item overrides, and new orders must retain their resolved time when defaults later change. (“Preparation defaults,” paragraph 1.)

2. **Representative case:** With a 15-minute default, missing or null `prep_minutes` inherits 15; explicit zero stays 0. Changing the default to 20 makes the inherited item’s next lookup return 20, while the zero item stays 0 and an earlier order retains 15. (Paragraph 2.)

3. **Current increment:** Adds lookup and order snapshots. `effective_minutes` resolves the current value; `create_order` copies it into a new order. The storage field is `prep_minutes`. (Paragraphs 1 and 3.)

4. **Outside this increment:** Scheduling. No other exclusions are stated. (Paragraph 3.)

5. **Decision still needed:** The product owner must decide inheritance badges for the menu editor. The document does not specify the options or decision criteria. (Paragraph 3.)
