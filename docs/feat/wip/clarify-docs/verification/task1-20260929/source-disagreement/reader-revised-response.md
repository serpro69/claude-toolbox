1. **Why this work exists:** Restaurant owners need a default preparation time with item-specific exceptions. Missing or null `prep_minutes` inherits the default; explicit values, including zero, override it. (“Preparation updates,” paragraph 1.)

2. **Representative case:** With a restaurant default of 15 and no item override, `effective_minutes` returns 15; `create_order` records that value in the order’s `prep_minutes` snapshot. Existing snapshots must remain unchanged. (“Preparation updates,” paragraph 2.)

3. **Current increment:** It covers preparation-time lookup and order snapshots. The guide does not specify the precise changes from the previous implementation. Required next-day activation is explicitly unimplemented: inherited lookups currently reflect a changed default immediately. (“Preparation updates,” paragraphs 1–3.)

4. **Outside the increment:** Scheduling is excluded. Existing order snapshots must remain unchanged. The guide does not establish whether inheritance badges belong to this increment. (“Preparation updates,” paragraphs 1, 2, and 5.)

5. **Decisions remaining:** The feature maintainer must reconcile required next-day activation with scheduling’s exclusion, identifying implementation work or an approved requirement change. Product must decide whether and how inherited preparation times receive badges. Neither outcome is specified. (“Preparation updates,” paragraphs 4–5.)
