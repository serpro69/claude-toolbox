# Internal fixture review — 2026-10-23

Fresh agent `/root/fixture_internal`, with no parent conversation history. The
same criteria, selected candidate, contract, unchanged caller, proposal and
absent optional path were supplied as to both external reviewers. No file
contents, receipt markers or expected defects were supplied in the prompt.
The internal host uses shell-backed file reads, so its wrapper explicitly
permitted only read-only `cat`/`sed` as its native Read adaptation. The external
wrappers use native file tools. This is a tool adaptation, not byte-identical
prompt execution; substantive criteria/evidence and no-edit scope are equivalent.

## Returned findings (native severity retained)

- **P2 — Initial retry delay violates the contract.** `snapshots/candidate.txt:3`
  returns `10` for every attempt. `project/contract.md:5` requires `5` for attempt
  zero, which `project/caller.txt:1` passes. That caller's assertion would fail.
  Return `5` when `attempt == 0` and `10` for later attempts.
- **P2 — Proposal contradicts its unchanged-contract claim.**
  `project/design.md:5` states that the public contract is unchanged while
  proposing `10` seconds for attempt zero. Revise the proposed behavior to
  preserve the initial delay.

The reviewer reported criteria-first reads, inspection of the selected snapshot
and all three supporting targets, no tests/edits, and no substitution of the
worktree `retry.txt`. The proposal was assessed as future work, not missing code.
`project/optional-context.md` was unavailable because it does not exist.

Returned file-only markers: `COPPER-LANTERN-317`, `VIOLET-COMET-951`,
`MOSS-HARBOR-826`, `SILVER-BIRCH-462`. These demonstrate tested fixture access;
the parent did not receive a separate raw child tool trace. This reviewer is
the internal reviewer, not an additional non-authoring external provider.
