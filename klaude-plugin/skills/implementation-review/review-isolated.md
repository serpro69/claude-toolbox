### Workflow

For capy knowledge base conventions, see [capy-knowledge-protocol.md](../_shared/capy-knowledge-protocol.md).
For reconciliation rules, see [review-reconciliation-protocol.md](../_shared/review-reconciliation-protocol.md).

Copy this checklist and check off items as you complete them:

```
Isolated Implementation Review Progress:
- [ ] Step 1: Prepare artifacts
- [ ] Step 2: Spawn spec reviewer
- [ ] Step 3: Reconcile findings
- [ ] Step 4: Present consolidated report
```

---

## Step 1: Prepare Artifacts

### 1a) Locate feature directory

Find the feature directory in `/docs/wip/[feature]/`. If the user specified a feature name, use it directly. If invoked from `implementation-process`, the feature directory is already known.

### 1b) Verify docs exist

Confirm that the following files exist in the feature directory:
- `design.md` — feature design and architecture
- `implementation.md` — implementation plan with task-level details
- `tasks.md` — task statuses and subtask checklists

If any are missing, inform the user and stop.

### 1c) Determine review scope

Read `tasks.md` to classify each task:
- **Done**: task is completed and should be reviewed
- **Pending/In-progress**: task is not yet complete and should be skipped

Determine the review mode:
- **Mid-implementation**: some tasks are pending — review only completed tasks
- **Post-implementation**: all tasks are done — review everything

### 1d) Prepare sub-agent context

Collect the absolute paths to `design.md`, `implementation.md`, and `tasks.md`. The sub-agent reads these files itself — do NOT inline their contents into the prompt.

---

## Step 2: Spawn Spec Reviewer

Spawn a single `spec-reviewer` sub-agent using the Agent tool:

| Parameter | Value |
|---|---|
| `subagent_type` | `kk:spec-reviewer` |
| `description` | `Isolated spec conformance review` |
| `prompt` | See prompt template below |

**Sub-agent prompt template:**

```
You are reviewing the implementation of the "{feature_name}" feature against its specification. Apply your full review workflow.

## Feature Directory

{absolute path to /docs/wip/[feature]/}

## Documents

- Design: {absolute path to design.md}
- Implementation plan: {absolute path to implementation.md}
- Tasks: {absolute path to tasks.md}

## Review Scope

{mid-implementation | post-implementation}

Tasks to review: {list of completed task names/numbers}
Tasks to skip: {list of pending task names/numbers, or "none — all tasks complete"}

Read the documents yourself using the Read tool. Produce your findings in the output format specified in your agent definition.
```

This is a single sub-agent, not parallel. Wait for it to complete before proceeding.

---

## Step 3: Reconcile Findings

Follow the [review-reconciliation-protocol.md](../_shared/review-reconciliation-protocol.md) strictly, applying **type-specific trust levels** for spec conformance findings.

### 3a) Collect findings

Parse the `spec-reviewer` sub-agent's structured output (finding type, severity, confidence, spec-vs-code evidence).

### 3b) Apply type-specific trust levels

For each finding, the trust level depends on the finding type:

| Finding Type | Trust Level | Default disposition |
|---|---|---|
| `MISSING_IMPL` | **High trust** | Default to **Confirmed** unless you can point to the specific code that implements it |
| `AMBIGUOUS` | **High trust** | Default to **Confirmed** — the spec needs clarification even if you know what was intended |
| `DOC_INCON` | **High trust** | Default to **Confirmed** unless the cited sections do not actually contradict |
| `OUTDATED_DOC` | **High trust** | Default to **Confirmed** unless the doc already reflects current state |
| `SPEC_DEV` | **Medium trust** | Evaluate against session context. If intentional, use **Disputed — Intentional** and recommend a spec update |
| `EXTRA_IMPL` | **Medium trust** | Evaluate against session context. If intentional, use **Disputed — Intentional** and recommend a spec update |

### 3c) Assign dispositions

For every finding, assign exactly one disposition:

| Disposition | When to use |
|---|---|
| **Confirmed** | Finding is valid — code or docs need to change |
| **Disputed — Intentional** | Deviation was deliberate. You MUST state the specific reason AND recommend updating the spec to document it |
| **Disputed — False Positive** | Finding is incorrect. You MUST cite specific evidence |

**Invariants** — these are non-negotiable:
- Every finding MUST appear in the report with a disposition
- You MUST NOT add new findings
- Disputed findings still appear — the user decides

### 3d) Spec update suggestions

For any `SPEC_DEV` or `EXTRA_IMPL` finding with disposition **Disputed — Intentional**: draft a concrete suggestion for updating the spec (which doc, which section, what to change). The goal is to keep spec and code in sync even when the deviation is correct.

---

## Step 4: Present Consolidated Report

Use the consolidated report template from [review-reconciliation-protocol.md](../_shared/review-reconciliation-protocol.md), adapted for spec conformance findings.

### Report content

- **Reviewers**: `spec-reviewer (sub-agent)`
- **Feature**: feature name and directory
- **Review scope**: mid-implementation or post-implementation, with task list
- **Overall assessment**: CONFORMANT / DEVIATIONS_FOUND / MAJOR_GAPS
- **Findings**: grouped by effective severity (P0-P3), each with:
  - Finding type (`MISSING_IMPL`, `SPEC_DEV`, etc.)
  - Location (file:line vs doc:section)
  - Disposition and reasoning (if Disputed)
  - Confidence (1-10) with reasoning
  - "Spec says" vs "Code does" evidence
  - Spec update suggestion (if applicable)
- **Reconciliation summary table**: all findings with type, severity, disposition, and action
- **Doc issues**: `DOC_INCON` and `OUTDATED_DOC` findings requiring spec updates
- **Ambiguities**: `AMBIGUOUS` findings requiring spec clarification

### Integration with implementation-process

If this review is happening within `implementation-process`:
- Feed `MISSING_IMPL` and `SPEC_DEV` findings back as implementation tasks
- Feed `DOC_INCON`, `OUTDATED_DOC`, and `AMBIGUOUS` findings back as doc-update tasks
- Present the combined list for user confirmation before proceeding

### Standalone mode

If invoked standalone, present the report and ask the user how to proceed:

```markdown
---

## Next Steps

I found X findings (P0: ..., P1: ..., P2: ..., P3: ...).

**How would you like to proceed?**

1. **Fix all** — I'll address all confirmed findings (code fixes + doc updates)
2. **Fix P0/P1 only** — Address critical and high priority issues
3. **Fix specific items** — Tell me which findings to address
4. **Update docs only** — Apply spec update suggestions without code changes
5. **No changes** — Review complete, no changes needed

Please choose an option or provide specific instructions.
```

**Important**: Do NOT implement any changes until the user explicitly confirms.
