## Setup

Stage the declared fixtures in a fresh workspace outside any `SKILL.md` ancestor. Expose only the competing descriptions and normal loading paths for `brainstorm`, `design`, `model`, and `implement`; do not preload bodies. Test canonical and generated instructions separately. Allow reads of workspace files and the selected variant's operative instruction closure, including shared files and profile detection/content, but no evals or oracles. Provide file-read/search and fixture-scoped editing tools. Web, knowledge-store, external services and independent-review tools are unavailable; provide no synthetic responses. Return each conversational question to the evaluator for the next scripted reply. The workspace starts empty. No writes are permitted.

## Start

Send `eval.json.prompt` exactly once. For generated instructions only, mechanically replace an explicit `/kk:` invocation with `$kk:`; leave natural-language prompts unchanged. Do not preload skill bodies or disclose the expected route.

## Replies

| ID | Send when | Exact user reply |
| --- | --- | --- |

## Stop

Max assistant turns: 1.

Check completion first: the assistant completes the requested response or file edit; terminate `complete`. No early stop is scripted. Otherwise, if input is needed and no unused row matches, stop `off-script`; at the bound stop `turn-limit`. Send at most one unused row per response, the first matching row; never resend or improvise replies.

## Grade

| Assertion | Observable evidence |
| --- | --- |
| 10.1 | Observed skill-loading calls and complete transcript. |
| 10.2 | Full conversation and final workspace contents; check the assertion directly, including the timing of confirmations relative to writes. |

Grade each PASS/FAIL/PARTIAL. Unreached or unobservable behavior is PARTIAL. Oracle access or an incomplete trace invalidates execution.
