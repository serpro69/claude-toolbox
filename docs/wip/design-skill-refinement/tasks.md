# Tasks: Design Skill Refinement

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Status: pending
> Created: 2026-05-21
> Not Doing: existing-task-process.md changes, implement skill changes, pal-based stress-testing, Mermaid graphs, design skill evals, skill-md profile design/ subdirectory

## Task 1: Create frameworks.md reference file
- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** Task 2
- **Docs:** [implementation.md#task-11-create-frameworksmd](./implementation.md#task-11-create-frameworksmd)

### Subtasks
- [ ] 1.1 Fetch original from capy source `idea-refine-frameworks` (or re-fetch from `https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/idea-refine/frameworks.md`)
- [ ] 1.2 Create `klaude-plugin/skills/design/frameworks.md` with all six frameworks (SCAMPER, HMW, First Principles, JTBD, Pre-mortem, Constraint Mapping), each with description and "Best for" guidance
- [ ] 1.3 Light adaptation: add SE-context framing note at top, replace consumer-product examples with SE equivalents, preserve structure and quality criteria

## Task 2: Create refinement-criteria.md reference file
- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** Task 1
- **Docs:** [implementation.md#task-12-create-refinement-criteriamd](./implementation.md#task-12-create-refinement-criteriamd)

### Subtasks
- [ ] 2.1 Fetch original from capy source `idea-refine-criteria` (or re-fetch from `https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/idea-refine/refinement-criteria.md`)
- [ ] 2.2 Create `klaude-plugin/skills/design/refinement-criteria.md` with three evaluation dimensions (User Value, Feasibility, Differentiation) plus MVP Scoping section
- [ ] 2.3 Light adaptation: add SE-context framing, remove consumer examples, preserve painkiller-vs-vitamin framing, differentiation ranking, value/feasibility matrix, and MVP rules

## Task 3: Rewrite idea-process.md Step 3
- **Status:** pending
- **Depends on:** Task 1, Task 2
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#task-21-rewrite-idea-processmd-step-3](./implementation.md#task-21-rewrite-idea-processmd-step-3)

### Subtasks
- [ ] 3.1 Replace current Step 3 body in `klaude-plugin/skills/design/idea-process.md` with five sub-phases (3a-3e)
- [ ] 3.2 Preserve the profile detection block in its current position (before questions begin)
- [ ] 3.3 Add instruction to read frameworks.md and refinement-criteria.md at the start of Step 3
- [ ] 3.4 Write sub-phase 3a (HMW framing) with reference to frameworks.md §HMW
- [ ] 3.5 Write sub-phase 3b (hard gate) with three explicit requirements: who, success, technical constraints
- [ ] 3.6 Write sub-phase 3c (proportional diverge) with two paths: non-trivial (2-3 alternatives) and simple (direct + one alternative)
- [ ] 3.7 Write sub-phase 3d (CoVe-assisted converge) with `/kk:chain-of-verification:isolated` invocation, complexity evaluation, and user confirmation gate
- [ ] 3.8 Write sub-phase 3e (surface outputs) requiring Assumptions and Not Doing artifacts

## Task 4: Update idea-process.md Steps 5 and 6
- **Status:** pending
- **Depends on:** Task 3
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#task-31-update-step-5-in-idea-processmd](./implementation.md#task-31-update-step-5-in-idea-processmd), [implementation.md#task-32-update-step-6-in-idea-processmd](./implementation.md#task-32-update-step-6-in-idea-processmd)

### Subtasks
- [ ] 4.1 Add Assumptions and Not Doing section requirements to Step 5's documentation guidelines (before the DO NOT list)
- [ ] 4.2 Add Not Doing header requirement to Step 6's key points
- [ ] 4.3 Add vertical slicing mandate with explicit anti-pattern to Step 6
- [ ] 4.4 Add Size tags (S/M/L) with L-forbidden rule to Step 6
- [ ] 4.5 Add slicing strategy definitions (Vertical, Contract-First, Risk-First) to Step 6
- [ ] 4.6 Add parallel markers requirement to Step 6
- [ ] 4.7 Add ASCII dependency graph requirement to Step 6

## Task 5: Rework example-tasks.md
- **Status:** pending
- **Depends on:** Task 4
- **Size:** S
- **Can run in parallel with:** Task 6
- **Docs:** [implementation.md#task-41-rework-example-tasksmd](./implementation.md#task-41-rework-example-tasksmd)

### Subtasks
- [ ] 5.1 Add `> Not Doing:` line to the header metadata block with realistic JWT-auth exclusions
- [ ] 5.2 Add `**Size:**` and `**Can run in parallel with:**` fields to each task
- [ ] 5.3 Reslice tasks to demonstrate vertical slices (e.g., "User login end-to-end" instead of "Token generation library")
- [ ] 5.4 Add `## Dependency Graph` section at the bottom with ASCII format

## Task 6: Update SKILL.md conventions
- **Status:** pending
- **Depends on:** Task 3
- **Size:** S
- **Can run in parallel with:** Task 5
- **Docs:** [implementation.md#task-51-reference-new-files-in-skillmd](./implementation.md#task-51-reference-new-files-in-skillmd)

### Subtasks
- [ ] 6.1 Add sentence to `klaude-plugin/skills/design/SKILL.md` Conventions section mentioning frameworks.md and refinement-criteria.md as reference material used during Step 3

## Task 7: Update review-design review-process.md
- **Status:** pending
- **Depends on:** Task 4
- **Size:** S
- **Can run in parallel with:** Task 5, Task 6
- **Docs:** [implementation.md#task-61-update-review-processmd-steps-3-and-4](./implementation.md#task-61-update-review-processmd-steps-3-and-4)

### Subtasks
- [ ] 7.1 Add design.md checks to Step 3: Assumptions section (present, testable), Not Doing section (present, justified). Finding type: `STRUCTURE`
- [ ] 7.2 Add tasks.md checks to Step 3: Not Doing in header, Size tags, no unbroken L tasks, vertical slicing (flag horizontal layers as `TECH_RISK`), parallel markers, dependency graph. Finding types: `STRUCTURE` and `TECH_RISK`
- [ ] 7.3 Add to Step 4: assumptions testability check (vague → `AMBIGUOUS`), Not Doing validity check (disguised critical requirement → `TECH_RISK`)

## Task 8: Final verification
- **Status:** pending
- **Depends on:** Task 5, Task 6, Task 7
- **Size:** S
- **Can run in parallel with:** —

### Subtasks
- [ ] 8.1 Run `bash test/test-plugin-structure.sh` — all assertions green, new files do not cause failures
- [ ] 8.2 Run `/kk:test` skill to verify all tasks
- [ ] 8.3 Run `/kk:document` skill to update any relevant docs
- [ ] 8.4 Run `/kk:review-code` skill to review the implementation
- [ ] 8.5 Run `/kk:review-spec` skill to verify implementation matches design and implementation docs

## Dependency Graph

```
Task 1 ──→ Task 3 ──→ Task 4 ──→ Task 5 ──→ Task 8
Task 2 ──→ Task 3     Task 3 ──→ Task 6 ──→ Task 8
                       Task 4 ──→ Task 7 ──→ Task 8
```
