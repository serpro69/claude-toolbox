# Source-disagreement rerun

Date: 2026-09-29. The first run's assertion 2.1 was PARTIAL: its reader explained the
timing conflict but answered the generic representative-case question with the
initial lookup at 15, omitting the required change to 20. That result is retained
in [the original verdict](../../task1-20260929/source-disagreement/verdicts.md).

Before this rerun's editor started, question 2 was made concrete: “When a restaurant
default changes from 15 to 20, what happens to new inherited lookups and existing
orders?” Expected answers, protected claims and all five assertions are unchanged.
The original and revised reader sessions receive the same revised question set.
No additional answer clues, oracle or source-only editor context go to either reader.

The editor starts again from the unchanged fixture in a fresh session. The entry
point and shared instructions are unchanged (hashes in the manifest); only the eval
question was refined. The canonical question was changed before spawning the editor
(attested by the originating tool-call order). The oracle and eval definition were
exported under grader-inputs/ after the editor completed; these copies do not prove
declaration timing by their timestamps. The previous oracle is preserved under the original
run's grader-inputs/. This is a separate attempt, not replacement evidence for the
earlier partial outcome.
