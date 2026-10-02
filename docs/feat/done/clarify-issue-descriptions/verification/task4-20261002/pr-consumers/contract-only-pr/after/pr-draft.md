# Preparation-time override contract

This PR records the accepted preparation-time contract in `contract.json`.
Restaurant defaults avoid repeating the same preparation time on every item;
an item can specify its own value or inherit the restaurant default.

The contract defines `prep_minutes` as an integer from 0 through 90, inclusive,
or `null`. With a restaurant default of 15 minutes, the specified results are:

- `null`: inherit the default, giving 15 minutes.
- `0`: use an explicit override of 0 minutes.

These are contract examples; runtime resolution remains future work.

Only `contract.json` changes in this PR. The accepted requirements in
`requirements.md` and the resolver stub in `resolve.py` are unchanged. The stub
still raises `NotImplementedError`, so this PR does not enable order-time
resolution. Review the contract's allowed values and its distinction between
inheritance and an explicit zero against the requirements.

Persistence, scheduling and the user interface are separate work. The product
owner still needs to decide whether inherited values should display a badge.

Recorded validation: the contract JSON parsed successfully. This diff adds no
tests; no runtime tests or deployment were performed.
