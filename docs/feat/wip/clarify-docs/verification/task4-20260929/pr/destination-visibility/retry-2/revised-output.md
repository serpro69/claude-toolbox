1. **Why:** Restaurant owners need a default preparation time with exceptions for individual items (lines 3–4).
2. **Representative case:** With a default of 15, `null` means 15 and zero means zero (line 4).
3. **Current increment:** This PR defines the contract; the schema permits 0–90. Validation is limited to JSON parsing, with no runtime or deployment evidence (lines 3–7).
4. **Outside scope:** The resolver is future work. Persistence, scheduling, and UI are outside this increment (lines 4–5).
5. **Pending decision:** The product owner must decide inheritance badges. The document does not explain the options or criteria for that decision (line 6).
