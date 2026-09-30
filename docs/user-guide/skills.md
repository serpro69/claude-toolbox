# Skills

The kk plugin ships 14 workflow and utility skills, including a complete development pipeline.

## The Pipeline

```
/kk:design → /kk:review-design → /kk:implement → /kk:review-code → /kk:test → /kk:document
```

1. **/kk:design** — turns an idea into design docs, an implementation plan, and a task list
2. **/kk:review-design** — evaluates design docs for completeness and technical soundness
3. **/kk:implement** — executes tasks with review checkpoints between batches
4. **/kk:review-code** — reviews code for SOLID violations, security risks, and quality issues
5. **/kk:test** — generates tests and runs the full suite
6. **/kk:document** — updates architecture docs and records ADRs

## Skill Reference

| Skill | What it does |
|-------|-------------|
| **/kk:design** | Turns an idea into design docs, an implementation plan, and a task list in `docs/feat/wip/`. Asks refinement questions, then documents everything a developer needs to start coding. |
| **/kk:implement** | Executes a task list from `docs/feat/wip/` with batched steps and code review checkpoints between batches. Updates task status as it goes. |
| **/kk:test** | Generates tests following project conventions: table-driven, integration, mocking, property-based. Runs the full suite and reports coverage. |
| **/kk:document**  | Updates project documentation and records ADRs for non-obvious decisions made during implementation.                                                                     |
| **/kk:review-code** | Reviews git changes for SOLID violations, security risks, and code quality. Domain-specific checklists for Go, Java, JS/TS, Kotlin, Python, Kubernetes, K8s Operator, and agent skills. Standard and isolated modes. |
| **/kk:review-design** | Pre-implementation review gate. Evaluates design docs for completeness, internal consistency, and technical soundness before code is written. |
| **/kk:review-spec** | Compares implemented code against design/implementation docs. Finds spec deviations, missing implementations, and outdated docs — in both directions. |
| **/kk:model** | Produces or updates a domain-reference kit — a durable glossary + divergences/traps page pair per bounded context, with concept-to-code bindings. Its primary output is a decision queue of precise, role-tagged questions only a human can close. Runs upstream of `/kk:design` as the first producer of the architecture flow. |
| **/kk:review-architecture** | Reviews a written architecture artifact (ADR, architecture doc, a design doc's architecture section, or a domain-reference kit — glossary + traps pages reviewed as one composite artifact) against the system it describes. Claim-driven: extracts an inspectable claim-set, verifies mechanism existence/topology across seven dimensions, and grades decision soundness, reversibility, and provenance (self-certification of reverse-engineered claims). Security architecture is delegated to PAL `secaudit`. |
| **/kk:dependency-handling** | Fires before calling a library/SDK/API or adding a dependency. Forces a capy/context7 lookup instead of guessing signatures or behavior. |
| **/kk:diff-skill** | Compares two versions of a skill's markdown instructions to detect degradations and complexity increases. Asymmetric — only regressions count. |
| **/kk:merge-docs** | Merges two competing design docs for the same feature into one unified document, resolving conflicts and preserving the best of both. |
| **/kk:clarify-docs** | Improves selected documentation and PR drafts after understanding requirements and source. Produces local edits, preserves meaning and respects the intended audience's access. |
| **/kk:chain-of-verification** | Makes Claude fact-check its own answers. Standard mode (prompt-based) or isolated mode (independent sub-agents). For high-stakes accuracy. |

## Commands

Commands are skill variants invoked with explicit mode selection:

| Command | Invocation | Description |
|---------|-----------|-------------|
| Code Review (isolated) | `/kk:review-code:isolated` | SOLID code review with independent sub-agents |
| CoVe (standard) | `/kk:chain-of-verification:default [question]` | Chain-of-Verification with prompt-based isolation |
| CoVe (isolated) | `/kk:chain-of-verification:isolated [--explore] [--haiku] [question]` | CoVe with true sub-agent isolation |
| Spec Review | `/kk:review-spec:default [feature]` | Verify code matches design/implementation docs |
| Spec Review (isolated) | `/kk:review-spec:isolated [feature]` | Spec conformance review with independent sub-agent |
| Template Sync | `/kk:template:sync [--version vX.Y.Z] [--dry-run]` | Sync repo with upstream template |

## Utility Skills

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

This utility improves existing documentation and PR-description drafts, saving results
locally. It does not change code or configuration, publish externally, or edit
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
