### Workflow

**Mandatory ordering — methodology before evaluation.** Follow this workflow strictly in sequence. Load the skill, this process, the shared protocols and the shared design-review criteria before reading, searching or evaluating subject documents. Scope resolution uses invocation arguments and directory listings only; the documents are read once, in Step 3.

```
Isolated Design Review Progress:
- [ ] Step 1: Load instructions
- [ ] Step 2: Resolve document scope from arguments and listings
- [ ] Step 3: Read documents and prepare the shared manifest
- [ ] Step 4: Discover the external backend once, spawn reviewers and resolve evidence requests
- [ ] Step 5: Annotate findings
- [ ] Step 6: Index findings
- [ ] Step 7: Present report and confirm next steps
```

## Step 1: Load Instructions

Read [SKILL.md](SKILL.md), this workflow, [shared-capy-knowledge-protocol.md](shared-capy-knowledge-protocol.md), [shared-verification-policy.md](shared-verification-policy.md), [shared-design-review-criteria.md](shared-design-review-criteria.md) (the checks every reviewer applies), [shared-pal-codereview-invocation.md](shared-pal-codereview-invocation.md) (API transport; use its document-review branch) and [shared-external-review-invocation.md](shared-external-review-invocation.md) (one-time backend discovery, clink roster and reviewer bookkeeping). Already loaded, unchanged instructions need not be read twice.

Resolve the absolute paths of the two criteria files, the design-review criteria and the verification policy, from this skill's directory, and the plugin root (parent of `skills/`). Every reviewer receives those two files as methodology, not as review targets; the internal reviewer additionally receives the plugin root.

## Step 2: Resolve Document Scope

Parse the invocation arguments:

- Extract the feature name and the optional scope argument.
- **Argument disambiguation:** if the first argument matches a directory in `/docs/feat/wip/`, treat it as the feature name. If it matches a scope keyword (`design`, `implementation`, `tasks`) and no such feature directory exists, treat it as the scope and ask the user for the feature name.
- Locate `/docs/feat/wip/[feature-name]/`. If the feature name is missing or ambiguous, list `/docs/feat/wip/` and ask the user.

| Scope arg        | Documents in scope                             |
| ---------------- | ---------------------------------------------- |
| _(none)_         | `design.md` + `implementation.md` + `tasks.md` |
| `design`         | `design.md` only                               |
| `implementation` | `implementation.md` only                       |
| `tasks`          | `tasks.md` only                                |

Use a directory listing to decide which in-scope documents exist. A requested document that is missing is disclosed to the user and to every reviewer as a coverage limit; proceed with the available documents. If no in-scope document exists, stop and report that instead of reviewing something else. Do not read documents in this step.

## Step 3: Read Documents and Prepare the Manifest

This is the single entry point for subject-matter reading. Read the in-scope documents from the feature directory. Then assemble one categorized manifest, with absolute paths, that every reviewer receives:

1. **Documents** — the in-scope documents that exist. These are the review targets.
2. **Related source** — existing files the documents reference as current code (to be modified, depended on or cross-checked), when they exist on disk. Files the documents describe as to-be-created are listed by name as **planned**, not as related source and not as missing evidence.
3. **Review criteria** — the design-review criteria and the verification policy, identified as methodology to apply, not documents under review.

Record the requested-but-missing documents and the planned files alongside the manifest. Use the same manifest and the same factual framing for every reviewer; the external backend is not chosen here.

## Step 4: Discover the Backend, Spawn Reviewers and Resolve Evidence Requests

### External backend discovery

Run the shared external-review protocol's discovery exactly once, now: inspect the advertised PAL tool surface and call `listmodels`, then record the frozen decision — **API** (resolve the most capable available model with reasoning support, per the PAL protocol), **clink** (build the roster: candidates, authoring provider, declared provider mapping, exclusions, one client per provider), **unresolved** or **none**. For document review the authoring provider is the provider that produced the reviewed documents, resolved from explicit authorship or from this session's context when it produced them; the host CLI of a later, separate review session is not evidence. One focused roster question, covering whatever is unresolved (authoring provider, undeclared client-to-provider mappings, duplicate-provider choice), is asked before any clink dispatch; the internal reviewer does not wait for it. The decision never changes within this invocation: an API runtime failure stays an API failure and does not re-open discovery.

Launch the independent `design-reviewer` and the first external request in parallel when supported (clink reviewers run sequentially after that). No reviewer receives the design conversation history or another reviewer's conclusions.

### Reviewer A — design-reviewer

Use the Agent tool with `subagent_type: kk:design-reviewer`, description `Isolated design review`, and this payload with every path absolute:

