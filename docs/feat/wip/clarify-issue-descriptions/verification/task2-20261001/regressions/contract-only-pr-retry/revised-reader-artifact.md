# Define the preparation-time override contract

Restaurant defaults avoid repeating the same preparation time for every item.
This PR records the accepted contract for `prep_minutes`: an item override may
be an integer from 0 through 90 minutes, inclusive, or `null` to inherit the
restaurant default. Zero is an explicit override.

For a restaurant default of 15 minutes, `null` specifies 15 minutes and an
explicit zero specifies 0 minutes. These are specified results for future runtime
integration; this PR does not make defaults resolve for orders.

The `review-base` to `review-head` diff changes only `contract.json`, replacing
an empty object with the field type, bounds and null/zero meanings. Review those
definitions against the accepted contract in `requirements.md`. The requirements
and `resolve.py` are unchanged; `effective_minutes` still raises
`NotImplementedError`.

Runtime integration, persistence, scheduling and the user interface remain
future work. The product owner still needs to decide whether inherited values
display a badge.

Validation: the contract JSON parsed successfully. No tests were added, and no
runtime tests or deployment were performed; parsing does not verify runtime
behavior.
