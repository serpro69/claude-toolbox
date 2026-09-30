# Preparation-time override contract

This PR records the accepted preparation-time contract: items can inherit a
restaurant default, avoiding repeated values on each item, or specify their own
preparation time. It defines the intended behavior; runtime integration remains
future work.

For `prep_minutes`:

- `null` means inherit the restaurant default.
- An integer from 0 through 90 minutes is an explicit override. Zero is a valid
  value, not an instruction to inherit.

For example, with a restaurant default of 15 minutes, `null` specifies an effective
time of 15 minutes and an explicit `0` specifies 0 minutes. These are contract
results, not behavior delivered by this PR.

The `review-base` → `review-head` diff changes only `contract.json`, replacing an
empty object with the field type, bounds and inheritance/zero meanings. Review
that change against the accepted rules in `requirements.md`. The unchanged
`resolve.py` still raises `NotImplementedError`, so defaults do not yet resolve
at runtime despite the `runtime-complete` stack label.

Persistence, scheduling and the user interface remain separate work. For the UI
work, the product owner still needs to decide whether inherited values display
a badge.

Validation recorded: the contract JSON parsed successfully. No runtime tests or
deployment were performed; parsing does not establish runtime behavior.
