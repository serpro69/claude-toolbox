1. **Why:** Owners need a shared preparation time with item overrides, while orders retain their original resolved time after defaults change. [guide.md, lines 2–4](/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/clear-factual-error/original/guide.md:2)

2. **Representative case:** With a 15-minute default, missing or null `prep_minutes` inherits 15; explicit zero remains 0. Changing the default to 20 changes subsequent inherited lookups, while an earlier order retains 15. [guide.md, lines 6–8](/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/clear-factual-error/original/guide.md:6)

3. **Current increment:** Adds value lookup and order snapshots: `effective_minutes` resolves the current value, and `create_order` copies it into a new order. [guide.md, lines 3–4 and 10–11](/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/clear-factual-error/original/guide.md:10)

4. **Outside scope:** Scheduling. [guide.md, line 11](/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/clear-factual-error/original/guide.md:11)

5. **Open decision:** The product owner must decide inheritance badges for the menu editor; the guide does not specify their intended behavior or appearance. [guide.md, line 12](/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/clear-factual-error/original/guide.md:12)
