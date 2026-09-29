1. **Why:** Restaurant defaults “avoid repeating preparation times on every item.” The resolver previously raised `NotImplementedError`.
2. **Representative case:** With a 15-minute default, null resolves to 15, zero to 0, and an override of 7 to 7.
3. **Current increment:** Implements `effective_minutes(default, override)` in `resolve.py` and adds `test_resolve.py`. “Scope and review” identifies runtime logic despite the stack’s “schema-only” title; the existing nullable contract stays unchanged.
4. **Outside scope:** Range enforcement, persistence, scheduling, user-interface integration and badge policy. “Validation” reports three passing assertions but no persistence or deployment validation.
5. **Remaining decision:** The product owner must decide whether inherited preparation times display a badge, for the separate user-interface work (“Open decision”).
