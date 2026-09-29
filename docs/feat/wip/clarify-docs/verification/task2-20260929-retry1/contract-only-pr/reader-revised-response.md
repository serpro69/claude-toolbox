1. **Why it exists:** To record the accepted preparation-time contract so items can inherit a restaurant default, “avoiding repeated values on each item,” or specify their own preparation time.

2. **Representative case:** With a 15-minute restaurant default, `null` means 15 minutes and explicit `0` means zero minutes. The example explicitly calls these “contract results, not behavior delivered by this PR.”

3. **Current increment:** The `review-base` → `review-head` paragraph says only `contract.json` changes, replacing an empty object with the field type, bounds of 0–90 minutes, and inheritance/zero meanings. Validation establishes only that the JSON parsed successfully.

4. **Outside it:** Runtime integration remains future work: unchanged `resolve.py` still raises `NotImplementedError`, despite the `runtime-complete` label. “Persistence, scheduling and the user interface remain separate work.” No runtime tests or deployment were performed.

5. **Decision still needed:** The product owner must decide “whether inherited values display a badge” in the UI. The artifact identifies no other pending decisions; whether others exist is unknown.
