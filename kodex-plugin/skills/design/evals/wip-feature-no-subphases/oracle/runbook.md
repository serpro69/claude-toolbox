## Setup

Explicitly select $kk:design through the harness for canonical instructions and $kk:design for generated instructions. This is a behavior regression, not implicit routing. Use a fresh workspace outside any SKILL.md ancestor. Permit reads of the selected variant's operative instruction closure, including shared references and profile detection/content, and staged fixtures only; never stage eval.json or any oracle. File-read/search and fixture-scoped editing tools are available; web, knowledge-store, external service and independent-review tools are unavailable, with no synthetic responses. Map test-files/design.md to docs/feat/wip/auth-refactor/design.md and test-files/tasks.md to docs/feat/wip/auth-refactor/tasks.md. Do not invent implementation.md or runtime source: their absence is part of the supplied fixture. Permit edits only to the existing two documents or a newly drafted docs/feat/wip/auth-refactor/implementation.md if a scripted reply authorizes it. No implementation outside these documents is possible from this fixture.

## Start

Select the design skill through the harness, then send `eval.json.prompt` exactly once. For generated instructions only, mechanically replace an explicit `$kk:` invocation with `$kk:`; leave natural-language prompts unchanged.

## Replies

| ID | Send when | Exact user reply |
| --- | --- | --- |
| W1 | The assistant asks whether the refresh-token cookie is allowed or how the storage prohibition should be interpreted. | The approved constraint permits an HttpOnly, Secure session cookie for the refresh token; it prohibits persistent cookies and localStorage. Keep the existing token lifetimes and rotation, with the cookie ending at the browser session. Clarify that distinction in the design, preserve completed tasks, and draft the missing implementation plan from the supplied decisions. Stop at the implementation handoff; no runtime code is available. |
| W2 | The assistant asks whether existing clients stay unchanged or must adopt Authorization headers during migration. | Existing legacy clients must keep working unchanged during the dual-auth transition. New clients use Authorization headers; old-session support is retired after the stated transition window. Clarify that compatibility boundary in the design, preserve completed tasks, and draft the missing implementation plan from the supplied decisions. Stop at the implementation handoff; no runtime code is available. |
| W3 | The assistant asks about the missing implementation.md, missing runtime source, or permission to refine the plan, without asking W1 or W2's specific policy question. | The supplied documents are all the available project material. Refine the design and remaining tasks as needed and draft implementation.md from the accepted decisions, keeping completed tasks intact. Stop at the implementation handoff; do not invent runtime files or begin coding. |
| W4 | The assistant asks to activate a technical profile based on the WIP prose. | Do not activate a technology profile; the available material is the existing design and task list only. |

## Stop

Max assistant turns: 6.

Check completion first: the assistant substantively refines the existing design/tasks, creates the missing implementation plan after a scripted authorization, identifies Task 2.2 as the next work, and stops at the implementation handoff without fresh-idea subphases; terminate `complete`. Merely identifying readiness gaps is not completion. If unscripted missing prerequisites prevent resumption, grade that assertion PARTIAL rather than inventing evidence. No early stop is scripted. Otherwise, if input is needed and no unused row matches, stop `off-script`; at the bound stop `turn-limit`. Send at most one unused row per response, the first matching row; never resend or improvise replies.

## Grade

| Assertion | Observable evidence |
| --- | --- |
| 4.1 | Trace loads existing-task-process.md and response recognizes existing WIP work. |
| 4.2 | Full response sequence contains no fresh HMW framing. |
| 4.3 | No who/success/constraints foundation interview occurs. |
| 4.4 | No alternative generation or diverge phase occurs. |
| 4.5 | Reads mapped documents, identifies Task 2.2 and resumes the existing-task workflow; distinguish a readiness assessment from actual implementation or substantive refinement. If absent prerequisites prevent resumption, grade PARTIAL. |

Grade each PASS/FAIL/PARTIAL. Unreached or unobservable behavior is PARTIAL. Oracle access or an incomplete trace invalidates execution.
