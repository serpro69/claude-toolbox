1. **Why it exists:** Restaurant owners need a default preparation time with item-specific exceptions. (Line 3)

2. **Representative case:** With a default of 15, `null` means 15, while zero means zero. These are contract rules; the resolver is future work. (Line 4)

3. **Current increment:** Defines the preparation-time contract and a schema permitting 0–90. Validation covers JSON parsing only; runtime behavior and deployment are unverified. (Lines 3–7)

4. **Outside this increment:** The resolver, persistence, scheduling, and UI. (Lines 4–5)

5. **Remaining decision:** The product owner must decide inheritance badges. The document does not specify the options or decision criteria. (Line 6)
