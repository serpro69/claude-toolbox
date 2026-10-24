# Skills

The kk plugin ships 15 workflow and utility skills, including a complete development pipeline.

## The Pipeline

Use `/kk:brainstorm` when you want to think through a technical idea in conversation. It is optional: start with `/kk:design` whenever you want written planning.

```
/kk:design → /kk:review-design → /kk:implement → /kk:review-code → /kk:test → /kk:document
```

1. **/kk:design** — turns an idea into design docs, an implementation plan, and a task list
2. **/kk:review-design** — evaluates design docs for completeness and technical soundness
3. **/kk:implement** — establishes behavior and constraints, executes tasks and hands current evidence to review
4. **/kk:review-code** — reviews functional behavior, compatibility, SOLID, security and quality
5. **/kk:test** — selects meaningful coverage, runs relevant checks and honors required repository/release suites
6. **/kk:document** — updates architecture docs and records ADRs

## Skill Reference

| Skill | What it does |
|-------|-------------|
| **/kk:brainstorm** | Interviews anyone exploring a technical idea or decision, adapting depth to the next decision. Asks one question at a time and closes with decisions, rationale, and open assumptions in chat; creates no files. |
| **/kk:design** | Turns an idea into design docs, an implementation plan, and a task list in `docs/feat/wip/`. Asks refinement questions, then documents everything a developer needs to start coding. |
| **/kk:implement** | Executes a feature plan or standalone fix after establishing intended behavior, affected callers and delivery constraints. Refreshes evidence for independent review and distinguishes code completion from external release prerequisites. |
| **/kk:test** | Reuses or adds meaningful coverage, runs relevant checks and required repository/release suites, and reports actual results and limits. Chooses testing techniques to suit the requirement. |
| **/kk:document**  | Updates project documentation and records ADRs for non-obvious decisions made during implementation.                                                                     |
| **/kk:review-code** | Traces changed behavior and affected contracts, including unchanged callers and relevant historical sources, alongside SOLID/security/quality checks. Domain-specific guidance covers Go, Java, JS/TS, Kotlin, Python, Kubernetes, K8s Operator and agent skills. Standard and isolated modes. |
| **/kk:review-design** | Pre-implementation review gate. Evaluates design docs for completeness, internal consistency, and technical soundness before code is written. Standard and isolated modes. |
| **/kk:review-spec** | Compares implemented code against design/implementation docs. Finds spec deviations, missing implementations, and outdated docs — in both directions. |
| **/kk:model** | Produces or updates a domain-reference kit — a durable glossary + divergences/traps page pair per bounded context, with concept-to-code bindings. Its primary output is a decision queue of precise, role-tagged questions only a human can close. Runs upstream of `/kk:design` as the first producer of the architecture flow. |
| **/kk:review-architecture** | Reviews a written architecture artifact (ADR, architecture doc, a design doc's architecture section, or a domain-reference kit — glossary + traps pages reviewed as one composite artifact) against the system it describes. Claim-driven: extracts an inspectable claim-set, verifies mechanism existence/topology across seven dimensions, and grades decision soundness, reversibility, and provenance (self-certification of reverse-engineered claims). Security architecture is delegated to PAL `secaudit`. |
| **/kk:dependency-handling** | Fires before calling a library/SDK/API or adding a dependency. Forces a capy/context7 lookup instead of guessing signatures or behavior. |
| **/kk:diff-skill** | Compares two versions of a skill's markdown instructions to detect degradations and complexity increases. Asymmetric — only regressions count. |
| **/kk:merge-docs** | Merges two competing design docs for the same feature into one unified document, resolving conflicts and preserving the best of both. |
| **/kk:clarify-docs** | Improves selected documentation, PR drafts and issue descriptions after understanding requirements and source. Produces local edits, preserves meaning and respects the intended audience's access. |
| **/kk:chain-of-verification** | Makes Claude fact-check its own answers. Standard mode (prompt-based) or isolated mode (independent sub-agents). For high-stakes accuracy. |

## Commands

Commands are skill variants invoked with explicit mode selection:

| Command | Invocation | Description |
|---------|-----------|-------------|
| Code Review (isolated) | `/kk:review-code:isolated` | Functional, compatibility and quality review with independent reviewers |
| CoVe (standard) | `/kk:chain-of-verification:default [question]` | Chain-of-Verification with prompt-based isolation |
| CoVe (isolated) | `/kk:chain-of-verification:isolated [--explore] [--haiku] [question]` | CoVe with true sub-agent isolation |
| Spec Review | `/kk:review-spec:default [feature]` | Verify code matches design/implementation docs |
| Spec Review (isolated) | `/kk:review-spec:isolated [feature]` | Spec conformance review with independent sub-agent |
| Template Sync | `/kk:template:sync [--version vX.Y.Z] [--dry-run]` | Sync repo with upstream template |

## Functional review and implementation

Use `/kk:review-code` for an ordinary change review; functional reasoning is part
of the existing invocation. The reviewer establishes the requested increment and
review baseline, traces changed behavior through relevant unchanged callers, and
checks meaningful success, boundary and failure scenarios. A specification helps,
but the reviewer can use repository contracts and label inferred intent when
formal design documents are absent.

For example, renaming a report label can be approved while an unchanged,
disabled calculation has an inherited bug. Enabling that calculation by default
is a different change: if valid empty input now crashes, the increment needs a
fix. A feature flag only supports a compatibility claim when the affected paths
actually obey it.

The report explains consequential findings, assessed paths and evidence limits.
Compatibility can be **Supported**, **Blocked**, **Unknown** or **Not applicable**
for the named baseline and scenarios. Missing deployment information does not
automatically block a scoped code review; it does prevent certifying a deployment
when that evidence is essential. Local tests and released-source inspection do
not verify a live environment.

`/kk:review-code:isolated` prepares the relevant diff, current/historical source,
task scope and review criteria for a named reviewer and PAL. If an external
reviewer is unavailable or receives insufficient source, the report retains the
available findings and discloses the lost coverage. Independent review does not
guarantee correctness. See [Isolated reviews and external models](#isolated-reviews-and-external-models)
for how the external reviewers are chosen and what the report can claim.

`/kk:implement` applies the same behavioral context before editing, runs
appropriate verification, and refreshes the evidence supplied to review. Use
`/kk:implement Fix the empty-note update while preserving omitted settings` for
a standalone change, or name a feature task to use its design and task records.
A known unmet hard requirement keeps the task open. External activation work can
remain separate when the agreed delivery contract permits it.

Testing focuses on agreed outcomes and consequential risks. Optional advice or
minor report variation is not automatically a failure; an accurately explained
inherited bug can be useful without prescribing its next action. Required checks
still need actual execution. A denied compound command does not establish that
every tool is unavailable: use an authorized direct route when appropriate, or
report the specific unresolved check. Inspect that limit before treating a change
as verified; the skills do not guarantee autonomous recovery in every session.

## Isolated reviews and external models

`/kk:review-code:isolated` and `/kk:review-design:isolated` run one internal
sub-agent (`code-reviewer` or `design-reviewer`) plus external review through
[PAL](mcp-servers.md#pal). Standard mode never calls PAL.

**Discovery-only selection.** Once per review, before any external call, the
skill checks PAL's tools and `listmodels`. With an eligible API model it runs
the existing `pal codereview` flow. Without one, and with `clink` available, it
runs one `pal clink` CLI review per eligible provider. If discovery fails or the
PAL build does not expose CLI metadata, there is no external review and the
report says so. The decision is frozen for that review: an API failure is
reported as a failure and never switches to clink.

**Roster.** Candidates are PAL's configured CLI clients whose executable was
found. The provider that authored the change (or, for design review, the
documents) is excluded, one client per provider is attempted once, and a failed
client is disclosed rather than retried or replaced. Provider identity is
**declared** (in the request, the project's `CLAUDE.md`/`AGENTS.md`, or client
configuration you name), **observed** when a shipped client's configured or returned model shows another
vendor, **assumed from shipped manifest** for PAL's shipped
names (`claude` → Anthropic, `codex` → OpenAI, `agy` → Google; the report labels
these and notes a declaration overrides them), or **undeclared** for any other
name, which triggers one question before dispatch. `gemini` is retired and never
a candidate. Cost scales with the roster: three shipped clients and a
Claude-authored change give two CLI reviews.

**Models and permissions stay yours.** On the API branch the skill selects the
most capable available model from PAL's catalog; on the clink branch it names no
model, and each CLI review uses the model configured in the CLI or its PAL client
manifest. Every request carries `allow_edits=false` and a no-edit prompt, which
is a behavior contract, not an enforced sandbox; some CLIs keep their native
permissions, and the report says so. CLIs must be able to read the plugin
installation and the temp directory `mktemp` uses (`$TMPDIR`, otherwise `/tmp`),
where criteria and evidence live; a
denied read is reported as lost coverage, never bypassed. Per-CLI setup is in
[MCP Servers → Pal](mcp-servers.md#pal).

**What the report claims.** Each external reviewer is classified as requested,
attempted, executed and adequately evidenced. Only observable read evidence
counts as receipt; of the verified clients only Claude returns one, so `codex`
and `agy` findings are kept with receipt unverified and cannot corroborate. A
finding is corroborated only when two independent reviewers support it: an
external reviewer counts only with observable receipt, the internal sub-agent
counts through its source-tied report, and a corroboration resting on an assumed
provider is labeled. Isolated design review is invoked as described in the
`/kk:review-design` skill (`/kk:review-design:isolated [feature] [scope]`); it is a
skill mode, not a separate command file. If every reviewer fails, the skill reports that isolated review did not
complete and suggests standard mode instead of running it.

**Minimum PAL.** The clink path needs a PAL build whose `listmodels` returns
`cli_clients` in every mode (commit `c73dab7d`, 2026-10-23, or a release that
contains it). Restart PAL after changing provider or CLI configuration.

## Utility Skills

### Explore a technical idea

Use `/kk:brainstorm Help me think through whether a local cache is worth adding to our developer tool` to explore alternatives, challenge assumptions, and decide whether to pursue, discard, narrow, or investigate an idea. The audience includes developers, architects, and anyone considering technical products, infrastructure, tools, operations, or engineering workflows.

The interview asks one question at a time and adapts its depth to your next decision. It reads relevant project files or web sources when evidence could change the advice, so a repository is optional. When a premise changes, it revisits affected decisions while preserving unrelated ones. Missing evidence stays explicit.

The result is a chat recap of settled decisions and their rationale, open assumptions, details that can wait, and the next decision or investigation. If you stop early, it recaps the partial discussion without claiming the idea is validated. The skill creates no files or saved interview state and performs no knowledge-store or session-vault searches, indexing, or implementation.

When written planning would help, the skill may suggest `/kk:design`. You choose whether to invoke it; the recap supplies context for its existing confirmations. Brainstorming does not invoke another workflow automatically and is not required before design. For a durable domain glossary and traps pages, use `/kk:model`; for a build or fix, use `/kk:implement`. Nontechnical brainstorming is outside this skill's scope.

### Other utilities

**/kk:dependency-handling** is pulled in automatically during implementation whenever you touch an external library, SDK, or API — it routes through capy/context7 instead of guessing.

**/kk:review-spec** verifies code matches design/spec and detects deviations — use during or after implementation.

**/kk:model** produces the domain-reference kit (glossary + traps pages) and a role-tagged decision queue for a bounded context — use before feature design when the domain's concepts, code bindings, or open questions need mapping.

**/kk:review-architecture** reviews an ADR, architecture doc, or domain-reference kit against the codebase it claims to describe — use after an architecture artifact is written, before or during implementation.

**/kk:merge-docs** reconciles competing design docs into one unified document.

**/kk:chain-of-verification** adds self-verification for high-stakes accuracy at any stage.

### Clarify an existing document

Use `/kk:clarify-docs docs/configuration.md for service owners; use src/config/`
to improve an existing guide, or select a design document or implementation plan
for the developer who needs to resume the work. Supply the target paths and any
known audience, purpose, requirements or source references. A directory helps find
the target; it does not authorize rewriting every document inside it.

The skill first understands the requirements and relevant implementation, then edits
the selected document in place. It explains purpose and behavior before reference
detail while preserving requirements, exceptions, decisions, task state and links.
Source disagreements and missing context remain explicit with a next step. No
additional summary file is produced, and a document that already meets the
requirements stays unchanged. Clear prose can still receive a source-backed factual
correction.

This utility improves existing documentation, PR drafts and issue descriptions,
saving results locally. It does not change code or configuration, publish externally, or edit
agent/skill instructions. An explicit `AGENTS.md`, `CLAUDE.md` or `SKILL.md` target receives a suggestion to use
`/kk:implement`, with no edit or automatic handoff. Generic requests for shorter
chat answers do not activate it.

The final comprehension and fidelity check runs in the editing session. Normal
project review remains the caller's responsibility; the skill does not provide
independent runtime verification or a guarantee of improved human comprehension.

### Optional clarification after drafting

`/kk:design` and `/kk:document` suggest `/kk:clarify-docs` after creating or materially
revising documents, naming the relevant paths. You decide whether to run it. Neither
writing skill loads the clarification procedure or applies a separate editorial
pass automatically. Both remain responsible for clear, accurate drafts and their
required content.

| Entry point | Recommendation and review boundary |
| --- | --- |
| `/kk:design` for a fresh idea | Suggests clarification of all created design, implementation and task documents, including split parts, before recommending `/kk:review-design`. Neither follow-up runs automatically. |
| `/kk:design` resuming WIP | Suggests clarification of only materially refined documents before recommending review and handing off. An unchanged resume does not rewrite documents or suggest clarification. |
| `/kk:document` | Suggests clarification of created or materially revised outputs; no suggestion when there are none. Project-prescribed review remains separate. |
| `/kk:implement` plan mode | Calls `/kk:document` when the whole plan completes, which may suggest clarification. It runs no automatic clarification pass; individual tasks do not trigger this completion call. |
| `/kk:implement` standalone mode | No automatic documentation completion call. Invoke `/kk:document` to update documentation or `/kk:clarify-docs` to edit existing prose explicitly. |

For example, `/kk:design` refining only `implementation.md` suggests clarification
of that path, leaving the linked design outside the suggested edit scope. Clarification
improves the explanation; `/kk:review-design` evaluates the design. If you choose both,
clarify first so the review assesses the final wording. The standalone clarification
skill's fidelity check remains in-session, not independent verification.

### Clarify a PR draft

Use `/kk:clarify-docs pr-draft.md for repository reviewers` to edit a local draft
in place. Supply the PR or base/head context and any relevant requirements. The
skill checks the actual review diff and source before explaining what this increment
delivers, which files deserve attention and what validation supports it. A contract
change is described separately from future runtime integration.
The draft identifies newly added tests and records validation outcomes and limits;
those details belong in the draft, even when the completion message reports them.

Use `/kk:clarify-docs <PR URL>; save to docs/feat/wip/import/pr-draft.md` to obtain
a PR body through read-only tools and produce a local draft. Pasted bodies work
the same way. Without a supplied destination, the skill names a draft under the
clearly established current feature directory; if neither is clear, it asks before
writing. Unrelated existing files are never overwritten. Missing source access
stays explicit and limits what the draft claims. No PR update, comment or message
is sent by this workflow.

Declare the intended audience and any private sources. Explicit restrictions take
precedence even for tracked files. Otherwise, files tracked at the PR head can be
referenced for that repository's review audience, including shared task documents.
External references need evidence that the audience can access them; the editor's
credentials alone are insufficient. Private context may help explain the work,
but removing its citation does not make its facts shareable. The skill uses an
accessible source or an explicitly authorized explanation, or retains a limitation.

Destination drafts, shared reports and gap notes exclude absolute workspace paths
and private source pointers. A completion message visible only to you may use an
absolute link to the selected local output so you can open it. That exception does
not authorize sharing private source paths or facts.

### Clarify an issue description

Use `/kk:clarify-docs` to explain an existing bug report, feature request or other
issue for its intended readers. Select the description and any known audience,
requirements or source references:

- Local draft: `/kk:clarify-docs issue-draft.md; preserve the reported reproduction details`.
- Issue URL: `/kk:clarify-docs <GitHub or Linear issue URL>; save to docs/feat/wip/import/issue-draft.md`.
- Pasted description: `/kk:clarify-docs the issue description pasted below; save to drafts/import-issue.md`, followed by the body.

The selected local draft is edited in place. Remote and pasted bodies become one
local draft at your destination, or an unused path within a clearly established
feature directory. Without either, the skill inspects available context and asks
where to save before writing. A captured body is input, not permission to overwrite
that file; unrelated existing drafts are protected. GitHub and Linear are examples:
the skill uses available read-only tools or supplied text and requires no particular
tracker integration. It sends no issue updates, comments or messages.

Bug reports retain reproduction steps, commands, environment/version details and
expected versus observed results. Reported behavior stays distinct from verified
behavior, including differences between the reported version and inspected source.
Feature requests preserve accepted intent, proposals, existing acceptance criteria
and open decisions. Future implementation and a PR diff are not prerequisites.
Missing decisions or criteria remain unknown with a next step and a known or
explicitly unknown owner where relevant. The skill neither invents criteria nor
executes reproduction commands. Tracker titles and types are read-only context;
supplied titles stay unchanged, with no replacement-title suggestions.

If the body is inaccessible, the skill requests its text or an accessible source
without writing a purported revision. If only supporting evidence is unavailable,
it can still clarify the supplied body while preserving verification limits.
Conflicting requirements and source remain explicit with a next action.

For a GitHub issue in repository R, the default readers are R's issue audience
unless you specify another audience. Files tracked in R at the inspected revision
are presumed accessible to those readers, including in a private repository;
the default branch supplies the revision when none is established. This does not
verify behavior in an older reported version. Explicit restrictions override that
presumption, even for tracked files. Another audience, repository or tracker needs
evidence of sharing; a Linear link or the editor's credentials alone does not prove
access. Restricted facts and pointers stay out of both the draft and shared report,
including uncited paraphrases. The caller-only output-link exception described
above applies only to the selected local draft.

Requests to implement, fix or work on an issue use `/kk:implement`; an issue URL
alone does not request description editing. Clarification remains a separate,
optional action after drafting, with the same in-session fidelity check and normal
project review described above.
