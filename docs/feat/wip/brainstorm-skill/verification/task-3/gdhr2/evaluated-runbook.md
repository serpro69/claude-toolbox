## Setup

Explicitly select /kk:design through the harness for canonical instructions and $kk:design for generated instructions. This is a behavior regression, not implicit routing. Use a fresh workspace outside any SKILL.md ancestor. Permit reads of the selected variant's operative instruction closure, including shared references and profile detection/content, and staged fixtures only; never stage eval.json or any oracle. File-read/search and fixture-scoped editing tools are available; web, knowledge-store, external service and independent-review tools are unavailable, with no synthetic responses. No fixtures or writes are permitted.

## Start

Select the design skill through the harness, then send eval.json.prompt exactly once unchanged. Only in the generated variant, convert the explicit /kk:design spelling in the clarity-after-drafting prompt to $kk:design; all other prompt text remains byte-identical.

## Replies

| ID | Send when | Exact user reply |
| --- | --- | --- |
| H1 | The assistant asks to confirm an HMW/problem framing. | Yes, that framing captures the latency problem; continue. |
| H2 | The assistant asks who the feature serves. | It serves customer support agents looking up order status during live calls. |
| H3 | The assistant asks for success or measurable outcomes. | Reduce p95 order-status response time from two seconds to under 300 milliseconds during the ordinary weekday peak. |
| H4 | The assistant asks about technical or system constraints. | Keep the existing API contract and deployment footprint. Do not cache customer-specific responses across customers; response freshness must stay within five seconds. |
| H5 | The assistant asks to confirm non-trivial complexity and exploration breadth after all foundations. | Yes, explore the alternatives within those constraints. |

## Stop

Max assistant turns: 10.

Check completion first: H2, H3, and H4 have been delivered and the next assistant response reaches complexity classification or alternatives; terminate `complete`. Do not continue to implementation. No early stop is scripted. Otherwise, if input is needed and no unused row matches, stop `off-script`; at the bound stop `turn-limit`. Send at most one unused row per response, the first matching row; never resend or improvise replies.

## Grade

| Assertion | Observable evidence |
| --- | --- |
| 1.1 | Inspect the complete ordered transcript and tool trace against this unchanged assertion; for artifact assertions inspect the final files and links too. |
| 1.2 | Inspect the complete ordered transcript and tool trace against this unchanged assertion; for artifact assertions inspect the final files and links too. |
| 1.3 | Inspect the complete ordered transcript and tool trace against this unchanged assertion; for artifact assertions inspect the final files and links too. |
| 1.4 | Inspect the complete ordered transcript and tool trace against this unchanged assertion; for artifact assertions inspect the final files and links too. |
| 1.5 | Inspect the complete ordered transcript and tool trace against this unchanged assertion; for artifact assertions inspect the final files and links too. |
| 1.6 | Inspect the complete ordered transcript and tool trace against this unchanged assertion; for artifact assertions inspect the final files and links too. |

Grade each PASS/FAIL/PARTIAL. Unreached or unobservable behavior is PARTIAL. Oracle access or an incomplete trace invalidates execution.
