# Record the preparation-time override contract

Restaurant defaults avoid repeating preparation times on every item. This PR
records the accepted contract in `contract.json`: an item's `prep_minutes` may
be `null` or an integer from 0 to 90 inclusive. `null` inherits the restaurant
default; `0` is an explicit override.

With a restaurant default of 15 minutes, a `null` override specifies 15 minutes
and an explicit `0` specifies 0 minutes. These are the accepted contract results;
runtime integration remains future work.

The `review-base` → `review-head` diff changes only `contract.json`, replacing its
empty object with this contract. `requirements.md` and `resolve.py` are unchanged;
the resolver still raises `NotImplementedError`. Review the contract's null
handling, inclusive bounds and explicit-zero semantics against `requirements.md`.

Persistence, scheduling and the user interface remain separate work. The product
owner still needs to decide whether inherited values display a badge.

Validation: the supplied record reports that the contract JSON parsed
successfully. No tests were added, and no runtime tests or deployment were
performed. JSON parsing does not verify runtime behavior.
