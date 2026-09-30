# Resolve item preparation time from the restaurant default or override

Restaurant defaults avoid repeating preparation times on every item. This PR
implements `effective_minutes(default, override)` in `resolve.py`: a null override
(`None` in Python) inherits the restaurant default, while any supplied override,
including zero, takes precedence.

For a restaurant default of 15 minutes, the helper returns 15 for a null override,
0 for an explicit zero, and 7 for an override of 7 minutes.

## What changes in this PR

The review diff is `review-base` (`08e5cd1`) to `review-head` (`af341ff`). It replaces
the helper's `NotImplementedError` with runtime resolution and adds
`test_resolve.py`. The stack's “schema-only” title does not describe this increment.

The accepted `prep_minutes` contract already exists at the base revision and is
unchanged: an item override is nullable, null inherits the restaurant default,
zero is an explicit value, and non-null values must be integers from 0 through 90.
The helper selects the effective value; it does not validate the allowed range.
Persistence, scheduling and the user interface remain separate work.

## Review and validation

Review the base-to-head change in `resolve.py`, then the new assertions in
`test_resolve.py`. Use the unchanged `requirements.md` and `contract.json` for the
accepted semantics.

The supplied validation record reports that all three new assertions passed at
head: inheritance with a default of 15, an explicit zero, and a nonzero override
of 7. These assertions do not cover range validation. No persistence or deployment
validation is recorded.

## Open decision

The product owner still needs to decide whether inherited values display a badge.
That decision belongs to the separate user-interface work.
