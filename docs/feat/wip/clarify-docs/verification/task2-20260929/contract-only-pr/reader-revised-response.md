1. **Why:** “Restaurant defaults avoid repeating preparation times on each item.” This PR records the accepted item-override contract.

2. **Representative case:** With a 20-minute restaurant default, `null` means 20 minutes; `0` explicitly means 0 minutes. This is specified behavior, not implemented runtime behavior.

3. **Current increment:** Only `contract.json` changes, replacing an empty object with the contract: `prep_minutes` accepts integers from 0 through 90 or `null`. Validation confirms JSON syntax only.

4. **Outside scope:** Runtime resolution, persistence, scheduling, and the user interface. `effective_minutes` still raises `NotImplementedError`; no runtime tests or deployment were performed.

5. **Pending decision:** The product owner must decide “whether inherited values display a badge.” No other pending decisions are identified in the artifact.
