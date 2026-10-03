## Setup

Explicitly select /kk:design through the harness for canonical instructions and $kk:design for generated instructions. This is a behavior regression, not implicit routing. Use a fresh workspace outside any SKILL.md ancestor. Permit reads of the selected variant's operative instruction closure, including shared references and profile detection/content, and staged fixtures only; never stage eval.json or any oracle. File-read/search and fixture-scoped editing tools are available; web, knowledge-store, external service and independent-review tools are unavailable, with no synthetic responses. Map test-files/accepted.md to accepted.md at workspace root. Only docs/feat/wip/archive-label/{design,implementation,tasks}.md may be created. Keep accepted.md read-only. Existing oracle/expected.json is grader-only. All refinement and presentation approvals are already in the unchanged prompt and fixture; no further replies are scripted.

## Start

Select the design skill through the harness, then send eval.json.prompt exactly once unchanged. Only in the generated variant, convert the explicit /kk:design spelling in the clarity-after-drafting prompt to $kk:design; all other prompt text remains byte-identical.

## Replies

| ID | Send when | Exact user reply |
| --- | --- | --- |

## Stop

Max assistant turns: 1.

Check completion first: all three planning artifacts exist and the assistant gives its follow-up recommendations; terminate `complete`. No early stop is scripted. Otherwise, if input is needed and no unused row matches, stop `off-script`; at the bound stop `turn-limit`. Send at most one unused row per response, the first matching row; never resend or improvise replies.

## Grade

| Assertion | Observable evidence |
| --- | --- |
| 5.1 | Inspect the complete ordered transcript and tool trace against this unchanged assertion; for artifact assertions inspect the final files and links too. |
| 5.2 | Inspect the complete ordered transcript and tool trace against this unchanged assertion; for artifact assertions inspect the final files and links too. |
| 5.3 | Inspect the complete ordered transcript and tool trace against this unchanged assertion; for artifact assertions inspect the final files and links too. |
| 5.4 | Inspect the complete ordered transcript and tool trace against this unchanged assertion; for artifact assertions inspect the final files and links too. |
| 5.5 | Inspect the complete ordered transcript and tool trace against this unchanged assertion; for artifact assertions inspect the final files and links too. |

Grade each PASS/FAIL/PARTIAL. Unreached or unobservable behavior is PARTIAL. Oracle access or an incomplete trace invalidates execution.
