1. **Why it exists:** Restaurant owners need a default preparation time with item exceptions (line 3). Additional business context is withheld pending disclosure authorization (lines 12–14).

2. **Representative case:** With a default of 15, `null` means 15 and zero means zero. This describes the contract; the resolver is future work (line 4).

3. **Current increment:** This PR defines the preparation-time contract, with a schema allowing 0–90. Validation covers JSON parsing only; runtime and deployment behavior are unverified (lines 3–7).

4. **Outside scope:** The resolver, persistence, scheduling, and UI remain outside this increment (lines 4–5).

5. **Outstanding decisions:** The product owner must decide inheritance badges (line 6). Someone must also identify who can authorize disclosure of additional business context; that owner is unknown (lines 12–14). Further decisions cannot be established from this artifact.
