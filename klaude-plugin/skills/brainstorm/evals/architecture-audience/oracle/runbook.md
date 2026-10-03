## Setup

Use a fresh empty workspace (`files: []`). Place the workspace outside the plugin and any `SKILL.md` ancestor. Explicitly select `/kk:brainstorm` for canonical instructions or its generated Codex counterpart. Allow only the selected entry point, both shared reasoning references (including canonical symlink targets), and the declared fixture paths as reads. Exclude evals, oracles, and future replies. Provide file-read/search tools; web and external service tools are unavailable, with no synthetic responses. No writes or external mutations are permitted.

Capture the instruction/fixture inventories and exact submitted setup before launch. Record provider/model/settings separately from instruction variant. The common evaluator guide's full tracing and grading contract applies.

## Start

Select the skill through the harness, then send `eval.json.prompt` exactly once, unchanged. Use the dollar invocation prefix in the generated variant's selection setup. This explicit-selection scenario does not certify implicit routing.

## Replies

| ID | Send when | Exact user reply |
| --- | --- | --- |
| A1 | The assistant asks about downtime, recovery, replication, data loss, failure handling, consistency, or operator capacity, or compares the two approaches. | Readers can tolerate the 30-minute recovery window. We can republish the last daily batch if needed. Our two operators have never run a regional failover exercise; minimizing operational burden matters more than uninterrupted writes. |
| A2 | After A1, the assistant asks about a recovery exercise, standby, next investigation, or operational risk, or recommends investigating standby. | I choose to investigate standby first with a timed recovery exercise. We have not measured whether it meets 30 minutes. That is enough for my next decision; please recap. |

## Stop

Max assistant turns: 4.

Check completion first: a closing recap after A2 ends as `complete`. No early stop is scripted. If more input is needed but no unused row matches, stop `off-script`; at the bound stop `turn-limit`. Send at most one unused matching row per response, choosing the first matching row; never resend, improvise, or extend the bound. A premature recap before A2 with no applicable reply is `off-script`, not a passed completion.

## Grade

| Assertion | Observable evidence |
| --- | --- |
| 2.1 | Ordered skill/reference reads before the first architecture analysis. |
| 2.2 | Responses compare failure/recovery and coordination or operational burden using the given facts; no invented measurements. |
| 2.3 | Every substantive turn and its questions; no irrelevant persona/market/spec gates. |
| 2.4 | Final response after A2 distinguishes the candidate, exercise, rationale, and unknown measured recovery time. |
| 2.5 | Full raw tool trace plus identical before/after workspace inventories. |

Grade each assertion PASS/FAIL/PARTIAL; unreached or unobservable behavior is PARTIAL. Oracle access or incomplete tracing invalidates execution. Audit every read against the allowed manifest and count attempted prohibited mutations even if blocked.
