# Design: clarify issue descriptions

> Issue: [#157](https://github.com/serpro69/claude-toolbox/issues/157)
> Status: done; all acceptance criteria verified (2026-10-02)
> Created: 2026-09-30
> Related: [Implementation](implementation.md), [tasks](tasks.md), [executed verification](verification.md)
> Repository baseline: `3e430b4`

## Problem and outcome

Help issue authors make bug reports and proposed work understandable and grounded
in evidence while preserving uncertainty and producing a local draft. The primary
readers are maintainers and contributors deciding what an issue means and what
work is needed. A caller can establish a more specific audience.

Success means a fresh reader can identify the problem, current and desired
behavior, scope, existing acceptance criteria, and unresolved questions where
applicable. All applicable preservation, destination, disclosure, and regression
assertions must pass. A shorter description is not itself a successful result.

This is a separate extension of `/kk:clarify-docs`, not a rewrite of the
[completed feature](../../done/clarify-docs/design.md). The accepted
[optional-clarification decision](../../../adr/0009-optional-document-clarification.md)
remains in force: writing workflows may suggest clarification but do not run it
automatically.

## Behavior at the design baseline

The [entry point](../../../../klaude-plugin/skills/clarify-docs/SKILL.md) explicitly
accepts documentation and PR drafts, including PR URLs and pasted bodies. It
loads the complete [shared procedure](../../../../klaude-plugin/skills/_shared/document-clarity.md)
through its existing per-skill symlink before reading targets and sources.

The procedure already distinguishes accepted requirements, proposals, current
implementation, and future work. It supports planned contracts without inventing
runtime evidence. Its PR paragraphs separately require actual base/head revisions
and review increments. Those requirements must remain specific to PR editing.

The current audience rules include a presumption for files tracked at a PR head
and accessible to that repository's established review audience. That presumption
does not establish access for an issue's readers. Issue-specific input routing,
reader guidance, and behavioral scenarios are currently absent.

## Decision and verification provenance

Sergio confirmed the problem, audience, success criteria, and issue constraints,
requested comparison of both approaches, requested isolated
`/kk:chain-of-verification`, selected approach A, and accepted the behavior
walkthrough: extend the existing shared procedure. The `skill-md` profile was
confirmed; the installed profile has no `design/` content and contributes no
additional design sections.

Four general-purpose verifiers completed separate factual questions without
inheriting the conversation. This was repository inspection, not a behavioral
eval or an implementation review. They shared the workspace.

| Question / verifier | Finding | Consequence |
| --- | --- | --- |
| Evidence and routing / `cove_evidence_routing` | Planned work already fits the evidence model; issues lack an explicit input route. | Reuse the evidence model and add issue-specific routing and preservation guidance. |
| Audience and destinations / `cove_audience_destination` | Output safeguards are reusable; PR-reviewer access does not establish issue-reader access. | Keep the existing safeguards and explicitly scope the PR access presumption. |
| Instruction structure / `cove_instruction_structure` | Only the standalone skill currently loads the procedure. A separate guide adds a dependency and conditional loading. | Keep the existing instruction dependency structure. |
| Eval coverage / `cove_eval_coverage` | Fifteen current scenarios cover documents and PRs, with no GitHub-bug or Linear-feature issue cases. | Add and execute issue scenarios and rerun existing coverage. |

The verification corrected two overstatements in the initial comparison: equivalent
outputs between approaches have not been demonstrated, and fitting the additions
within the instruction budget remains unproven. File and word counts do not
establish maintenance effort, token cost, latency, or reliability. These limits
remain explicit assumptions below; no live tracker integration was verified.

### Review findings disposition

The subsequent external review's findings were checked against all three artifacts
and the operative shared procedure before changes were made:

| Finding | Verdict and evidence | Resolution |
| --- | --- | --- |
| P1: budget check cannot catch overflow | Partly valid. The implementation plan already required counting the complete cumulative procedure, so overflow would be detected. Late discovery across serial slices could nevertheless force rework. The existing design-reopen instruction was a stop condition, not a predetermined fallback. | Draft and check the complete candidate before operative Task 1 changes. Sergio selected retaining A and raising the ceiling with a recorded justification if necessary; the budget policy below defines that fallback. |
| P2: no same-repository audience default | Valid. The original rules required public availability or explicit sharing confirmation and provided no default for private same-repository issues. | Add the bounded GitHub default, with restriction and audience overrides; exercise it in scenario 16 and its limits in scenario 19. |
| P3: title-editing scope unclear | Valid. The title was named as input context without an explicit output boundary. | Titles remain read-only for description edits; scenarios 16 and 18 protect them. |

## Request and output contract

Extend the existing entry point to accept a selected local issue-description draft,
a pasted description, or an issue URL. GitHub and Linear are examples of supported
sources when suitable read-only tools or supplied text are available, not required
integrations or a closed provider list. No new SDK, service, or adapter is added.

Route by the requested action. Requests to clarify an issue description select
editorial work. Ordinary requests to implement, fix, or work on the described issue
belong to `/kk:implement` and must not activate description editing. A URL alone
does not establish editorial intent. Clarify consequential ambiguity rather than
silently selecting a different task. Existing code, config, agent-instruction,
skill-instruction, and generic-brevity boundaries remain intact.

| Input | Authorized output |
| --- | --- |
| Explicitly selected local issue draft | Edit that draft in place. |
| Pasted description or remote body, with destination | Save one revised local draft at the selected destination, subject to collision rules. |
| Pasted description or remote body, with established feature scope | Name one unused draft within that scope. |
| Pasted description or remote body, with neither | Ask for a destination or feature scope before writing. |

An issue's tracker title and type are read-only context for description edits.
Do not propose a replacement title; if a local draft carries the supplied title,
preserve its wording. Headings within the description remain editable. Editing a
tracker title requires a separately scoped request and is outside this follow-up.

An immutable fixture or capture of a pasted/remote body is input, not automatically
the selected local draft. Never overwrite an unrelated file. If a proposed path
collides, choose an unused name within a clearly established feature scope or ask
for a destination. Reading an issue permits no issue update, comment, or message.

## Editorial behavior

Keep the existing instruction order and four-stage procedure. Load the entry point
and shared procedure fully before target/source content. Early selection uses
request keywords and filenames only; issue retrieval occurs in the source-reading
stage, not as a preflight before instruction loading.

1. **Understand the issue.** Read the full selected description and relevant supplied
   context: its title/type when available, requirements, decisions, referenced
   discussions, and source or tests behind particular claims. Follow references far
   enough to explain the work without auditing the entire tracker or feature.
   Comments can supply evidence or decision provenance; they are not editing targets
   and are not automatically accepted requirements.
2. **Protect meaning.** Preserve identifiers, conditions, constraints, scope,
   ownership, decisions, task state, and uncertainty. Keep reported observations
   distinct from verified behavior and suspected causes distinct from established
   causes. Requirements establish intent; source establishes behavior at the
   inspected revision. An issue report and current source may describe different
   versions; retain that distinction or the unresolved disagreement.
3. **Edit for the reader.** Explain the problem and relevant current/desired behavior
   before incidental technical detail. Preserve useful bug-report reproduction
   steps, environment/version details, expected and observed results, and frequency
   or conditions when supplied. Feature requests explain the need, proposed or
   accepted outcome, scope, existing acceptance criteria, and open decisions.
   Other issue types follow their own purpose and existing organization. Do not
   impose mandatory empty headings or turn these topics into a universal template.
4. **Verify separately.** Compare comprehension and fidelity independently against
   the original and inspected evidence. Check reproduction details, qualifications,
   acceptance criteria, links, checkboxes, decision status, and disclosure. Report
   the local path and material unresolved gaps briefly; create no extra summary or
   claim-ledger artifact.

Restating an existing acceptance criterion more clearly is allowed; adding a new
threshold, scope commitment, solution decision, or acceptance criterion is not.
Missing criteria or decisions remain unknown, with a concrete next step and a known
owner or an explicit unknown owner when relevant. Do not claim reproduction or
passing tests without evidence. Reading examples or source commands does not
authorize executing them or implementing the issue.

A proposed feature does not require an existing implementation or a PR diff.
Relevant source can explain current behavior; absence of future implementation is
normal. A linked PR can be supporting evidence where relevant but does not convert
the issue-description edit into a PR-description workflow. Existing PR editing
continues to require its actual review context.

## Audience and incomplete context

Apply the existing restrictions to facts as well as citations. Establish the
intended audience for the resulting issue description even when saving it locally.
For a GitHub issue identified as belonging to repository R, default to R's issue
audience when the caller specifies no different audience. Files tracked in R at
the relevant inspected revision are presumed accessible to that audience, including
in a private repository. Use R's default branch when no source revision is otherwise
established; that choice does not prove behavior in an older reported version.
Neither an audience question nor a disclosure limitation is needed solely because
this same-repository case is private.

This is a bounded design default, supported by GitHub's
[repository permissions](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization).
Explicit restrictions override it, including restrictions on tracked files. It
does not cover untracked drafts, private aggregators, another repository, or a
different intended audience. Do not infer GitHub repository access from a Linear
issue or another tracker's link to that repository. For those cases, public
availability or user/repository confirmation must establish sharing; editor
credentials or common organizational membership are insufficient. Keep the
PR-head presumption restricted to its existing review context.

Retain legitimate audience-accessible task references. Exclude restricted facts,
private source pointers, and absolute workspace paths from drafts and shared gap
notes. Deleting a citation never permits paraphrasing its restricted fact. Use an
accessible source or an explicitly authorized standalone explanation; otherwise
retain a non-disclosing limitation. The caller-only local-output link exception
remains limited to the selected output.

| Gap | Required behavior |
| --- | --- |
| Issue body cannot be retrieved | Explain the access limitation and request the text or an accessible source; do not invent a description or write a purported revision. |
| Body exists; supporting source is unavailable | Continue supported edits at an established destination, retaining reported/proposed status and verification limits. |
| Requirements and source disagree | Preserve both, their provenance, and the next action needed; do not silently ratify one. |
| Destination is unresolved | Inspect available context and ask before writing. |
| Audience access remains unknown after applying the bounded same-repository default and any explicit restrictions | Do not disclose the unsupported private fact; ask or retain a non-disclosing limitation. |

## Instruction size and compatibility

Use concise issue paragraphs within `_shared/document-clarity.md` and update the
existing entry point. Add no issue-only guide, new skill, new shared symlink,
profile, or automatic consumer invocation. Preserve the PR paragraphs and common
rules while removing duplication only where meaning remains intact.

At the inspected baseline the shared procedure contains 1,000 whitespace-delimited
words. Use 1,200 words as the initial ceiling for the complete procedure and any
mandatory dependencies, with this explicit fallback:

1. Before operative Task 1 edits or candidate behavioral grading, draft the complete
   replacement procedure and entry point covering Tasks 1–3, including all issue
   types, gaps, audience rules, title scope, and existing safeguards. Remove
   duplication and check requirement coverage. Count the whole procedure plus
   mandatory dependencies, not just added paragraphs or the first slice. Measure
   the entry point separately; its trigger/input rules are not all procedure text.
2. If the full candidate is at most 1,200 words, retain that ceiling. If it exceeds
   1,200 after deduplication and a preservation check, keep A and set this
   follow-up's ceiling to the full candidate's measured count. Before proceeding,
   record the exact count, increase over 1,200, duplication removed, and why the
   remaining additional guidance is necessary. This fallback was explicitly
   selected by Sergio; it does not authorize dropping safeguards or adopting B.
3. Record the ceiling and complete candidate revision in the implementation
   evidence. Every slice checks both the operative cumulative procedure and the
   candidate representing all remaining planned rules against that same ceiling.
   If later wording needs more room, repeat the complete-candidate preflight and
   record the revised ceiling and rationale before applying it; rerun affected
   behavioral checks after the change. No slice receives a fresh 200-word allowance.

Do not meet the budget by hiding instructions in another mandatory file, weakening
protected meaning, or loading necessary instructions after source reads. Budget
increases cover only the agreed issue scope. They do not authorize extra features.

Recheck current provider description guidance when editing the skill description,
as required by repository conventions. Canonical changes live in `klaude-plugin/`;
regenerate Codex output. Maintained usage documentation must describe issue inputs,
local output, uncertainty, and the implementation-request boundary consistently.

## Acceptance and evaluation

Use the existing manual editor/reader/grader protocol with synthetic read-only
platform responses. The [implementation matrix](implementation.md#evaluation-matrix)
specifies nine new scenarios. They cover GitHub bug reports, Linear proposals,
local and pasted inputs, collisions, missing context, restricted audiences, and
both implement/fix non-triggers. Rerun all fifteen existing document/PR scenarios
and the current optional-consumer scenarios.

For edited outputs, fresh original and revised readers receive only their respective
artifact and declared accessible reading path. Grade against fixed, applicable
questions and protected claims in a separate oracle. Preserve correct unknowns;
do not require every issue type to answer irrelevant questions. Unchanged or
blocked-output scenarios are judged by their observable routing and file effects.

Every applicable assertion must pass with evidence. Missing evidence and PARTIAL
are not passes. Structural tests, authored scenarios, and this design verification
do not establish executed editorial behavior. Synthetic tracker responses verify
the editorial contract, not live connector compatibility or universal human
comprehension. No new eval runner is included.

## Assumptions

- **Compact guidance:** complete issue rules may fit within the initial 1,200-word
  ceiling. Validate the full candidate before operative changes; otherwise retain
  A and use the measured, justified ceiling under the budget policy above.
- **Available evidence:** existing read-only tools or caller-supplied descriptions
  can supply enough context for useful edits. Validate positive and missing-access
  paths with synthetic responses; no particular tracker tool is assumed present.
- **Compatibility:** additive issue guidance can preserve document/PR routing,
  fidelity, visibility, and output behavior. Validate by executing existing evals.
- **Audience resolution:** the GitHub same-repository default and explicit sharing
  declarations can resolve access without relying on editor credentials. Validate
  an undeclared private same-repository audience, restriction overrides, and a
  declared different audience.

## Not Doing

- Remote publication, issue updates, comments, or messages: editing authorizes local output only.
- Implementing, fixing, or reproducing the described work: those are separate execution tasks.
- New product decisions or acceptance criteria: clarification preserves meaning and uncertainty.
- Tracker-title editing: titles are context for the selected description, not another output.
- Mandatory tracker integrations or live connector certification: use available read-only capabilities and supplied text.
- A separate issue guide, new skill/profile, or automatic clarification: reuse the chosen workflow and preserve ADR 0009.
- Bulk rewrites, new summary artifacts, or edits to completed designs: keep targets bounded and history frozen.

## Rejected Alternatives

| Alternative | User value | Feasibility and trade-off | Reason not selected |
| --- | --- | --- | --- |
| B: conditionally loaded issue guide | Intended reader outcome is the same; equivalence is untested. | Reduces non-issue instruction text but adds routing, a dependency, and loading-order coverage. | Retain A, including on budget overflow: the selected fallback is a measured, justified ceiling increase, not a separate guide. |

No reliability, latency, or maintenance-time advantage has been measured for either
approach. A is selected for its simpler instruction structure, subject to the
explicit budget and behavioral checks above.
