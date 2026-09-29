# Visibility retry after explicit destination placement

[Retry-1](../retry-1/grading/verdicts.md) passed all seven original scenario assertions
and both readers scored 5/5, but failed the strengthened shared procedure: successful
JSON parsing was reported only to the caller and remained absent from the destination
draft. Its failure and the initial visibility pass remain preserved.

The main agent made the placement rule explicit: validation outcomes and limits
belong in the draft; completion messages do not substitute. This [instruction diff](instruction-diff.diff)
is the only semantic input change from retry-1. The final shared instruction hash is
`624f14dd7e033c729b116cc65f93af79c4663dff6ca9e34b2b5c24bd89198b5d`.

This correction-based retry keeps all fixture bytes, actual Git refs, scenario prompt,
questions, oracle and assertions unchanged. New editor and reader sessions receive no
earlier artifacts, findings or expected answers. A fresh independent grader checks
the seven assertions, full procedure compliance, and applicability of the other four
latest passing PR cases to the final instruction snapshot. No acceptance is softened.
