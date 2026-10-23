### Workflow

**Mandatory ordering — methodology before evidence.** Follow this workflow strictly in sequence. Load basic instructions and every resolved profile checklist before investigating source, searching knowledge, forming findings or preparing evidence. The sole early-content exception is bounded routing for declared detection/conditional-load predicates: approximately 16 KiB per candidate file, predicate/path logged, conservative loading when undecidable. Routing permits no behavioral analysis, full-diff investigation, edits or tests.

```
Isolated Code Review Progress:
- [ ] Step 1: Load basic instructions
- [ ] Step 2: Resolve scope from filenames/metadata only
- [ ] Step 3: Detect profiles and route all checklists
- [ ] Step 4: Read every checklist and confirm the loading gate
- [ ] Step 5: Investigate and prepare equivalent evidence for every reviewer
- [ ] Step 6: Discover the external backend once, spawn reviewers and resolve evidence requests
- [ ] Step 7: Annotate findings without overriding reviewers
- [ ] Step 8: Index systemic findings
- [ ] Step 9: Present findings, coverage and qualified verdict; confirm next steps
- [ ] Step 10: Verify outputs and clean up temporary evidence
```

## Step 1: Load Basic Instructions

Read [SKILL.md](SKILL.md), this workflow, [shared-capy-knowledge-protocol.md](shared-capy-knowledge-protocol.md), [shared-profile-detection.md](shared-profile-detection.md), [shared-review-scope-protocol.md](shared-review-scope-protocol.md), [shared-change-context.md](shared-change-context.md), [functional-review.md](functional-review.md), [shared-pal-codereview-invocation.md](shared-pal-codereview-invocation.md) (API transport), and [shared-external-review-invocation.md](shared-external-review-invocation.md) (one-time backend discovery, clink roster and reviewer bookkeeping). Already loaded, unchanged instructions need not be read twice. The common method applies even without profiles or specification documents.

## Step 2: Resolve Scope from Filenames/Metadata

Use status, diff statistics and filenames only to resolve scope. Honor an explicit range/file selection; otherwise choose unstaged changes, falling back to staged when none are unstaged. Keep that selector throughout preparation; do not silently combine scopes. If neither has changes, report that and request a range. A feature-directory listing may locate specifications; reading them belongs to investigation. Metadata scope does not open the investigation gate: the next actions are detection-rule reads, profile indexes and their checklists, never the diff or feature documents.

## Step 3: Detect Profiles and Route All Checklists

Run the shared detection procedure on scoped filenames. Read each entry in its **Known profiles** list and record the returned rule paths; do not discover names by listing directories or infer unread rules from profile names. An obvious extension match does not end enumeration. Resolve the plugin root from the loaded skill location (parent of `skills/`); construct absolute instruction paths rather than forwarding unresolved root tokens. For every active profile, read `profiles/<profile>/review-code/index.md` and select always-load, matching conditional and conservatively selected entries. Evaluate metadata predicates first; use only the bounded routing exception for content predicates. Do not defer conditionals until investigation.

Batch the Known-profile reads together when supported, then reconcile expected versus returned rule paths before resolving profiles. An unread rule keeps routing incomplete; do not substitute a remembered extension rule for its returned contents.

The size bound alone does not authorize a read. Before any routing content read, name the unresolved predicate from an already returned detection rule/index and the candidate path it applies to. Extension/filename-only decisions require no source bytes. **Never run a full `git diff` for routing, even for a tiny diff:** inspect only a bounded candidate-file view needed by that declared predicate. With no unresolved content predicate, proceed directly to checklist loading.

Collect `(profile, checklist, triggered_by)` records with absolute checklist paths and conservative-load notes.

## Step 4: Read Every Checklist and Confirm Loading

