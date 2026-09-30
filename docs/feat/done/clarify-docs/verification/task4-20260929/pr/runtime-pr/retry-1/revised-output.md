1. **Why it exists:** Restaurant defaults avoid repeating preparation times on every item. The helper resolves whether to use that default or an item override. *(Opening paragraph.)*

2. **Representative case:** With a default of 15 minutes, a null override returns 15, an explicit zero returns 0, and an override of 7 returns 7. *(Second paragraph.)*

3. **Current increment:** The PR replaces `effective_minutes`’s `NotImplementedError` with runtime resolution and adds `test_resolve.py`. The existing `prep_minutes` contract remains unchanged. *(“What changes in this PR.”)*

4. **Outside this increment:** Range validation, persistence, scheduling, and the user interface. The recorded assertions cover resolution only; no persistence or deployment validation is recorded. *(“What changes in this PR” and “Review and validation.”)*

5. **Remaining decision:** The product owner must decide whether inherited values display a badge, as part of separate UI work. No other unresolved decision is identified in this document. *(“Open decision.”)*
