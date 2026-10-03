## Setup

Explicitly select /kk:design through the harness for canonical instructions and $kk:design for generated instructions. This is a behavior regression, not implicit routing. Use a fresh workspace outside any SKILL.md ancestor. Permit reads of the selected variant's operative instruction closure, including shared references and profile detection/content, and staged fixtures only; never stage eval.json or any oracle. File-read/search and fixture-scoped editing tools are available; web, knowledge-store, external service and independent-review tools are unavailable, with no synthetic responses. Map test-files/design.md to docs/feat/wip/auth-refactor/design.md and test-files/tasks.md to docs/feat/wip/auth-refactor/tasks.md. Do not invent implementation.md or runtime source: their absence is part of the supplied fixture. Permit edits only to the existing two documents or a newly drafted docs/feat/wip/auth-refactor/implementation.md if a scripted reply authorizes it. No implementation outside these documents is possible from this fixture.

## Start

Select the design skill through the harness, then send eval.json.prompt exactly once unchanged. Only in the generated variant, convert the explicit /kk:design spelling in the clarity-after-drafting prompt to $kk:design; all other prompt text remains byte-identical.

## Replies

| ID | Send when | Exact user reply |
| --- | --- | --- |
| W1 | The assistant asks about the missing implementation.md, missing runtime source, or whether to refine the incomplete plan. | The supplied documents are all that is available. Keep completed work and existing decisions intact, identify the next pending work, and refine the documentation if needed; stop at the implementation handoff. |
| W2 | The assistant asks to activate a technical profile based on the WIP prose. | Do not activate a technology profile; the available material is the existing design and task list only. |

## Stop

Max assistant turns: 4.

Check completion first: the assistant identifies Task 2 remaining refresh-flow tests and reaches a readiness/refinement or implementation-handoff boundary without fresh-idea subphases; terminate `complete`. If missing fixtures prevent the required resume behavior, grade that assertion PARTIAL rather than inventing evidence. No early stop is scripted. Otherwise, if input is needed and no unused row matches, stop `off-script`; at the bound stop `turn-limit`. Send at most one unused row per response, the first matching row; never resend or improvise replies.

## Grade

| Assertion | Observable evidence |
| --- | --- |
| 4.1 | Inspect the complete ordered transcript and tool trace against this unchanged assertion; for artifact assertions inspect the final files and links too. |
| 4.2 | Inspect the complete ordered transcript and tool trace against this unchanged assertion; for artifact assertions inspect the final files and links too. |
| 4.3 | Inspect the complete ordered transcript and tool trace against this unchanged assertion; for artifact assertions inspect the final files and links too. |
| 4.4 | Inspect the complete ordered transcript and tool trace against this unchanged assertion; for artifact assertions inspect the final files and links too. |
| 4.5 | Inspect the complete ordered transcript and tool trace against this unchanged assertion; for artifact assertions inspect the final files and links too. |

Grade each PASS/FAIL/PARTIAL. Unreached or unobservable behavior is PARTIAL. Oracle access or an incomplete trace invalidates execution.
