1. **Why:** Restaurant defaults let items share a preparation time without duplicating it on every item. Explicit item overrides, including zero, take precedence (lines 3–6).

2. **Representative case:** With a default of 15 minutes, null resolves to 15, zero resolves to 0, and an override of 7 resolves to 7 (lines 8–9).

3. **Current increment:** Implement `effective_minutes(default, override)` by replacing the `NotImplementedError` placeholder with runtime selection. The nullable contract already exists; requirements and schema remain unchanged (lines 15–23).

4. **Outside scope:** Range enforcement, persistence, scheduling, and UI work. The recorded tests cover the three selection cases but do not establish range validation or end-to-end integration; persistence and deployment validation are unrecorded (lines 22–32).

5. **Open decision:** The product owner must decide whether inherited values display a badge in the UI (lines 32–34).
