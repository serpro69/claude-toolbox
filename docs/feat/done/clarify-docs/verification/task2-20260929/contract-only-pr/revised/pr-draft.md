# Define the preparation-time override contract

Restaurant defaults avoid repeating preparation times on each item. This PR records
the accepted item-override contract in `contract.json`: `prep_minutes` may be an
integer from 0 through 90, inclusive, or `null`. Null means inherit the restaurant
default; zero is an explicit override.

For example, with a restaurant default of 20 minutes, the contract calls for a null
override to use 20 minutes and a zero override to use 0 minutes. Runtime resolution
is still future work: `effective_minutes` in `resolve.py` continues to raise
`NotImplementedError`.

The `review-base` → `review-head` diff changes only `contract.json`, replacing its
empty object with this contract. Review that diff against `requirements.md`; use
`resolve.py` to confirm the runtime boundary. Persistence, scheduling and the user
interface remain separate work. The product owner still needs to decide whether
inherited values display a badge.

Validation recorded for this PR: the contract JSON parsed successfully. This checks
JSON syntax only; no runtime tests or deployment were performed.
