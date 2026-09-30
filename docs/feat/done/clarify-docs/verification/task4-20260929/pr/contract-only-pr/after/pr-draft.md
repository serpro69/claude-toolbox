# Preparation-time contract

Restaurant defaults avoid repeating preparation times on every item. This PR
records the accepted item-override contract in `contract.json`: `prep_minutes`
accepts null or an integer from 0 through 90. Null means inherit the restaurant
default; zero is an explicit override. For a restaurant default of 15 minutes,
the specified result is 15 minutes for null and 0 minutes for an explicit zero.

The `review-base` to `review-head` diff changes only `contract.json`, replacing
its empty object with the contract. These are specified results, not working
runtime behavior: the unchanged `effective_minutes` function in `resolve.py`
still raises `NotImplementedError`. Runtime integration, persistence, scheduling
and the user interface remain future work. The product owner still needs to
decide whether inherited values display a badge.

Review `contract.json` against the accepted rules and example in `requirements.md`;
`resolve.py` shows the runtime integration boundary. Validation recorded for this
PR is successful JSON parsing of the contract. No runtime tests or deployment
were performed, so that check does not verify default resolution.