Read every selected file: an index or requested path is not returned instruction content. Do not batch these reads with investigation. Emit a compact loading checkpoint naming completed common-instruction reads and loaded checklists (or no active profiles). A failed or omitted instruction read keeps the gate closed; surface unreadable paths. Explicitly reconcile every resolved path with returned contents before proceeding. Loading the common files alone does not satisfy this gate. Do not read the diff, source or specifications in the same call as detection, index or checklist reads.

## Step 5: Investigate and Prepare Evidence

This is the single entry point for subject-matter investigation. Locate and read available component README/contract documentation and relevant design/task contracts first; establish explicit intent and preserved invariants, labeling inference when no contract exists. Then read the selected full diff and changed files at the reviewed candidate, accounting for deletions. For staged review use index blobs; for a commit range use the selected candidate revision. Materialize those candidate sources outside the worktree when its current files differ; never pass unrelated worktree bytes as reviewed source. Large diffs (>500 lines) may be batched by module; report any context limit.

Write the selected diff to a temporary file outside the reviewed worktree, using `mktemp` and the same selector. Keep evidence until every reviewer and any follow-ups finish.

### Context and affected paths

- Build the Task Scope block from those contracts with the shared scope protocol, including the invoking implementation task even if still in progress. Without a related feature, use its no-task-scope variant.
- Establish or refresh the shared change context: intent/authority, task boundary, preserved behavior, delivery constraints, review base/candidate, separate compatibility baselines, scenarios and attributed verification results. Without a spec, infer provisional purpose from the request, diff, callers and tests; label it. Functional reasoning remains required.
- Trace affected behavior using the common method, including unchanged consumers and required compatibility combinations. Select source by the contract question it answers, not directory proximity. Search `kk:review-findings` and, for active programming-language profiles, `kk:lang-idioms`.
- Include concrete rejected-approach facts if useful, with their source; omit implementation-session narrative. Author explanations and test claims remain attributed evidence that reviewers may challenge.
- If exploration adds a target with another profile or conditional, pause its analysis and return to routing/loading before proceeding.

### Historical source and evidence manifest

When a comparison depends on source absent from candidate files or diff hunks, obtain the actual local Git blob or bounded excerpt. Materialize it in a read-only evidence bundle outside the reviewed worktree. For each item record repository identity, full revision, original path, blob/content hash, original line span and omitted/redacted extent. Distinguish source-level tag comparisons from verified deployment state. A missing source stays explicitly Unknown; a parent summary cannot replace it.

Before declaring a named baseline unavailable, inspect relevant repository documentation for its location and attempt to resolve the stated local ref/tag and source path in Git. If only a symbol/component is named, use a bounded history/tree lookup to locate it. Record the attempted ref/path and result. A separate-repository description or absence from the checkout does not prove absence from local history. Review-base mocks establish test assumptions, not the named provider's implementation; do not substitute them for available historical source.

Prepare one categorized manifest for every reviewer, with absolute paths:

1. **Instructions:** shared change context, common functional method, scope/knowledge protocols and all resolved profile checklists. These are criteria, not review targets.
2. **Review evidence:** selected diff, changed candidate source (mark deletions), unchanged entry points, dependencies, consumers, state contracts and relevant delivery configuration. Ten surrounding files is an initial selection budget only. Follow identified contract questions through focused additions or name the uncovered boundary; do not scan the whole repository.
3. **Historical evidence:** actual source files plus provenance manifest, distinct from candidate source.
4. **Intent/context:** applicable specification files, Task Scope and factual change-context record. The record may be inlined into both prompts or placed in a readable file provided to both; a filename alone is insufficient evidence of receipt.

Use these same material facts and source artifacts for every reviewer. The external backend is not chosen here; Step 6 discovers it once.

Before dispatch, compare the manifest's instruction paths with the loading ledger. Every resolved checklist (including always-load templates), common method, shared context, scope and knowledge protocol must appear in every reviewer's instruction set. Do not drop an always-load file as irrelevant or rebuild a smaller list from memory. Reconcile missing paths now; carry this checked manifest unchanged into the agent payload, PAL's expert continuation or each clink reviewer's first request, adding focused evidence only when needed.

