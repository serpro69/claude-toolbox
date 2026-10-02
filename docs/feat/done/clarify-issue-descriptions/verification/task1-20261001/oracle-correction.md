# Scenario 17 oracle correction

The initial grade remains preserved as PARTIAL in
[the original report](issues/issue-local-draft/grading/final.md), with its original
oracle snapshot. Before regrading, the independent code-reviewer compared the
disputed expectations to the accepted design, implementation plan, fixtures,
artifacts and reader answers and identified a **P2 oracle defect (98% confidence)**.

Q4 asks what remains outside the issue. Its original expected answer combined
asynchronous-export scope with a demand to state that implementing a fix is outside
this editorial task. The latter is an editor-action boundary, not a required topic
inside a bug report. Design Editorial behavior defines reader scope; its final
paragraph and implementation scenario 17 prohibit implementation actions. Assertion
17.4 directly checks those actions. The issue itself still calls for a future fix.

Q3 originally demanded that the artifact name the editor as the actor who did not
reproduce. The required distinction is inspected source versus unconfirmed runtime
behavior/causation. Both edited artifacts and readers preserve that distinction,
as the original grader's PASS for 17.3 already establishes. Requiring narration of
the editing session would add an unsupported product-document requirement.

Apply the independent reviewer's exact minimal correction to the canonical oracle:

- Q3: “The source uses timeout_ms or 30000 and replaces zero with the fallback; this
  is source evidence, not runtime confirmation of the reported behavior or its
  cause, and Mina still needs to confirm the reported build before a fix is chosen.”
- Q4: “Asynchronous export.”

All questions, assertions, fixtures, prompts, instructions and resulting artifacts
remain unchanged. No prohibition on implementation, reproduction, invented
verification, source edits or extra outputs is removed. The original reader's
missing inspected-source evidence remains a legitimate Q3 limitation.

The corrected expected answers are a versioned oracle correction, not a skill fix
or a passing result. Preserve the original oracle/grade, save a separate corrected
oracle before dispatch, and independently regrade the existing complete audited
traces and unchanged answers. No editor rerun is needed because the questions,
inputs and operative instructions did not change. The regrade must remain distinct
from the original result, and any remaining failures remain failures.
