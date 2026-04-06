# Tasks: design-review Skill

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Status: pending
> Created: 2026-04-06

## Task 1: Create the SKILL.md entry point
- **Status:** pending
- **Depends on:** —
- **Docs:** [implementation.md#skillmd--skill-entry-point](./implementation.md#skillmd--skill-entry-point)

### Subtasks
- [ ] 1.1 Create `klaude-plugin/skills/design-review/SKILL.md` with frontmatter (`name: design-review`, description) following the pattern of `solid-code-review/SKILL.md`
- [ ] 1.2 Add Overview section — one paragraph describing purpose as pre-implementation review gate
- [ ] 1.3 Add Review Modes section — standard and isolated, with brief descriptions and links to `review-process.md` and `review-isolated.md`
- [ ] 1.4 Add Finding Types table — the 6-type taxonomy (INCOMPLETE, INCONSISTENT, TECH_RISK, MISSING, AMBIGUOUS, STRUCTURE) from design.md
- [ ] 1.5 Add Severity Levels table — P0-P3 adapted for design review
- [ ] 1.6 Add Workflow section — phase list with link to `review-process.md`
- [ ] 1.7 Add Invocation section — command examples for both modes with scope argument explanation and examples

## Task 2: Create the standard mode workflow
- **Status:** pending
- **Depends on:** Task 1
- **Docs:** [implementation.md#review-processmd--standard-mode-workflow](./implementation.md#review-processmd--standard-mode-workflow)

### Subtasks
- [ ] 2.1 Create `klaude-plugin/skills/design-review/review-process.md` with the capy knowledge base convention reference and progress checklist
- [ ] 2.2 Implement Step 1 (Load documents) — argument parsing, scope resolution logic (none/design/implementation/tasks/all), feature directory lookup, graceful handling of missing docs
- [ ] 2.3 Implement Step 2 (Capy search) — search `kk:arch-decisions` and `kk:review-findings` for prior context
- [ ] 2.4 Implement Step 3 (Document quality review) — completeness, clarity, internal consistency, cross-document consistency, convention adherence, subtask quality checks
- [ ] 2.5 Implement Step 4 (Technical soundness review) — viability, edge cases, trade-offs, scalability, testing strategy, migration/rollback, codebase cross-reference
- [ ] 2.6 Implement Step 5 (Self-check and confidence assessment) — re-read, question assumptions, assign confidence, drop unsubstantiated findings
- [ ] 2.7 Implement Step 6 (Present findings) — output format template, next-steps prompt, capy index instruction for confirmed TECH_RISK findings

## Task 3: Create the isolated mode workflow
- **Status:** pending
- **Depends on:** Task 1, Task 4
- **Docs:** [implementation.md#review-isolatedmd--isolated-mode-workflow](./implementation.md#review-isolatedmd--isolated-mode-workflow)

### Subtasks
- [ ] 3.1 Create `klaude-plugin/skills/design-review/review-isolated.md` with the capy knowledge base convention reference and progress checklist
- [ ] 3.2 Implement Step 1 (Prepare artifacts) — read documents, resolve pal model via `listmodels`, prepare document content for pal
- [ ] 3.3 Implement Step 2 (Spawn reviewers) — sub-agent prompt template for `design-reviewer` (with document paths and scope), `pal codereview` call with document contents, parallel execution requirement, error handling (one fails, both fail, malformed output)
- [ ] 3.4 Implement Step 3 (Annotate findings) — duplicate merging with "corroborated" tagging, author context annotations, author-sourced findings, optional pal follow-up
- [ ] 3.5 Implement Step 4 (Present report) — report template organized by agreement level (corroborated/design-reviewer/pal/author-sourced), section omission rules, next-steps prompt

## Task 4: Create the design-reviewer sub-agent
- **Status:** pending
- **Depends on:** —
- **Docs:** [implementation.md#design-reviewer-agent-definition](./implementation.md#design-reviewer-agent-definition)

### Subtasks
- [ ] 4.1 Create `klaude-plugin/agents/design-reviewer.md` with frontmatter (`name: design-reviewer`, description, tools allowlist: Read, Grep, Glob, capy_search)
- [ ] 4.2 Write identity section — independent reviewer, no authorship attachment, zero session context
- [ ] 4.3 Write "What You Receive" and "What You Do NOT Have" sections following `code-reviewer.md` pattern
- [ ] 4.4 Write Tool Access section — restricted allowlist, usage guidance for Read/Grep/Glob/capy_search
- [ ] 4.5 Write Finding Type Taxonomy table — 6-type taxonomy with codes, descriptions, examples
- [ ] 4.6 Write Severity Levels and Confidence Levels tables
- [ ] 4.7 Write Review Workflow — 7 steps: read docs, capy search, quality pass, soundness pass, cross-doc consistency, self-check, output findings
- [ ] 4.8 Write Output Format contract — structured markdown with P0-P3 grouping, finding type code, doc:section reference, confidence with reasoning, description, evidence, recommendation
- [ ] 4.9 Write Output Rules — mandatory fields, `(none)` for empty sections, no "next steps" section, overall assessment values (SOUND / CONCERNS_FOUND / MAJOR_GAPS)

## Task 5: Final verification
- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3, Task 4

### Subtasks
- [ ] 5.1 Run `testing-process` skill to verify all skill files are well-formed and consistent
- [ ] 5.2 Run `documentation-process` skill to update any relevant docs
- [ ] 5.3 Run `solid-code-review` skill to review the new skill files
- [ ] 5.4 Run `implementation-review` skill to verify implementation matches design and implementation docs
