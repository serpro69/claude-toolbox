# Resolve preparation-time overrides

This PR implements preparation-time selection in `effective_minutes(default, override)`. Restaurant defaults avoid repeating the same preparation time on every item: a null item override inherits the restaurant default, while an explicit override replaces it, including zero.

For a restaurant default of 15 minutes, a null override resolves to 15, zero resolves to 0, and an override of 7 resolves to 7.

## Changes in this PR

The actual diff from `review-base` (`3ace972e33ad800bde05b54ca9d58747287c5df5`) to `review-head` (`b615d57370dfbdda263ef319c1317ca8dfa903c7`) replaces the resolver's `NotImplementedError` with this selection behavior and adds three assertions in `test_resolve.py`.

The accepted nullable `prep_minutes` contract, including the allowed integer range of 0–90, is already present at the base revision in `contract.json` and `requirements.md`. Despite the stack's “schema-only” label, this increment implements the runtime helper; it does not add the schema. The helper selects between the supplied values and does not enforce the range itself.

## Review and validation

Review the `resolve.py` change and the three new assertions in `test_resolve.py`, using the existing contract and requirements for context. The supplied validation record reports all three assertions passed at head, covering inheritance, an explicit zero, and an explicit positive override. These cases do not demonstrate range enforcement, persistence, or deployment behavior. No persistence or deployment validation is recorded.

## Separate work and open decision

Persistence, scheduling, and the user interface remain separate work. The product owner still needs to decide whether inherited values display a badge; the next step is to resolve that display decision for the UI work.
