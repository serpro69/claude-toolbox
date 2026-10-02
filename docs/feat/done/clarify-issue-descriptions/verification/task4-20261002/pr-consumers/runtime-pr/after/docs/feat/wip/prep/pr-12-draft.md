Resolve an item's preparation time from its restaurant default and optional
`prep_minutes` override, so items can share a default without repeating it.

## Behavior

The accepted contract allows `prep_minutes` to be null or an integer from 0–90
inclusive. Null means “inherit the restaurant default”; zero is an explicit
override. With a 15-minute default:

- A null override resolves to 15 minutes.
- A zero override resolves to 0 minutes.
- A 7-minute override resolves to 7 minutes.

## Changes and review scope

This PR implements `effective_minutes(default, override)` in `resolve.py`, replacing
the runtime placeholder, and adds the three assertions above in `test_resolve.py`.
The helper falls back to the default only when the override is `None`; it does not
validate the allowed range.

The actual PR diff (`7c54cf1` → `761325c`) changes only those two files. The nullable
field and accepted contract in `contract.json` and `requirements.md` already exist
in the base and remain unchanged. Review the `None`-specific fallback and the tests
that preserve zero and other explicit overrides.

## Validation and remaining work

The supplied validation record reports that all three assertions passed at the PR
head. This validates the listed resolution cases; persistence and deployment were
not validated.

Persistence, scheduling and the user interface remain separate work. The product
owner still needs to decide whether inherited values display a badge.
