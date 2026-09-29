1. **Why this exists:** Restaurant owners need a default preparation time with exceptions for individual items. (Opening paragraph under “Preparation updates.”)

2. **When the default changes from 15 to 20:** The accepted requirement says new inherited lookups should remain at 15 until tomorrow. The current implementation instead returns 20 immediately and has no next-day activation mechanism. Existing order snapshots must remain unchanged, but the supplied source establishes only snapshot creation; handling of existing orders elsewhere is unknown. (“Default changes…” bullets and “`create_order` stores…” paragraph.)

3. **Current increment:** Look up the effective preparation time and store it in an order snapshot. Null or missing item values inherit the restaurant default; other values, including zero, override it. The artifact does not establish which of these behaviors are newly added versus already present. (Opening, “In `prep.py`…,” and “`create_order` stores…” paragraphs.)

4. **Outside the increment:** Scheduling is explicitly excluded. No other exclusions are established. (Opening paragraph.)

5. **Decisions still needed:** The feature maintainer must reconcile next-day activation with the exclusion of scheduling, or obtain an explicit change to the accepted requirement or scope. The product owner must decide whether items display inheritance badges. Both remain unresolved. (Final two paragraphs.)