The required criteria set has **four common files plus every resolved profile file**: `functional-review.md`, `shared-change-context.md`, `shared-review-scope-protocol.md`, `shared-capy-knowledge-protocol.md`, and the resolved checklist paths. Verify both the count and exact resolved paths, using a set comparison through available tools when possible. The knowledge protocol remains included even when an external reviewer cannot use Capy; that protocol specifies the unavailable-tool fallback. Keep criteria and source paths in the prepared manifest so submission does not depend on reconstructing either list from memory.

## Step 6: Discover the Backend, Spawn Reviewers and Resolve Evidence Requests

### External backend discovery

Run the shared external-review protocol's discovery exactly once, now: inspect the advertised PAL tool surface and call `listmodels`, then record the frozen decision — **API** (resolve the most capable available model with reasoning support, per the PAL protocol), **clink** (build the roster: candidates, authoring provider, declared provider mapping, exclusions, one client per provider), **unresolved** or **none**. One focused roster question, covering whatever is unresolved (authoring provider, undeclared client-to-provider mappings, duplicate-provider choice), is asked before any clink dispatch; the internal reviewer does not wait for it. The decision never changes within this invocation: an API runtime failure stays an API failure and does not re-open discovery.

Launch the independent `code-reviewer` and the first external request in parallel when supported (clink reviewers run sequentially after that). No reviewer receives implementation conversation history or another reviewer's conclusions.

### Reviewer A — code-reviewer

Use the Agent tool with `subagent_type: kk:code-reviewer`, description `Isolated code review`, and this payload. Expand plugin-relative checklist paths to absolute paths before dispatch; the reviewer requires resolved paths rather than environment variables.

```
Review the selected changes using your full workflow. Load instructions before evidence.

## Plugin Root
{resolved absolute plugin root}

## Instructions
{absolute paths to shared change context, functional method, scope/knowledge protocols}

## Active Profiles and Resolved Checklists
{flat (profile, absolute checklist path, triggered_by) records; conservative selections; or empty list}

## Change Context and Spec Context
{factual record with provenance, assumptions, attributed execution results and spec paths;
or explicitly inferred intent when no spec exists}

{Task Scope block}

## Evidence Manifest
{selected diff path, candidate/source paths, historical-source paths and provenance manifest;
review selector and candidate identity; missing evidence}

## Rejected Approaches
{concrete attributed facts only, or none}

Independently inspect the evidence and challenge inferences. Request specific missing source
by repository, revision, path/symbol and comparison needed. Report provisional findings and
limits in your agent output format; do not claim test execution from source-only access.
```

### Reviewer B — external review (API branch)

When discovery selected API, use the shared PAL protocol's two-step external review with the resolved model. Keep `step` lean: functional/correctness, security, architecture and design-intent framing; the same Task Scope and change-context facts; spec summary (or inferred purpose); categorized absolute file manifest. Identify the common method and profiles as criteria, historical source as baseline evidence and candidate source as the review target. The initial planning call's `relevant_files` contains only the selected diff; the expert continuation must attach the complete source/context/criteria bundle. Pass actual files through `relevant_files`, not pasted contents in `step`.

After the initial response, complete the continuation; do not mistake the planning response for external findings. Preserve the native output and actual source-coverage evidence. Supplying paths does not prove the external reviewer read them.

Immediately before the expert call, verify its `relevant_files` contains every path in the checked manifest. The diff-only planning payload is not the expert payload. A nonempty set of missing instruction/evidence paths blocks submission until those paths are added.

### Reviewers B… — external review (clink branch)

When discovery selected clink, send each roster client one fresh `clink` request under the shared protocol's request contract (`role: default`, `allow_edits: false`, project root as working directory, no model parameter, no `continuation_id`). Attach the **complete** checked manifest in `absolute_file_paths` on this first request — criteria, candidate evidence, historical evidence with provenance and intent/context; there is no diff-only planning call. Immediately before each request, verify that `absolute_file_paths` contains every manifest path; a missing path blocks that request until added.

