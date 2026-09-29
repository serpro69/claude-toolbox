1. **Why it exists:** Restaurant owners need a default preparation time with exceptions for individual items (lines 3–4).

2. **Representative case:** With a default of 15, an item value of `null` means 15; a value of zero means zero. This describes the contract; the resolver is future work (line 4).

3. **Current increment:** Defines that contract and a schema permitting values from 0–90. Validation is limited to JSON parsing; runtime and deployment behavior are not established (lines 3–7).

4. **Outside this increment:** The resolver, persistence, scheduling, and UI (lines 4–5).

5. **Decision still needed:** The product owner must decide inheritance badges. The document does not specify the choices or decision criteria (line 6).
