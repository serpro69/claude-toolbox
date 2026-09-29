1. **Why:** Restaurant owners need a default preparation time with item exceptions (line 3). Further business context is explicitly omitted, so it cannot be established here (line 12).
2. **Representative case:** With a default of 15 minutes, `null` means 15 and `0` means zero. This describes the contract; the resolver is future work (line 4).
3. **Current increment:** Define the contract accepting integer minutes from 0–90 or `null`. JSON parsing passed, but there is no runtime or deployment evidence (lines 3–7).
4. **Outside scope:** The resolver, persistence, scheduling, and UI (lines 4–5).
5. **Remaining decision:** The product owner must decide inheritance badges. The document provides no further detail about that decision (line 6).