Build the `prompt` from this template, with facts only:

```
Independent code review. Read the criteria first, in order, then the evidence. Perform the
review yourself: do not invoke isolated-review skills or sub-agents. Make no edits to project
files and run no tests, builds or commands that write files; read-only inspection commands
are acceptable where you need them to read files. The listed diff and candidate snapshot
paths are the review target: do not run your own `git diff` and do not substitute
working-tree copies for listed candidate files. Return findings with file:line, your native
severity, the files you actually read and those you could not read, and any evidence requests.

## Criteria (apply, do not review)
{absolute paths: common method, shared change context, scope/knowledge protocols, resolved checklists}

## Review target
{selected diff path; candidate source paths with revision/index identity, deletions marked}

## Affected behavior
{unchanged entry points, consumers, contracts, delivery configuration}

## Historical evidence
{historical source paths and provenance manifest, or none}

## Intent and context
{spec paths, Task Scope block, factual change-context record}
```

Record configured and observed model identity separately from the response. Preserve native output; do not remap severity.

### Outcome records and receipt

Before annotation, record each reviewer's outcome class (requested, attempted, executed, adequately evidenced) and observed source receipt under the shared protocol's reviewer record. For the API path inspect PAL's returned file-context/embedding metadata; for clink inspect returned tool-use/read results and denied-action metadata. Zero or unspecified coverage without other observable receipt evidence stays unverified. Final findings, the parent's `files_checked` list and correct-looking citations cannot establish receipt. Carry that limitation into the report before deciding whether any finding is corroborated.

### Additional evidence and continuation

For any reviewer's evidence request, retain its origin and requested repository/revision/path or symbol and comparison. Obtain available local source using the historical-bundle rules. Resume the requesting code-reviewer with the original scope/context, its provisional findings and new source; if resume is unavailable, re-invoke it with that same package. Send equivalent relevant additions to each external reviewer through its own continuation (API `continuation_id`, or that clink reviewer's `continuation_id` with `allow_edits: false`), and to every other reviewer whose assessment depends on them. Include new guidance first if an addition activates a profile/conditional.

Before final reporting, reconcile every request with either supplied source or an actual failed/bounded lookup. Do not merely defer a locally answerable request because an earlier handoff assumed the source was unavailable. A request essential to acceptance that remains unanswered keeps its conclusion Unknown under the common verdict mapping.

Do not pass one reviewer's findings to another as evidence. Track what was supplied and which questions remain unanswered. Stop collecting once the identified comparison is settled or bounded investigation reaches an unavailable boundary. Unavailable source remains Unknown with a specific next action; do not expand reviewer permissions or seek production/network access automatically.

### Failure and coverage limits

- If discovery is unresolved, or an external backend/call fails, retain useful available findings and proceed with the remaining reviewers; disclose the failure. An API failure never triggers clink; a failed clink client is not retried or replaced.
- If one clink client fails while others succeed, keep every attempted request in the record with its own outcome and attribution.
- If the code-reviewer fails, retain usable external findings and suggest standard review as a supplement.
- If every reviewer fails, stop isolated review and suggest standard review. Do not imply a completed review or run standard review silently.
- Attempt best-effort parsing of malformed output; wholly unusable output is a failure.
- A successful response with zero or unverified source coverage cannot establish corroboration or broad approval. An adequately sourced clean result is not a failure merely because it found no defect.

## Step 7: Annotate Findings

The parent supplies context, not replacement reviewer judgments. Do not assign dispositions such as Confirmed/Disputed or silently discard findings based on author preference.

