## Setup

Stage only `test-files/ops/release-queue.md` as `ops/release-queue.md`. Place the workspace outside the plugin and any `SKILL.md` ancestor. Explicitly select `$kk:brainstorm` for canonical instructions or its generated Codex counterpart. Allow only the selected entry point, both shared reasoning references (including canonical symlink targets), and the declared fixture paths as reads. Exclude evals, oracles, and future replies. Provide file-read/search tools; web and external service tools are unavailable, with no synthetic responses. No writes or external mutations are permitted.

Capture the instruction/fixture inventories and exact submitted setup before launch. Record provider/model/settings separately from instruction variant. The common evaluator guide's full tracing and grading contract applies.

## Start

Select the skill through the harness, then send `eval.json.prompt` exactly once, unchanged. Use the dollar invocation prefix in the generated variant's selection setup. This explicit-selection scenario does not certify implicit routing.

## Replies

| ID | Send when | Exact user reply |
| --- | --- | --- |
| F1 | After reading the fixture, the assistant asks about wait time, urgency, acceptable delay, parallelism, lock usage, or the next investigation, or recommends retaining the current limit. | A ten-minute queue wait is acceptable for us. I choose to keep the limit at one and measure how much of each deployment actually holds the migration lock before revisiting parallelism. Please close with that decision and its rationale. |

## Stop

Max assistant turns: 3.

Check completion first: a closing recap after F1 ends as `complete`. No early stop is scripted. If more input is needed but no unused row matches, stop `off-script`; at the bound stop `turn-limit`. Send at most one unused matching row per response, choosing the first matching row; never resend, improvise, or extend the bound. A premature recap before F1 with no applicable reply is `off-script`, not a passed completion.

## Grade

| Assertion | Observable evidence |
| --- | --- |
| 3.1 | Tool order: entry point, both references, then project read and analysis. |
| 3.2 | Read call/result for ops/release-queue.md and subsequent identification of both documented facts; no question asking the user for either fact. |
| 3.3 | Transcript distinguishes configuration/lock evidence from acceptable latency and chosen next action. |
| 3.4 | Final recap after F1 retains one deployment and measuring lock occupancy, with a reason grounded in the shared lock. |
| 3.5 | Complete trace and identical fixture hash in initial/final manifests. |

Grade each assertion PASS/FAIL/PARTIAL; unreached or unobservable behavior is PARTIAL. Oracle access or incomplete tracing invalidates execution. Audit every read against the allowed manifest and count attempted prohibited mutations even if blocked.
