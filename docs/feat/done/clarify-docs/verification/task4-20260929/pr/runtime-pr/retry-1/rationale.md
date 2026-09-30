# Runtime PR retry rationale

The initial independent grade is retained in [the initial verdict report](../../grading/verdicts.md):
assertion 12.1 is PARTIAL because the revised reader omits newly added tests from
the increment. The initial draft mentions the test file as a review target and
explains its assertions, but never explicitly identifies those tests as new.

The main agent changed only the shared procedure's PR paragraph to request explicit
identification of newly added tests. The [instruction diff](instruction-diff.diff)
and [new instruction hashes](instruction-hashes.json) record that narrow correction.
The original frozen instruction snapshot and all initial evidence remain intact.

This retry holds fixture bytes, real Git revisions/diff, scenario prompt, five
neutral questions, oracle and assertion texts constant. Editor and readers are
fresh sessions and receive no initial output, grader findings or expected answers.
Only the editor's shared instructions change. This is a correction-based retry,
not a repeated sample of unchanged instructions to obtain a favorable answer.

A fresh independent grader assesses the retry and whether the other four PR passes
remain applicable after the focused instruction change. Reader comparisons remain
observations of AI reader behavior rather than a human-comprehension claim.
