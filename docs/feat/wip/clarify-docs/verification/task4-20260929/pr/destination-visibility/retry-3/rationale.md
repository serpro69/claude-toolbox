# Explicit validation-outcome regression run

The initial visibility run passed its seven assertions. Updated-procedure retries
[1](../retry-1/grading/verdicts.md) and [2](../retry-2/grading/verdicts.md) also passed
those assertions and retained 5/5 reader answers, but failed full procedure compliance:
their drafts named JSON parsing without stating its successful outcome. All prior
results remain preserved.

The main agent made the rule concrete: validation outcomes must be passed, failed or
unavailable; check names and completion reports cannot substitute. The frozen shared
SHA256 is `5908c353733671baffd74e0e8e17bfac2b9c3eb62bd3423643896613b7590e35`.
See the [instruction diff](instruction-diff.diff).

Before this editor ran, the main agent also authored permanent assertion 13.8 and
strengthened the oracle's validation claim and predeclared baseline defect. See the
[assertion diff](assertion-diff.diff) and [oracle diff](oracle-diff.diff). This adds
coverage; it does not weaken the original seven assertions, which remain byte-for-byte
equal as JSON values. Questions, expected reader answers, user prompt, source fixtures
and Git refs remain unchanged. Earlier oracle snapshots are intact.

Editor and readers are fresh and receive no oracle, previous outputs or grading
feedback. A fresh grader assesses all eight assertions, full procedure compliance
and applicability of the other four latest passing PR runs. This is a documented
source correction and added regression coverage, not a repeated unchanged sample.
