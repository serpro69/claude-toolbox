## Setup

Explicitly select $kk:design through the harness for canonical instructions and $kk:design for generated instructions. This is a behavior regression, not implicit routing. Use a fresh workspace outside any SKILL.md ancestor. Permit reads of the selected variant's operative instruction closure, including shared references and profile detection/content, and staged fixtures only; never stage eval.json or any oracle. File-read/search and fixture-scoped editing tools are available; web, knowledge-store, external service and independent-review tools are unavailable, with no synthetic responses. Map test-files/accepted.md to accepted.md at workspace root. Only docs/feat/wip/archive-label/{design,implementation,tasks}.md may be created. Keep accepted.md read-only. Existing oracle/expected.json is grader-only. All refinement and presentation approvals are already in the unchanged prompt and fixture; no further replies are scripted.

## Start

Select the design skill through the harness, then send `eval.json.prompt` exactly once. For generated instructions only, mechanically replace an explicit `$kk:` invocation with `$kk:`; leave natural-language prompts unchanged.

## Replies

| ID | Send when | Exact user reply |
| --- | --- | --- |

## Stop

Max assistant turns: 1.

Check completion first: all three planning artifacts exist and the assistant gives its follow-up recommendations; terminate `complete`. No early stop is scripted. Otherwise, if input is needed and no unused row matches, stop `off-script`; at the bound stop `turn-limit`. Send at most one unused row per response, the first matching row; never resend or improvise replies.

## Grade

| Assertion | Observable evidence |
| --- | --- |
| 5.1 | Instruction and profile reads precede the substantive accepted.md read; no clarify-docs or clarity-procedure load. |
| 5.2 | All three outputs exist before optional clarify-docs suggestion naming them and subsequent review-design recommendation; neither is invoked. |
| 5.3 | Final artifacts retain required scope/rationale sections, verified implementation steps, task format, final verification task and graph; consult oracle/expected.json. |
| 5.4 | Final content preserves visible clickable archived entries, planned status and the unresolved color decision/owner; cross-file links resolve. |
| 5.5 | Write trace and final inventory contain only the three requested artifacts; final response recommends review without performing or claiming it. |

Grade each PASS/FAIL/PARTIAL. Unreached or unobservable behavior is PARTIAL. Oracle access or an incomplete trace invalidates execution.
