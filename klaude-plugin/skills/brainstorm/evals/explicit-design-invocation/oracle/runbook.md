## Setup

Stage the declared fixtures in a fresh workspace outside any `SKILL.md` ancestor. Expose only the competing descriptions and normal loading paths for `brainstorm`, `design`, `model`, and `implement`; do not preload bodies. Test canonical and generated instructions separately. Allow reads of workspace files and the selected variant's operative instruction closure, including shared files and profile detection/content, but no evals or oracles. Provide file-read/search and fixture-scoped editing tools. Web, knowledge-store, external services and independent-review tools are unavailable; provide no synthetic responses. Return each conversational question to the evaluator for the next scripted reply. Only docs/feat/wip/archive-command/{design,implementation,tasks}.md may be written; README.md is read-only. No language profile is implied by this prose-only fixture.

## Start

Send `eval.json.prompt` exactly once. For generated instructions only, mechanically replace an explicit `/kk:` invocation with `$kk:`; leave natural-language prompts unchanged. Do not preload skill bodies or disclose the expected route.

## Replies

| ID | Send when | Exact user reply |
| --- | --- | --- |
| A1 | The assistant asks to confirm or correct an HMW/problem framing. | Yes, that framing captures the problem: help the collection owner retire a note while preserving access to it. |
| A2 | The assistant asks who the user or persona is, or asks to confirm that persona. | The user is the owner of a small local note collection, using the tool directly. |
| A3 | The assistant asks about success or measurable acceptance. | Success means selecting one existing ID marks exactly that item archived, keeps it visible with working links, and repeating the action changes nothing further; a missing ID changes nothing. |
| A4 | The assistant asks about constraints, existing behavior, or scope. | Keep the existing item data and ordinary listing behavior described in README.md. Work offline, add no dependencies, and exclude deletion, hiding, bulk operations, restore, and synchronization. |
| A5 | The assistant asks to confirm simple versus non-trivial classification or the breadth of alternatives. | A simple direct path plus one alternative is enough; proceed with that scope. |
| A6 | The assistant presents alternatives and asks which to carry forward or choose. | Choose the direct archive-flag update. Reject hiding or moving notes because existing visibility and links must stay intact. |
| A7 | The assistant offers optional factual verification of alternatives. | Proceed with the analysis as-is; keep unverified assumptions explicit. |
| A8 | The assistant asks to confirm assumptions, exclusions, rejected alternatives, or the recommended direction. | Yes. Keep the direct flag update, the exclusions already stated, and the assumption that IDs are unique pending a check before implementation. |
| A9 | The assistant presents a design section and asks whether it looks right, or asks permission to draft. | That section looks right. I approve the design presentation as a whole; write the design document, implementation plan, and task list under docs/feat/wip/archive-command/. Do not implement or run a follow-up review. |
| A10 | The assistant asks for the documentation destination before presenting a design section. | Use docs/feat/wip/archive-command/ for the three planning documents. Keep following the design confirmations before drafting. |

## Stop

Max assistant turns: 16.

Check completion first: all three planning artifacts exist and the assistant presents their completion; terminate `complete`. No early stop is scripted. Otherwise, if input is needed and no unused row matches, stop `off-script`; at the bound stop `turn-limit`. Send at most one unused row per response, the first matching row; never resend or improvise replies.

## Grade

| Assertion | Observable evidence |
| --- | --- |
| 11.1 | Exact explicit invocation and actual /kk:design load; no /kk:brainstorm load. |
| 11.2 | Full exchange shows foundation and classification confirmations before alternatives, direction choice and design approval before writes. |
| 11.3 | Three output files exist; final response recommends review; tools perform no runtime implementation. |

Grade each PASS/FAIL/PARTIAL. Unreached or unobservable behavior is PARTIAL. Oracle access or an incomplete trace invalidates execution.
