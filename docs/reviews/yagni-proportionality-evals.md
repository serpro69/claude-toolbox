# YAGNI / proportionality change — review-code over-application evals

Date: 2026-11-04. Candidate: `dfb76054` on branch `yagni-proportionality`
("Apply YAGNI to design plans and make scope reviews two-sided").

## Question and decision rule

The change lets `/kk:review-code` flag code that does not trace to the stated
problem, even when an approved design requested it. The risk is
over-application: simplifying away necessary recovery, or treating planned,
unreachable scaffolding as removable scope.

- **Material assertions:** 11.4 and 12.4 (no simplification of required
  behavior; no demands without a demonstrated current issue).
- **Quality observations:** 11.2–11.3, 11.5, 12.2–12.3, 12.5.
- **Out of scope for this mode:** 11.1, 11.6, 12.1, 12.6 (instruction order and
  isolated dispatch payloads need workflow mode; this change does not touch them).
- **Rule:** one repetition each. If both material assertions pass, accept. If
  either fails, run the immediate predecessor (`master` at `91550c42`) on that
  eval to separate a regression from pre-existing behavior.

## Harness

Component mode per `klaude-plugin/skills/review-code/evals/_harness/HARNESS.md`:
`kk:profile-resolver` → `kk:code-reviewer` → `kk:eval-grader`, one chain per
eval, staged with `setup.sh` outside any `SKILL.md` ancestor.

- Plugin root: `git archive dfb76054 klaude-plugin` with every `evals/` subtree
  removed (no grading material reachable by actors).
- Reviewer payload: the harness template plus the candidate worktree path and,
  for eval 11, the no-task-scope block. This matches the evidence the real
  isolated workflow supplies; no prompt, trap or assertion text was passed.
- Single model (session default) for all actors.

## Results

| Eval | Assertions | Pass | Fail | Partial |
|---|---|---|---|---|
| functional-justified-recovery (11) | 11.1–11.6 (6) | 4 | 0 | 2 |
| functional-clean-partial-feature (12) | 12.1–12.6 (6) | 4 | 0 | 2 |
| **Total** | 12 | 8 | 0 | 4 |

All four PARTIALs are the out-of-scope workflow assertions (x.1 ordering, x.6
dispatch payloads), which component-mode output text cannot establish. Both
material assertions passed, so no baseline run was made.

## Highlights

- **Eval 11:** APPROVE, no findings. The reviewer traced the trim through
  `read_resilient` and described the new retry/exhaustion/permanent-error tests
  as "proportionate verification, not speculative scope". It did not suggest
  removing or bypassing the retry.
- **Eval 12:** APPROVE, no findings. The reviewer explicitly considered the
  YAGNI challenge on the unreachable stub and did not raise it: Task 1 requests
  the code, Task 2 is the concrete follow-up, and the cost is negligible. This
  is the intended proportionate outcome, not suppression of the new rule.

## Limits

- One repetition per eval; this shows no regression on these fixtures, not
  reliability.
- The `kk:code-reviewer` agent definition came from the installed plugin
  (0.25.2). The candidate's one-line restatement in `agents/code-reviewer.md` was
  not exercised; the candidate `functional-review.md` it loads was.
- No `/kk:design` or `/kk:review-design` eval covers the new size/lifetime,
  classification or Proportionality guidance. A design eval using the
  "add one map field to 8 documents" prompt, with a proportionate-design
  control for review-design, would be the next useful check if those paths
  regress in practice.
