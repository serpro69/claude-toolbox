---
name: review-code
description: |
  Code review of current git changes with an expert senior-engineer lens. Detects SOLID violations, security risks, and proposes actionable improvements.
  Use when performing code reviews.
---

# Code Review

## Overview

Review whether the current changes achieve their intended behavior, preserve affected contracts and meet applicable delivery constraints. Apply SOLID, architecture, security, quality and removal guidance alongside that reasoning. Default to review-only output unless the user asks to implement changes.

## Conventions

Load these through [packet-preparation.md](packet-preparation.md)'s preparation
sequence. It supplies complete original instruction text in fewer Read calls;
the direct-read fallback uses the same sources.

- **Read capy knowledge base conventions** at [shared-capy-knowledge-protocol.md](shared-capy-knowledge-protocol.md).
- **Always read change context** at [shared-change-context.md](shared-change-context.md) and the common method at [functional-review.md](functional-review.md), even when no profile matches.
- **Read task scope** at [shared-review-scope-protocol.md](shared-review-scope-protocol.md); pending work does not excuse regressions in current flows.
- **Read profile detection** at [shared-profile-detection.md](shared-profile-detection.md). Use its records to select and load domain guidance before investigation.

## Required Outputs

Before declaring the review complete, verify all outputs are delivered:

- [ ] Review report presented to user
- [ ] Intent, scope/baselines, inspected behavior, applicable compatibility conclusions and evidence limits reported
- [ ] P0/P1 systemic findings indexed as `kk:review-findings` (skip if no qualifying findings)
- [ ] Next steps confirmation from user

Indexing is owned by this skill — callers (e.g., `/kk:implement`) do NOT duplicate it.

## Review Modes

### Standard Mode (`/kk:review-code`)

Reviews code in the main conversation context. Fast, single-pass review using the workflow below.

### Isolated Mode (`/kk:review-code:isolated`)

Delegates detection to independent reviewers that did not write the code, then annotates their findings with author context. Two parallel reviewers: a `code-reviewer` sub-agent and `pal codereview` (external model in native format). Produces a report organized by agreement level with corroborated findings highlighted.

- **Cost**: Higher (sub-agent + external model + annotation)
- **Isolation**: True — reviewers have zero authorship bias or session context
- **Degradation**: Graceful — if one reviewer fails, proceeds with the other; if both fail, suggests standard mode fallback
- **Best for**: When extra rigor is worth the cost (pre-merge, high-stakes changes)

See [review-isolated.md](./review-isolated.md) for the isolated workflow.

## Severity Levels

| Level  | Name     | Description                                                      | Action                             |
| ------ | -------- | ---------------------------------------------------------------- | ---------------------------------- |
| **P0** | Critical | Demonstrated critical security, integrity or availability impact needing immediate mitigation | Must block merge                   |
| **P1** | High     | Logic error, significant SOLID violation, performance regression | Should fix before merge            |
| **P2** | Medium   | Code smell, maintainability concern, minor SOLID violation       | Fix in this PR or create follow-up |
| **P3** | Low      | Style, naming, minor suggestion                                  | Optional improvement               |

## Workflow

### Mandatory ordering — methodology before evidence

The standard workflow below is strictly sequential. **Load the process, shared protocols, common functional method and every resolved profile checklist before source investigation, `capy_search`, findings, edits or tests.** After basic process instructions load, the sole early-content exception is bounded inspection to resolve declared detection/conditional-load predicates: at most approximately 16 KiB per candidate file; log predicate/path, and conservatively load an instruction when its conditional is undecidable within the bound. No behavioral analysis or full-diff investigation is permitted during routing.

This ordering is load-bearing, not stylistic. Reviewing from a diff before loading profile checklists is the known failure mode this skill is designed to prevent: the LLM has enough from the diff to produce plausible findings, and optimizes away the methodology if the workflow permits.

**Phases** (same order as [review-process.md](./review-process.md)):

1. Prepare instruction packets — read [packet-preparation.md](packet-preparation.md), run the helper below for `bootstrap`, and Read every returned part; this loads process, shared protocols, common method and all known detection rules
2. Scope — resolve diff selection from status/filenames only
3. Detect profiles and route checklists — read and reconcile every known detection rule; filename/metadata signals, then bounded declared predicates; no deferred conditionals
4. Read every resolved checklist — build and Read the selected checklist packet; its manifest rejects missing index decisions and skipped always-load files. Confirm actual complete Read results before proceeding
5. Investigate — read available component contracts and establish context/task scope, then selected diff/current files; trace behavior and historical compatibility, and search relevant knowledge
6. Apply profile and general checklists to that behavior
7. Self-check findings and confidence through targeted verification
8. Index systemic P0/P1 findings as `kk:review-findings`
9. Present findings, coverage and evidence-qualified verdict
10. Confirm next steps
11. Verify required outputs

See [review-process.md](./review-process.md) for the detailed step-by-step process.

**Preparation helper:** execute [scripts/prepare_instructions.py](scripts/prepare_instructions.py)
with Python 3 using its resolved path. The installed path is
`${CLAUDE_PLUGIN_ROOT}/skills/review-code/scripts/prepare_instructions.py`.
The helper reads instructions only and prints packet paths. Creating a packet
does not load it: use Read on every part, including continuations, before source
investigation. If execution is unavailable, use the direct-read fallback.

## Invocation

Standard mode:

```
/kk:review-code
```

Isolated mode with independent sub-agents:

```
/kk:review-code:isolated
```
