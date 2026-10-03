## Setup

Stage the declared fixtures in a fresh workspace outside any `SKILL.md` ancestor. Expose only the competing descriptions and normal loading paths for `brainstorm`, `design`, `model`, and `implement`; do not preload bodies. Test canonical and generated instructions separately. Allow reads of workspace files and the selected variant's operative instruction closure, including shared files and profile detection/content, but no evals or oracles. Provide file-read/search and fixture-scoped editing tools. Web, knowledge-store, external services and independent-review tools are unavailable; provide no synthetic responses. Return each conversational question to the evaluator for the next scripted reply. Permit only the requested documentation within the workspace, keeping both fixtures read-only. Do not name a documentation home or exact output paths in the agent-visible access policy: that would supply a user-declared home and bypass the default-home confirmation this scenario exercises. After M1, the expected allowed writes are docs/architecture/{equipment-lending,equipment-lending-traps,index}.md. No active feature directory exists.

## Start

Send `eval.json.prompt` exactly once. For generated instructions only, mechanically replace an explicit `/kk:` invocation with `$kk:`; leave natural-language prompts unchanged. Do not preload skill bodies or disclose the expected route.

## Replies

| ID | Send when | Exact user reply |
| --- | --- | --- |
| M1 | The assistant asks to confirm docs/architecture/ as the kit home. | Use docs/architecture/ for the equipment-lending glossary, traps page, and conventions index. |
| M2 | The assistant asks the operations owner to decide whether multiple active loans are allowed. | I am not the operations owner and cannot settle that policy. Keep it undecided and route the question to that owner; finish the kit using the supplied evidence. |
| M3 | The assistant asks for runtime source or evidence of enforcement. | There is no runtime source in this workspace. Treat the snapshot as evidence of stored records only and keep enforcement unknown. |

## Stop

Max assistant turns: 6.

Check completion first: the two kit pages and index exist and the assistant surfaces the decision queue; terminate `complete`. No early stop is scripted. Otherwise, if input is needed and no unused row matches, stop `off-script`; at the bound stop `turn-limit`. Send at most one unused row per response, the first matching row; never resend or improvise replies.

## Grade

| Assertion | Observable evidence |
| --- | --- |
| 12.1 | The competing catalog and actual /kk:model loading call; no /kk:brainstorm load. |
| 12.2 | Home question and M1 reply occur before the first artifact write. |
| 12.3 | Both kit pages plus index exist and cite requirements.md and records.json; check grounded claims in their contents. |
| 12.4 | Kit and final queue distinguish the observed overlap from undecided policy, name the operations owner and keep enforcement unknown; trace shows no implementation. |

Grade each PASS/FAIL/PARTIAL. Unreached or unobservable behavior is PARTIAL. Oracle access or an incomplete trace invalidates execution.
