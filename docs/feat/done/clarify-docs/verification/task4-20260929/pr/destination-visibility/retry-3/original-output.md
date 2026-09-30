1. **Why it exists:** Restaurant owners need a default preparation time with item-specific exceptions. (Lines 3–4.)

2. **Representative case:** With a default of 15, `null` means 15 and `0` means zero. This defines intended behavior; the resolver is future work. (Line 4.)

3. **Current increment:** The PR defines the preparation-time contract, with a schema permitting 0–90. Validation covers JSON parsing only; runtime and deployment behavior are unverified. (Lines 3–7.)

4. **Outside scope:** Implementing the resolver, persistence, scheduling, and UI. (Lines 4–5.)

5. **Pending decision:** The product owner must decide inheritance badges. The document does not specify the available options. (Line 6.)
