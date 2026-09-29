# Design: documentation readers can understand

> Issue: [#156](https://github.com/serpro69/claude-toolbox/issues/156)
> Status: implementation — Tasks 1–2 complete; Tasks 3–5 pending
> Created: 2026-09-29
> Related: [Implementation plan](implementation.md), [tasks](tasks.md)
> Review reconciliation: [assessment](review-assessment.md)

## Problem and outcome

How might we help an author or reviewer understand a feature's purpose, behavior,
boundaries and open decisions without making them reconstruct that understanding
from implementation detail and verification history?

Shortening the prose alone does not solve this. A short explanation can still require
unexplained concepts, hide uncertainty or describe the implementation incorrectly.

**The editor must always understand the relevant requirements and implementation before
deciding how to explain them.**

Two readers need different entry points:

| Reader                  | Job                                                 | Available material                                                   |
| ----------------------- | --------------------------------------------------- | -------------------------------------------------------------------- |
| Feature author          | Understand and resume their own work                | Private design, implementation and task documents plus source        |
| Contributor or reviewer | Understand an increment and assess its consequences | PR description, repository docs, diff and other team-visible sources |

A reader should be able to answer: why does this change exist; what happens in a
representative case; what changes now; what remains outside the increment; and
what still needs a decision? Technical reference detail remains available after
that orientation. No word-count reduction target defines success.

## Decisions and provenance

Sergio accepted the comprehension-focused scope and selected the combined approach
on 2026-09-29: a standalone editorial skill plus integration into existing writing
workflows. He explicitly clarified that identifying claims includes understanding
the requirements and implementation behind them. Independent CoVe verification of
the approach was offered; he selected proceeding with inspected repository evidence.

The new entry point is `/kk:clarify-docs`. One shared procedure supplies its behavior
and the final editing passes in `/kk:design` and `/kk:document`. Editing happens
after drafting. It does not impose brevity on coding, investigation or reasoning.

The current `/kk:design` instructions emphasize comprehensive implementation
guidance; `/kk:document` covers documentation discovery and domain rubrics. Neither
provides this evidence-grounded editorial pass. `/kk:implement` invokes
`/kk:document` at **plan-mode completion only**. Standalone implementation has no
prescribed documentation completion step. The plugin has no PR-writing workflow to extend.

## Reader experience

Given a dense configuration document, the editor might lead with a restaurant
default and an item exception, explain what happens when the default changes, then
introduce storage fields and error responses. It must verify that example against
the accepted rules and implemented behavior before presenting it as fact.

For a contract-only PR, the explanation identifies what consumers can agree on now
and which runtime behavior is still future work. For a private implementation plan,
it makes the current task and unresolved decisions easy to find while retaining
the detail needed to implement safely.

The default result is an edited existing artifact, not another summary document.
Already-clear material can remain unchanged. A PR body obtained from a remote
source is edited as a local draft; reading a PR never authorizes updating it.

## Editorial workflow

1. **Load instructions and resolve scope.** Load the skill and shared procedure
   before reading targets. Establish the selected artifact, reader, purpose and
   destination from the request and repository instructions. Reuse known answers;
   ask only when missing information materially changes the edit. A directory is a
   discovery scope, not permission to rewrite every file inside it.
2. **Understand the underlying work.** Read the complete selected artifact and
   follow the relevant requirements, decisions, implementation and tests. For a PR,
   establish its actual base/head and review increment. For a proposed feature,
   distinguish accepted requirements and planned behavior from code that exists.
   Inspect enough context to explain the relevant behavior, boundaries and rationale;
   do not recursively audit the entire feature or treat tests as proof of intent.
3. **Establish what the explanation must preserve.** Keep a working inventory of
   requirements, observable behavior, constraints, decisions, uncertainty and evidence.
   Trace important claims to their sources. This inventory guides the edit; it does
   not create a new mandatory report or duplicate source of truth.
4. **Edit for the reader.** Lead with purpose and current behavior. Introduce a
   concrete scenario where it helps, explain unfamiliar terms at first use, remove
   duplication, and place reference detail after orientation. Preserve document-type
   requirements and the project's existing organization. Do not force every document
   into one template or add examples that the evidence cannot support.
5. **Verify the result.** Compare the revised artifact with its requirements,
   implementation evidence and original meaning. Check the reader questions above,
   protected details, links and required structure. Correct editorial regressions;
   surface source disagreements. Report changed paths and material unresolved gaps.

An existing session may supply source understanding when its revision and scope are
still applicable. The editor verifies applicability and reads gaps; it need not repeat
all investigation. Reading implementation is allowed. Changing implementation or
running deployment, migration or production-write operations is outside this skill.

## Truth, preservation and visibility

Preserve technical meaning rather than blindly preserving every original sentence.
Requirements establish intended behavior; code establishes implemented behavior.
Neither automatically overrides the other. A factual documentation error may be
corrected when the evidence is conclusive. A requirements/implementation mismatch
must remain explicit; the editor cannot silently ratify the implementation, invent
a product decision or erase a requirement to make the document consistent.

Preserve mandatory versus optional language, conditions, exceptions, thresholds,
identifiers, interface shapes, ownership, decision provenance, deployment gates,
completion status and verification limits. Reorganization must retain working
anchors or update affected in-scope links; changes needing wider edits are surfaced.
Keep executable examples intact unless an authorized, verified correction is needed.

When evidence is missing, inspect accessible references first. If a consequential
gap remains, ask a focused question or retain an explicit limitation. Do not replace
uncertainty with smooth prose. Record unresolved issues in the affected artifact or
its already-selected task document, with a concrete next step and known owner.

Private context can support understanding without becoming shareable. Apply these
visibility rules in order, to both facts and references:

1. Explicit user and repository instructions establish the audience and any restricted
   material. A restriction overrides the fact that a file is tracked or reachable.
2. Otherwise, a file tracked at the target repository's PR head is an accessible
   reference for that repository's established review audience. This does not authorize
   quoting it to a wider audience. Private aggregator files and untracked local drafts
   do not qualify merely because they are next to the target checkout.
3. An external reference needs evidence of audience access: it is public, or the user
   or repository instructions identify it as shared with that audience. Access through
   the editor's own credentials is insufficient. Unknown visibility stays unknown.
4. Use an accessible source or an explicitly authorized standalone explanation. If
   neither is available, retain the limitation or ask for the missing authorization;
   do not disclose the private fact merely by deleting its citation.

A task number is not inherently private. Retain it when its referenced task is
available to the intended audience; exclude private task IDs and absolute workspace
paths. Fixtures must declare the destination, access facts and restrictions so this
decision is reproducible, including tracked-but-restricted and shared-task cases.

## Integration boundaries

| Entry point                     | When and where the pass runs                                                                   | Downstream review                                                                                 |
| ------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `/kk:clarify-docs`              | Explicit request; selected human documentation or PR draft                                     | In-session fidelity check; caller's normal document/PR review, with no automatic independent gate |
| `/kk:design`                    | After drafting all three artifacts, or changed documents on resume                             | Existing recommendation to run `/kk:review-design`; this is not automatic execution               |
| `/kk:document`                  | After updating the invocation's selected outputs                                               | In-session fidelity check; any project-prescribed review remains the caller's responsibility      |
| `/kk:implement` plan mode       | Through its existing completion call to `/kk:document`                                         | Inherits the documentation pass and its review limits; no extra pass                              |
| `/kk:implement` standalone mode | No automatic pass added in v1; explicit `/kk:document` or `/kk:clarify-docs` remains available | No new completion or review guarantee                                                             |

All consumers load the shared procedure during instruction loading and apply it
after drafting. They reuse it directly; the procedure never calls its consumers.
It adds no profile and performs no domain-profile detection itself. Existing skills
continue to own their profile rubrics, which the editor must preserve.

The shared procedure is loaded on every invocation of either writing consumer,
including a resume that produces no edit. Target at most 1,000 whitespace-delimited
words, with a v1 ceiling of 1,200 across the procedure and any mandatory linked
instructions it adds. Record this count during implementation. This is an instruction
cost budget, not a compression target for user documents. Do not evade it with linked
files or late loading; reduce duplication or revise the design if the ceiling cannot
be met without losing rules.

The in-session comparison is a useful check, not independent fidelity evidence.
Independent evaluators test the skill before release. An optional isolated runtime
verification variant is [deferred](implementation.md#deferred-work); v1 does not
claim the code-review workflow's isolation guarantees for editorial self-checks.

PR authoring remains a standalone use case in v1. No publishing, PR creation, hooks
or repository-wide automatic rewrite is introduced. Code, config, agent instructions
and `SKILL.md` are not editorial targets in v1. On an explicit instruction-editing
request, explain the scope boundary and suggest `/kk:implement`; do not invoke it or
edit automatically. That workflow performs its own profile detection (`skill-md`
when the target matches its signals). Ordinary code or brevity requests do not
activate `/kk:clarify-docs`.

## Verification and acceptance

Behavioral evals use synthetic, self-contained fixtures with requirements and source
when needed. Private customer artifacts are motivation only and are not copied into
this public repository. Expected claims and answers live in grader-only `oracle/`
directories outside `test-files/`.

Each applicable case checks two independent outcomes:

- **Comprehension:** a fresh reader given only the artifact and its intended reading
  path can correctly answer all five reader questions. For a dense fixture, the
  rubric names the specific confusion the edit must resolve. Compare original and
  revised artifacts in separate fresh reader sessions. Passing all five questions
  does not establish that the artifact is correct, shareable or well structured.
  Permit repairs to any predeclared correctness, fidelity, visibility, structure or
  orientation defect while preserving answer accuracy. Expect no editorial change
  only when the baseline meets all applicable requirements. Do not claim improvement
  from word count alone.
- **Fidelity:** no protected requirement or qualification is lost, no unsupported
  claim is introduced, and source disagreements remain visible. Fluent prose cannot
  compensate for failure here.

Cases cover implementation-dependent meaning, document/source disagreement, missing
context, dense private plans, PR increments, private-reference exclusion, cross-file
requirements, already-clear text, non-trigger requests and automatic final-pass ordering.
Include clear prose whose five answers pass but which contains a prohibited reference
or a factual error outside those answers; necessary repairs must still be accepted.
Use separate general-purpose reader sessions with no inherited conversation, and a
separate grader with the oracle. The existing `eval-grader` role cannot be the reader:
it is prohibited from opening fixtures. The [implementation protocol](implementation.md#fresh-reader-protocol)
defines isolation, inputs and verdicts. Record runs in `verification.md` and supporting
files under `verification/` in this feature directory; these are created when runs begin.
There is no built-in eval runner. Structural tests cannot substitute for these evals.

## Assumptions

- Relevant requirements and implementation are usually accessible locally or through
  existing tools. Missing access must produce a visible limitation, not invented context.
- Reader and destination can usually be inferred from the requested artifact and
  repository instructions. Evals must exercise ambiguity rather than assuming this always works.
- A shared editorial procedure can improve comprehension without semantic loss.
  Source-grounding and preservation evals are the decisive test of that assumption.
- Explicit invocation is sufficient for PR editing in v1. If adoption remains poor,
  consider a PR-authoring integration after an actual owning workflow exists.

## Not Doing

- Global response shortening or changes to model reasoning: the target is a drafted artifact.
- Product decisions, code refactoring or a complete behavioral audit: understand the
  relevant work, expose disagreements, and leave their resolution to the owning workflow.
- Automatic publication or edits to external PRs: draft editing grants no publishing authority.
- Automatic standalone-implementation coverage: it would require a new completion
  path beyond the agreed integration into existing writing workflows.
- Bulk cleanup, archived-history rewrites or new mandatory summary files: keep the edit bounded.
- A new profile, runtime service, dependency or universal readability score: existing
  skill composition and concrete comprehension checks are sufficient for v1.

## Rejected alternatives

| Alternative                             | Why it was not selected                                                            |
| --------------------------------------- | ---------------------------------------------------------------------------------- |
| Standalone skill only                   | Covers existing artifacts but relies entirely on authors remembering to invoke it. |
| Existing workflows only                 | Improves their outputs but misses PR drafts and other ad hoc editing.              |
| Generic compaction or word-count target | Can remove necessary context while leaving the explanation hard to understand.     |
| Markdown-detected profile               | File format does not establish an editorial request, reader or destination.        |

The main risks are unnecessary source exploration, semantic drift during rewriting,
and edit churn. Bounded evidence gathering, separate fidelity checks and unchanged
output for already-clear text address those risks and are explicit eval targets.
