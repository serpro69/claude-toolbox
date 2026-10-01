# Resolve item preparation-time overrides

Restaurant preparation-time defaults avoid repeating the same value on every item. This PR implements `effective_minutes(default, override)`: a null override (`None` in Python) uses the restaurant default, while any supplied override—including zero—is returned as the item's value.

For a restaurant default of 15 minutes:

- A null item override resolves to 15 minutes.
- An explicit zero resolves to 0 minutes.
- An explicit override of 7 resolves to 7 minutes.

## Changes in this PR

The review diff is `review-base` (`3ace972`) to `review-head` (`b615d57`). The nullable `prep_minutes` contract in `contract.json` is already present at the base and is unchanged here. The accepted contract allows integer values from 0 through 90; null means inherit the restaurant default, and zero is an explicit override.

This increment replaces the `NotImplementedError` in `resolve.py` with runtime resolution and adds three assertions in `test_resolve.py` covering inheritance, explicit zero and a positive override. Review those two files for this increment. The resolver selects a value; it adds no type or range validation.

## Validation

The supplied validation record reports that all three assertions passed at the PR head. The assertions exercise the examples above; they do not establish type or range enforcement. No persistence or deployment validation is available.

## Separate work and open decision

Persistence, scheduling and the user interface remain separate work. The product owner still needs to decide whether inherited values display a badge; the next step is to record that decision for the UI work. The preparation-time contract itself is already accepted in `requirements.md`.
