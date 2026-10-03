## Setup

Explicitly select /kk:design through the harness for canonical instructions and $kk:design for generated instructions. This is a behavior regression, not implicit routing. Use a fresh workspace outside any SKILL.md ancestor. Permit reads of the selected variant's operative instruction closure, including shared references and profile detection/content, and staged fixtures only; never stage eval.json or any oracle. File-read/search and fixture-scoped editing tools are available; web, knowledge-store, external service and independent-review tools are unavailable, with no synthetic responses. No fixtures or writes are permitted. A Go design-profile confirmation may be needed; no Go runtime source is supplied.

## Start

Select the design skill through the harness, then send `eval.json.prompt` exactly once. For generated instructions only, mechanically replace an explicit `/kk:` invocation with `$kk:`; leave natural-language prompts unchanged.

## Replies

| ID | Send when | Exact user reply |
| --- | --- | --- |
| P1 | The assistant asks whether to activate the Go profile. | Yes, activate the Go profile. |
| P2 | The assistant asks to confirm an HMW framing. | Yes, that framing matches the operational need. |
| P3 | The assistant asks who this serves. | The operations team and its existing monitoring probe. |
| P4 | The assistant asks for measurable success. | A healthy process responds with 200 and version plus uptime in under 10 milliseconds locally; no dependency checks are involved. |
| P5 | The assistant asks about constraints, existing routing, or implementation context. | Use the existing standard HTTP handler style, no new dependencies, no external probes, and a process-local uptime value. Runtime source is not supplied; only the design choice is needed now. |
| P6 | The assistant asks to confirm a simple classification or direct path plus one alternative. | Yes, the simple path is appropriate; show the direct approach and one alternative. |

## Stop

Max assistant turns: 10.

Check completion first: after P6 the assistant presents the direct approach plus one alternative; terminate `complete`. No further planning is requested in this run. No early stop is scripted. Otherwise, if input is needed and no unused row matches, stop `off-script`; at the bound stop `turn-limit`. Send at most one unused row per response, the first matching row; never resend or improvise replies.

## Grade

| Assertion | Observable evidence |
| --- | --- |
| 2.1 | Assistant explicitly classifies the idea as simple/straightforward. |
| 2.2 | Classification and rationale precede alternatives. |
| 2.3 | Assistant asks for classification confirmation and waits for P6. |
| 2.4 | Response after P6 contains the direct approach plus exactly one alternative. |
| 2.5 | Full conversation has no broad multi-framework expansion or third direction. |

Grade each PASS/FAIL/PARTIAL. Unreached or unobservable behavior is PARTIAL. Oracle access or an incomplete trace invalidates execution.