```
You are reviewing the design documents for the "{feature_name}" feature. Apply your full review workflow: load the review criteria before any document.

## Plugin Root
{resolved absolute plugin root}

## Review Criteria
- Design-review criteria: {absolute path to shared-design-review-criteria.md}
- Verification policy: {absolute path to shared-verification-policy.md}

## Feature Directory
{absolute path to /docs/feat/wip/[feature]/}

## Documents to Review
- Design: {absolute path to design.md} (or "Not in scope" / "Requested but missing")
- Implementation: {absolute path to implementation.md} (or "Not in scope" / "Requested but missing")
- Tasks: {absolute path to tasks.md} (or "Not in scope" / "Requested but missing")

## Related Source
{absolute paths of existing referenced files, or none; planned files named as planned}

Read the documents yourself using the Read tool. Produce your findings in the output format specified in your agent definition.
```

### Reviewer B — external review (API branch)

When discovery selected API, use the shared PAL protocol's two-step external review with the resolved model and its document-review branch. Keep `step` lean:

1. Framing: "The following documents are design documents (markdown), not source code; implementation they describe is planned work, not a missing implementation. Review them for technical soundness, completeness, internal consistency, feature value and sufficient implementation detail. Apply the supplied design-review criteria and verification policy as methodology. Focus on consequential edge cases, missing constraints and ambiguities that would block an implementer."
2. Scope: the feature name, the requested scope and any requested document that is missing.
3. The categorized manifest from Step 3 as **Documents**, **Related source** and **Review criteria**, with planned files named as planned.

Pass the manifest through `relevant_files` on the initial call and again on the expert continuation; do not paste document contents into `step`. Immediately before the continuation, verify its `relevant_files` contains every manifest path; a missing path blocks submission until added. Complete the continuation; the initial response is not external findings. Preserve native output and the returned source-coverage evidence; supplying paths does not prove the external reviewer read them.

### Reviewers B… — external review (clink branch)

When discovery selected clink, send each roster client one fresh `clink` request under the shared protocol's request contract (`role: default`, `allow_edits: false`, the project root as working directory, no model parameter, no `continuation_id`). Attach the **complete** manifest in `absolute_file_paths` on this first request: criteria, documents and related source. Immediately before each request, verify `absolute_file_paths` contains every manifest path; a missing path blocks that request until added.

Build the `prompt` from this template, with facts only:

```
Independent design-document review. The listed documents are feature proposals (markdown),
not source code: implementation they describe is planned work, so do not report code that
does not exist yet as a missing implementation. Read the criteria first, in order, then the
documents, then any related source. Perform the review yourself: do not invoke review skills
or sub-agents. Make no edits to any file and run no commands that write files; read-only
inspection commands are acceptable where you need them to read files. Review only the listed
documents; do not substitute other files from the working directory. Return findings with
document and section, your native severity, the files you actually read and those you could
not read, and any evidence requests.

## Criteria (apply, do not review)
{absolute paths: design-review criteria, verification policy}

## Documents (review targets)
{absolute paths; requested documents that are missing}

## Related source (existing code the documents reference)
{absolute paths, or none; planned files named as planned}

## Context
{feature name; requested scope; review purpose}
```

Record configured and observed model identity separately from the response. Preserve native output; do not remap severity.

### Outcome records and receipt

Before annotation, record each reviewer's outcome class (requested, attempted, executed, adequately evidenced) and observed receipt under the shared protocol's reviewer record. For the API path inspect PAL's returned file-context/embedding metadata; for clink inspect returned tool-use/read results and denied-action metadata. Zero or unspecified coverage without other observable receipt evidence stays unverified. Final findings, correct-looking section citations and a reviewer-authored file list cannot establish receipt. Carry that limitation into the report before deciding whether any finding is corroborated.

### Additional evidence and continuation

For any reviewer's evidence request (a referenced source file, a document section, a missing requested document that has since appeared), obtain what is available locally and send equivalent relevant additions to each affected reviewer without sharing any reviewer's conclusions: resume the design-reviewer with its original scope and provisional findings, and use each external reviewer's own continuation (API `continuation_id`, or that clink reviewer's `continuation_id` with `allow_edits: false`). Unavailable material stays an explicit coverage limit with a next action; do not expand reviewer permissions.

### Failure and coverage limits

- If discovery is unresolved, or an external backend/call fails, retain useful available findings, proceed with the remaining reviewers and disclose the failure. An API failure never triggers clink; a failed clink client is not retried or replaced.
- If one clink client fails while others succeed, keep every attempted request in the record with its own outcome and attribution.
- If the design-reviewer fails, retain usable external findings and suggest `/kk:review-design` (standard mode) as a supplement.
- If every reviewer fails, stop isolated review and suggest `/kk:review-design` (standard mode). Do not imply a completed review or run standard review silently.
- Attempt best-effort parsing of malformed output; wholly unusable output is a failure.
- A successful response with zero or unverified receipt cannot establish corroboration; an adequately sourced clean result is not a failure merely because it found nothing.

