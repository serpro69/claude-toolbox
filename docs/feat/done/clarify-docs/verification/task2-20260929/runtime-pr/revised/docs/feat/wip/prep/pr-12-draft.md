# Resolve item preparation-time overrides

Restaurant defaults avoid repeating preparation times on every item. This PR
implements `effective_minutes(default, override)` in `resolve.py`: a null override
(`None` in Python) inherits the restaurant default, while an explicit value,
including zero, is returned unchanged. Previously, the function raised
`NotImplementedError`.

For a restaurant default of 15 minutes, a null override resolves to 15 minutes,
zero resolves to 0 minutes, and an override of 7 resolves to 7 minutes.

## Scope and review

The actual `review-base` → `review-head` diff changes `resolve.py` and adds
`test_resolve.py`. Despite the stack's “schema-only” title, this increment delivers
runtime resolution logic. The accepted nullable `prep_minutes` contract already
exists at the base and is unchanged: null means inherit, zero is an explicit
override, and allowed values are 0–90 minutes. The resolver selects a value; it
does not enforce that range.

Review `resolve.py` for the null-versus-zero behavior, then `test_resolve.py` for
the three exercised cases. `requirements.md` and `contract.json` provide the
accepted contract behind this change. Persistence, scheduling and user-interface
integration remain separate work.

## Validation

The supplied validation record reports that all three assertions in
`test_resolve.py` passed at `review-head`: inheritance, explicit zero, and an
explicit positive override. These assertions do not exercise range enforcement,
persistence or deployment; no persistence or deployment validation was reported.

## Open decision

The product owner still needs to decide whether inherited preparation times
display a badge. Resolve that choice for the separate user-interface work; this
PR does not implement a badge policy.