- Merge the same logical issue across lenses/reviewers once and list every supporting reviewer. Mark it **corroborated** only when at least two independent reviewers support it with relevant observable evidence; name their actual providers. Two external reviewers may corroborate an issue the code-reviewer missed; a reviewer with unverified receipt or a same-provider duplicate cannot corroborate. Otherwise preserve separate attribution and the coverage gap. Show differing severities side by side; external reviewers keep their native format and severity, and a majority is not a verdict.
- Add clearly labeled **Author context** where the implementation rationale helps: “I chose X because Y,” not “This finding is invalid.”
- Label new parent observations **author-sourced**, distinct from independent findings.
- Use the reviewer's own continuation to clarify ambiguous external findings if needed. Preserve disagreements and provisional findings while awaiting source.

## Step 8: Index Findings

Index systemic P0/P1 patterns as `kk:review-findings` on first encounter, from any attributed source, under the shared knowledge protocol. Do not index one-off mistakes. When none qualify, explicitly state “No findings to index.”

## Step 9: Present Report and Confirm Next Steps

Apply the common method's verdict mapping; keep code correctness, increment compatibility and release/activation readiness distinct. A hard acceptance/delivery violation cannot receive approval. Material Unknown evidence receives COMMENT absent a demonstrated blocker; an unrelated operational unknown need not downgrade a supported, explicitly scoped code verdict.

```markdown
## Review Summary (Isolated Mode)

**Reviewers**: code-reviewer ([actual model]); external backend [API / clink / unresolved / none] —
  per external reviewer: client/provider, configured vs observed model, outcome class, receipt
**Roster**: eligible providers attempted; excluded (authoring provider, duplicates, unknown identity); failures
**Files reviewed**: actual inspected coverage per reviewer, distinct from files supplied
**Overall assessment**: APPROVE / REQUEST_CHANGES / COMMENT, with scope
**Intent and scope**: requirement source, task/request, diff selector and candidate state
**Baselines**: review base/candidate; separate named compatibility baseline

### Behavior and Compatibility
Inspected paths/scenarios, Supported / Blocked / Unknown / Not applicable conclusions,
source references and limits. Attribute author results and inherited issues.

### Corroborated Findings
- **[file:line]** Title ⟨corroborated: {supporting reviewers with providers}⟩
  - Profile: {profile} · Checklist: {checklist} · Triggered by: {signal}
  - code-reviewer: [P0–P3, confidence/reasoning, trigger/path, expected/actual, consequence, correction]
  - {external reviewer, client/provider}: [native finding]
  - Author context: [optional]

### Code Reviewer Findings
{same evidence fields, code-reviewer attribution}

### External Review Findings
{one subsection per external reviewer: native output with attribution, receipt/coverage limits
and optional author context}

### Author-Sourced Findings
{explicit author-sourced label; generic profile labels when appropriate}

### Outstanding Evidence and Prerequisites
{missing evidence, release/migration/activation conditions, owner, next action and durable
tracking location when deferred; separate them from demonstrated code defects}
```

Omit empty finding sections, but always report behavior/compatibility coverage and limits, even with defects, and always report the backend decision, roster and per-reviewer outcomes, even with no findings. Preserve useful findings during external failure or undercoverage without claiming corroboration or release safety from that external response.

When neither actionable findings nor outstanding evidence/prerequisites required
by the reviewed task remain,
finish with the scoped verdict and coverage; state that no changes are recommended.
Do not append a remediation menu or offer hypothetical future work. Otherwise,
offer only supported actions. For review-only work, obtain authorization before
editing; when the invoking implementation request already authorizes fixes,
follow that scope without asking again. Unverified hard requirements still follow
the common method's conditional verdict rules.

## Step 10: Verify Outputs

- [ ] Findings, actual scope/baselines, behavior/compatibility and evidence limits presented
- [ ] Backend decision, roster and every reviewer's outcome and coverage disclosed; additional evidence supplied or gaps named
- [ ] Systemic findings indexed, or “No findings to index” noted
- [ ] Required next steps agreed/authorized, or clean review closed without new work

Retain evidence needed for unresolved requests or a durable deferred review record. Once follow-ups and any required retention are complete, remove only temporary files/bundles created for this review.
