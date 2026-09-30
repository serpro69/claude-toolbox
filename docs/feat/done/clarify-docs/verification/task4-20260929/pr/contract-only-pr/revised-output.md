1. **Why:** Restaurant defaults avoid repeating preparation times for every item; this PR records the accepted item-override contract. (Lines 3–5.)

2. **Representative case:** With a restaurant default of 15 minutes, null specifies 15 minutes, while an explicit zero specifies 0 minutes. These are specified results; runtime behavior is unimplemented. (Lines 5–7, 10–12.)

3. **Current increment:** Only `contract.json` changes, replacing its empty object with a contract accepting null or integers from 0 through 90. Validation confirms successful JSON parsing. (Lines 4–5, 9–10, 17–18.)

4. **Outside scope:** Runtime integration, persistence, scheduling, and the user interface remain future work. No runtime tests or deployment occurred; default resolution remains unverified. (Lines 11–13, 18–19.)

5. **Pending decision:** The product owner must decide whether inherited values display a badge. (Lines 13–14.)
