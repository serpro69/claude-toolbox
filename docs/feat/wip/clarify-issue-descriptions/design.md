# Design: clarify issue descriptions

> Issue: [#157](https://github.com/serpro69/claude-toolbox/issues/157)
> Status: pending design review; approach A and behavior walkthrough accepted
> Created: 2026-09-30
> Related: [Implementation](implementation.md), [tasks](tasks.md)
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

## Current behavior

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
Explicit restrictions win. Public availability or user/repository confirmation
can establish sharing; editor credentials, common organizational membership, or
mere repository tracking cannot establish access for a different issue audience.
Keep the PR-head presumption explicitly restricted to its existing review context.

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
| Audience access is unknown | Do not disclose the unsupported private fact; ask or retain a non-disclosing limitation. |

## Instruction size and compatibility

Use concise issue paragraphs within `_shared/document-clarity.md` and update the
existing entry point. Add no issue-only guide, new skill, new shared symlink,
profile, or automatic consumer invocation. Preserve the PR paragraphs and common
rules while removing duplication only where meaning remains intact.

At the inspected baseline the shared procedure contains 1,000 whitespace-delimited
words. This follow-up retains the original 1,200-word ceiling for that procedure
and any mandatory dependencies it introduces. Count the final text and record the
result. Do not preserve the limit by dropping a safeguard, hiding instructions in
another mandatory file, or moving a necessary load after source reads. If it cannot
fit, record the actual count and needed rules in the implementation evidence and
revisit this design before treating that task as complete.

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

- **Compact guidance:** complete issue rules can fit within the retained ceiling.
  Validate with a count and fidelity review after each instruction change.
- **Available evidence:** existing read-only tools or caller-supplied descriptions
  can supply enough context for useful edits. Validate positive and missing-access
  paths with synthetic responses; no particular tracker tool is assumed present.
- **Compatibility:** additive issue guidance can preserve document/PR routing,
  fidelity, visibility, and output behavior. Validate by executing existing evals.
- **Audience resolution:** explicit context can establish sharing without inferring
  access from credentials. Validate both shared and restricted evidence cases.

## Not Doing

- Remote publication, issue updates, comments, or messages: editing authorizes local output only.
- Implementing, fixing, or reproducing the described work: those are separate execution tasks.
- New product decisions or acceptance criteria: clarification preserves meaning and uncertainty.
- Mandatory tracker integrations or live connector certification: use available read-only capabilities and supplied text.
- A separate issue guide, new skill/profile, or automatic clarification: reuse the chosen workflow and preserve ADR 0009.
- Bulk rewrites, new summary artifacts, or edits to completed designs: keep targets bounded and history frozen.

## Rejected Alternatives

| Alternative | User value | Feasibility and trade-off | Reason not selected |
| --- | --- | --- | --- |
| B: conditionally loaded issue guide | Intended reader outcome is the same; equivalence is untested. | Reduces non-issue instruction text but adds routing, a dependency, and loading-order coverage. | The bounded extension can reuse the existing procedure; revisit only if complete guidance cannot remain compact. |

No reliability, latency, or maintenance-time advantage has been measured for either
approach. A is selected for its simpler instruction structure, subject to the
explicit budget and behavioral checks above.
