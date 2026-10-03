## Setup

Use a fresh empty workspace (`files: []`). Place the workspace outside the plugin and any `SKILL.md` ancestor. Explicitly select `/kk:brainstorm` for canonical instructions or its generated Codex counterpart. Allow only the selected entry point, both shared reasoning references (including canonical symlink targets), and the declared fixture paths as reads. Exclude evals, oracles, and future replies. Provide file-read/search tools; web and external service tools are unavailable, with no synthetic responses. No writes or external mutations are permitted.

Capture the instruction/fixture inventories and exact submitted setup before launch. Record provider/model/settings separately from instruction variant. The common evaluator guide's full tracing and grading contract applies.

## Start

Select the skill through the harness, then send `eval.json.prompt` exactly once, unchanged. Use the dollar invocation prefix in the generated variant's selection setup. This explicit-selection scenario does not certify implicit routing.

## Replies

| ID | Send when | Exact user reply |
| --- | --- | --- |
| C1 | The assistant first discusses cross-run or disk caching, freshness, reuse, cache invalidation, or whether to pursue the proposed cache. | Correction: these reports include confidential customer data. The approved rule is that no report data may persist after the process exits, including encrypted copies. Manual invocation and local-only processing remain settled. |
| C2 | After C1, the assistant revises the disk-cache direction, discusses nonpersistent alternatives, or asks about recomputation, reuse within a run, or acceptable delay. | Each invocation needs just one report, and 20 seconds is tolerable for now. I choose to drop cross-run caching and investigate where computation time goes before deciding on optimization. We do not know yet whether that investigation will find a useful improvement. Please recap. |

## Stop

Max assistant turns: 4.

Check completion first: a closing recap after C2 ends as `complete`. No early stop is scripted. If more input is needed but no unused row matches, stop `off-script`; at the bound stop `turn-limit`. Send at most one unused matching row per response, choosing the first matching row; never resend, improvise, or extend the bound. A premature recap before C2 with no applicable reply is `off-script`, not a passed completion.

## Grade

| Assertion | Observable evidence |
| --- | --- |
| 4.1 | Ordered entry-point and reference reads before cache analysis. |
| 4.2 | Initial response engages provisionally with proposed disk caching and the two already settled decisions. |
| 4.3 | First response after C1 retracts or rules out cross-run persistence under the no-retention rule; no encryption workaround. |
| 4.4 | Responses after C1 and final recap retain both unrelated decisions with no renewed choice request. |
| 4.5 | Final response after C2 records dropped cross-run cache, computation investigation, and unproven optimization benefit. |
| 4.6 | Complete raw tools and unchanged empty workspace inventories. |

Grade each assertion PASS/FAIL/PARTIAL; unreached or unobservable behavior is PARTIAL. Oracle access or incomplete tracing invalidates execution. Audit every read against the allowed manifest and count attempted prohibited mutations even if blocked.
