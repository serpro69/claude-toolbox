## commentary

I’ll answer the five questions from the permitted document and identify any gaps explicitly.

## final_answer

1. **Why:** Restaurant owners need a default preparation time with exceptions for individual items. (Line 3)

2. **Representative case:** With a default of 15, `null` means 15, while zero means zero. This describes the contract; the resolver is future work. (Line 4)

3. **Current increment:** Defines the preparation-time contract and a schema permitting 0–90. Validation is limited to JSON parsing; runtime and deployment behavior are unverified. (Lines 3–7)

4. **Outside scope:** The resolver, persistence, scheduling, and UI remain outside this increment. (Lines 4–5)

5. **Pending decision:** The product owner must decide inheritance badges. The document does not specify the available options or decision criteria. (Line 6)
