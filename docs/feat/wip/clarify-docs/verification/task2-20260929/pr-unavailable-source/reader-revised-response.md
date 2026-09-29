1. **Why:** Restaurant defaults “avoid repeating the same preparation time.”
2. **Representative case:** With a default of 15, `null` inherits 15 and explicit `0` remains zero. This contract is confirmed; runtime behavior remains unverified.
3. **Current increment:** Uncertain. “Branch names alone do not establish what this PR adds.” Exact revisions, the diff, and test output are needed.
4. **Outside scope:** “Persistence and scheduling remain outside this PR” and are planned for later work.
5. **Open decision:** The badge decision remains open with the product owner. The preparation-time contract is already confirmed.
