1. **Why it exists:** Owners need a restaurant-wide preparation-time default with exceptions for individual menu items. [Guide, lines 6–7](/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/dense-source/original/guide.md:6)

2. **Representative case:** With a restaurant default of 15, an item whose `prep_minutes` is null inherits 15; an item set to zero uses zero. Changing the default to 20 updates inherited menu-item reads, while existing orders retain their copied values. [Guide, lines 2–10](/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/dense-source/original/guide.md:2)

3. **Current increment:** Introduces preparation-time resolution and copying the resolved number into each new order. The named functions are `effective_minutes` and `create_order`. [Guide, lines 6–9](/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/dense-source/original/guide.md:6), [lines 12–13](/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/dense-source/original/guide.md:12)

4. **Outside the increment:** Scheduling is explicitly excluded. [Guide, line 10](/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/dense-source/original/guide.md:10)

5. **Decision still needed:** The product owner must decide whether the menu editor should display inheritance badges. Their inclusion remains uncertain. [Guide, lines 11–12](/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/dense-source/original/guide.md:11)
