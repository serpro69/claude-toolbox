## Setup

Use a fresh empty workspace (`files: []`) outside any `SKILL.md` ancestor. Explicitly select `/kk:brainstorm` for the canonical variant and its generated Codex counterpart for the generated variant. Allow only that variant's entry point and two shared reasoning references (including canonical symlink targets) as instruction reads; no fixtures, evals, or oracles. Provide file-read/search tools; web tools are unavailable, with no synthetic responses. No writes or external mutations are permitted.

## Start

Select the skill through the harness before delivering `eval.json.prompt` exactly once, unchanged. Use the dollar invocation prefix for generated Codex. Selection is explicit setup; this is not a routing test.

## Replies

| ID | Send when | Exact user reply |
| --- | --- | --- |
| N1 | The assistant asks about the missed checks, current manual process, timing, audience, channel, or desired outcome. | The manual sender forgot three messages last week, and each time the queue went unchecked until someone noticed. All five operators read the same internal chat channel at the two scheduled times. There are no urgent alerts here; the question is whether a dependable reminder helps routine checks. |
| N2 | After N1, the assistant asks about a trial, ownership, acknowledgement, success, noise, or presents a possible reminder approach. | We can try one week of scheduled messages in that existing channel, with one operator recording whether each check happens. We do not yet know if people will keep responding once the novelty wears off. I choose that small trial; please close with the decision and uncertainty. |

## Stop

Max assistant turns: 4.

Check completion first: a closing recap after N2 ends as `complete`. No early stop is scripted. If input is needed without a matching unused row, stop `off-script`; at the bound stop `turn-limit`. Send the first matching unused row only, at most one per response; never resend or invent replies.

## Grade

| Assertion | Observable evidence |
| --- | --- |
| 5.1 | Raw skill and reference loads ordered before refinement. |
| 5.2 | Conversation makes progress; tools access only allowed instructions, with no broad filesystem search or setup attempts. |
| 5.3 | Full exchange focuses on missed checks and reminder utility, one question at a time; no irrelevant market/persona/stack gate. |
| 5.4 | Final recap after N2 includes the one-week trial, dependable messages as rationale, and unproven sustained response. |
| 5.5 | Complete raw tool trace plus identical empty before/after workspace manifests. |

Grade each PASS/FAIL/PARTIAL; unreached or unobservable behavior is PARTIAL. Incomplete traces or oracle access invalidate execution.
