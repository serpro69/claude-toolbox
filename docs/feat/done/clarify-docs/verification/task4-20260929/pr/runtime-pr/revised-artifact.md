# Resolve preparation time from an item override or restaurant default

Restaurant defaults let items share a preparation time without duplicating it on
every item. This PR implements `effective_minutes(default, override)`: a null
override (`None` in Python) inherits the restaurant default; an explicit override,
including zero, takes precedence.

For a restaurant default of 15 minutes, a null override resolves to 15, zero
resolves to 0, and an override of 7 resolves to 7.

## Current increment and review path

The review range is base `08e5cd169c65117c509ec3b58bebdd229df194a0` to head
`af341ff761181751094e5ed58ee7fde3cf6ef65d` (`review-base` to `review-head`).
The accepted nullable `prep_minutes` contract is already present in the base.
It allows integer values from 0 through 90, with null meaning inheritance and zero
meaning an explicit override.

Start with `resolve.py`: this change replaces the `NotImplementedError` placeholder
with the runtime selection of the default or override. Then review
`test_resolve.py` for the three cases above. `requirements.md` and `contract.json`
provide the unchanged requirements and schema. The resolver selects a value; it
does not itself enforce the contract's 0–90 range.

## Validation and remaining work

The supplied validation record reports that all three assertions in
`test_resolve.py` passed at head. They exercise null inheritance, an explicit zero,
and an explicit positive override; they do not establish range validation or
end-to-end integration. No persistence or deployment validation is recorded.

Persistence, scheduling, and the user interface remain separate work. The product
owner still needs to decide whether inherited values display a badge; that decision
remains open for the UI work.