## Step 5: Annotate Findings

The main agent supplies context, not replacement reviewer judgments. Do not assign dispositions such as Confirmed/Disputed; the user is the final arbiter.

- **Duplicate merging.** Merge the same logical issue (same document section, same concern) across reviewers once and list every supporting reviewer. Mark it **corroborated** only when at least two independent reviewers support it with relevant observable evidence; name their actual providers. Two external reviewers may corroborate an issue the design-reviewer missed; a reviewer with unverified receipt or a same-provider duplicate cannot corroborate. Severity stays as the design-reviewer assessed it; external reviewers keep their native format and implied urgency side by side. Do not map native output to P0–P3, and a majority is not a verdict.
- **Planned work.** An external finding that treats planned implementation as missing code is kept with its attribution and annotated as planned work; it is not promoted to a corroborated defect.
- **Author context.** Where the design session adds relevant information, add a clearly labeled **Author context** annotation: "We chose X because Y" is context; "This finding is invalid" is not.
- **Author-sourced findings.** Label new observations made during this close re-reading **author-sourced**, distinct from independent findings.
- **Follow-up.** Clarify an ambiguous external finding through that reviewer's own continuation if needed.

## Step 6: Index Findings

Index confirmed `TECH_RISK` findings that reveal non-obvious architectural constraints as `kk:arch-decisions`, and confirmed P0/P1 findings that suggest a systemic or structural design pattern as `kk:review-findings`, from any attributed source. Index on first encounter; do not index one-off issues. When none qualify, state "No findings to index."

## Step 7: Present Report and Confirm Next Steps

```markdown
## Design Review Summary (Isolated Mode)

**Reviewers**: design-reviewer ([actual model]); external backend [API / clink / unresolved / none] —
  per external reviewer: client/provider, configured vs observed model, outcome class, receipt
**Roster**: eligible providers attempted; excluded (authoring provider, duplicates, unknown identity); failures
**Documents reviewed**: in-scope documents; requested documents that were missing; related source supplied
**Coverage**: per reviewer, files actually read versus supplied, and receipt limits

---

### Corroborated Findings

- **[doc:section]** Brief title ⟨corroborated: {supporting reviewers with providers}⟩
  - design-reviewer: Type: [finding_type] | Severity: P[0-3] | Confidence: [N]/10 — [reasoning];
    description, evidence, recommendation
  - {external reviewer, client/provider}: [native finding]
  - Author context: [optional annotation]

### Design Reviewer Findings

- **[doc:section]** Brief title
  - Type: [finding_type] | Severity: P[0-3] | Confidence: [N]/10 — [reasoning]
  - **Description:** / **Evidence:** / **Recommendation:**
  - Author context: [optional annotation]

### External Review Findings

{one subsection per external reviewer: native output with attribution, receipt/coverage limits,
planned-work annotations and optional author context}

### Author-Sourced Findings

- **[doc:section]** Brief title ⟨author-sourced⟩
  - [description]

### Outstanding Evidence and Prerequisites

{missing requested documents, unanswered evidence requests, outstanding PAL/roster prerequisites,
with owner and next action when deferred}
```

Omit empty finding sections, but always report the backend decision, roster, every reviewer's outcome and coverage, and the document scope actually reviewed, even with no findings. If a reviewer failed, note the failure at the top and present the available findings under their sections. Preserve useful findings during external failure or unverified receipt without claiming corroboration from that response.

### Next steps

After presenting the report, ask the user how to proceed:

```markdown
---

## Next Steps

I found X issues (corroborated: ..., design-reviewer: ..., external per reviewer: ..., author-sourced: ...).

**How would you like to proceed?**

1. **Update docs** — I'll revise the design docs to address all findings
2. **Update corroborated + high severity** — Address corroborated findings and P0/P1 issues
3. **Update specific items** — Tell me which findings to address
4. **Proceed to implementation** — Findings are acceptable, move forward
5. **No changes** — Review complete, no action needed

Please choose an option or provide specific instructions.
```

**Important:** Do NOT update any documents until the user explicitly confirms.

### Verify outputs

- [ ] Backend decision, roster and every reviewer's outcome, receipt and coverage disclosed
- [ ] Document scope, missing requested documents and planned files reported
- [ ] Findings annotated without replacing reviewer judgment; corroboration evidence-backed only
- [ ] Qualifying findings indexed, or "No findings to index" noted
- [ ] Next steps offered; no document edited before the user confirms
