1. **Why it exists:** Owners need a restaurant-wide preparation default with per-item overrides, while existing orders retain their original resolved time. See [guide.md, lines 2–4](/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/clear-factual-error/revised/guide.md:2).

2. **Representative case:** With a 15-minute default, missing or null `prep_minutes` inherits 15; explicit zero remains 0. Changing the default to 20 updates subsequent lookups for inherited items, while an earlier order keeps 15. See [guide.md, lines 6–8](/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/clear-factual-error/revised/guide.md:6).

3. **Current increment:** Adds current-value lookup through `effective_minutes` and snapshots that value into new orders through `create_order`. See [guide.md, lines 3–4 and 10–11](/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/clear-factual-error/revised/guide.md:10).

4. **Outside scope:** Scheduling. See [guide.md, line 11](/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/clear-factual-error/revised/guide.md:11).

5. **Pending decision:** The product owner must decide inheritance badges for the menu editor; the guide does not specify the badge behavior or appearance. See [guide.md, line 12](/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/clear-factual-error/revised/guide.md:12).
