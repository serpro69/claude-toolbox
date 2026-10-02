# Preparation-time override contract

Restaurant defaults avoid duplicating preparation times on every item. This PR
records the accepted contract for an item's `prep_minutes` override: `null`
inherits the restaurant default; an integer from 0 through 90 supplies an explicit
value, including zero.

With a restaurant default of 15 minutes, the contract specifies 15 minutes for
`null` and 0 minutes for an explicit zero. These are specified results; runtime
integration remains future work. Orders do not gain default resolution in this PR.

The diff from `review-base` (`48aee21`) to `review-head` (`0658ef5`) changes only
`contract.json`, replacing an empty object with the field's type, bounds and
inheritance rules. The accepted requirements already exist in `requirements.md`.
The resolver in `resolve.py` is unchanged and still raises `NotImplementedError`.
Review `contract.json` against those requirements, especially the distinction
between `null` and zero and the inclusive 0–90 range.

Persistence, scheduling and the user interface remain separate work alongside
runtime integration. The product owner still needs to decide whether the UI
displays a badge for inherited values.

Validation: the contract JSON parsed successfully. No tests were added, and no
runtime tests or deployment were performed. Parsing confirms JSON syntax; it does
not verify runtime behavior.
