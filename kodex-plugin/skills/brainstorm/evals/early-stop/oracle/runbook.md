## Setup

Use a fresh empty workspace (`files: []`) outside any `SKILL.md` ancestor. Explicitly select `$kk:brainstorm` in the canonical variant or its generated Codex counterpart. Allow read-only access to the selected entry point and two shared references, including canonical symlink targets; exclude evals and oracles. Provide file-read/search tools. Web tools are unavailable; no synthetic responses. No writes or external mutations are permitted. No project files can answer repeat-execution safety in this scenario.

## Start

Select the skill through the harness, then send `eval.json.prompt` exactly once, unchanged. Use the dollar invocation prefix for generated Codex. This explicit selection is not implicit-routing evidence.

## Replies

| ID | Send when | Exact user reply |
| --- | --- | --- |
| E1 | The assistant's first substantive response discusses retry safety, duplicate execution, side effects, or asks about the failed jobs. | Stop here for now. We still do not know which jobs are safe to repeat, and I have made no rollout decision. Please just recap what is settled and what remains open. |

## Stop

Max assistant turns: 2.

Check completion first: the response to E1 ends the run as `early-stop`; grade that response even if it improperly asks another question. If the initial response requires input but no row matches, stop `off-script`. At the bound without the expected stop, record `turn-limit`. Send E1 at most once; do not continue interrogation or provide any invented answer.

## Grade

| Assertion | Observable evidence |
| --- | --- |
| 7.1 | Ordered entry-point/reference loads and first substantive discussion of unknown repeat safety. |
| 7.2 | Exact delivery of E1 and subsequent response: partial recap, no further question. |
| 7.3 | Recap separates reduced operator work as the goal from unknown side effects/repeat safety and absent rollout approval. |
| 7.4 | Complete tool trace and unchanged before/after workspace state, including attempted prohibited actions. |

Grade PASS/FAIL/PARTIAL per assertion. Behavior not reached or observable is PARTIAL; oracle access or incomplete tracing invalidates the run.
