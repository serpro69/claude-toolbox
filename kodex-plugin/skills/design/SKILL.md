---
name: design
description: |
  TRIGGER when: asked to write or refine a technical design, PRD, specification, implementation plan, or task list, or resume an existing docs/feat/wip feature.
  Turns ideas and requirements into written design documents, implementation plans, and tasks in docs/feat/wip/ before coding. For conversational exploration without written planning, use $kk:brainstorm.
---
<!-- codex: tool-name mapping applied. See .codex/scripts/session-start.sh -->

# Task Analysis Process

**Goal: Before writing any code, make sure you understand the requirements and have an implementation plan ready.**

## Conventions

- **Read capy knowledge base conventions** at [shared-capy-knowledge-protocol.md](shared-capy-knowledge-protocol.md).
- **Read profile detection** at [shared-profile-detection.md](shared-profile-detection.md). When an active profile contributes a `design/` subdirectory (e.g., `../../profiles/k8s/design/`), its `questions.md` feeds the idea-refinement question pool and its `sections.md` lists required sections the design document must cover. Both the idea-to-design and continue-WIP flows consult the shared procedure; see each flow's workflow file for the specific integration points.

For fresh ideas, two reference files provide methodology and evaluation rubric: [shared-ideation-frameworks.md](shared-ideation-frameworks.md) (ideation lenses for the diverge phase) and [shared-idea-refinement-criteria.md](shared-idea-refinement-criteria.md) (evaluation dimensions and MVP scoping for the converge phase). These are loaded during the instruction-load step and consumed by idea-process.md Step 3 sub-phases.

## Workflow

**Mandatory order — understanding before engagement.** The flow below is strictly sequential. Do not engage with idea prose beyond a keyword scan, read WIP document content, ask refinement questions, or write design content until all instructions — this SKILL.md, the relevant process file, the shared protocols, every resolved profile's `design/` content, and the fresh-idea references below (when applicable) — are fully loaded. Bounded signal inspection for profile detection is the only content-read exception.

The `$kk:design` skill has two entry points; each has its own process file with a detailed workflow. Both follow the same mandatory ordering:

1. **Keyword scan only.** The idea prose (or WIP feature directory) is scanned at the keyword/filename level — enough to drive profile detection, not enough to engage with the content.
2. **Load instructions.** Read the relevant process file ([idea-process.md](./idea-process.md) or [existing-task-process.md](./existing-task-process.md)), the shared protocols above and [example-tasks.md](./example-tasks.md) (task format), even on an unchanged resume.
  - For WIP, also load the drafting guidelines in idea-process.md for potential refinement, without running its fresh-idea sub-phases.
  - For fresh ideas, also read [shared-ideation-frameworks.md](shared-ideation-frameworks.md) (ideation lenses) and [shared-idea-refinement-criteria.md](shared-idea-refinement-criteria.md) (evaluation rubric).
3. **Detect active profiles.** Delegate to [shared-profile-detection.md](shared-profile-detection.md). For fresh ideas, this uses the design interaction pattern (token matching against idea prose). For WIP features, this uses file-based detection with design-pattern fallback.
4. **Load profile content.** For each active profile contributing a `design/` subdirectory, read its `index.md` and all always-load and matching conditional entries. These feed the refinement question pool and required design sections.
5. **Engage with subject matter.** Follow the selected process file's content-reading, refinement and drafting steps.
6. **Recommend next steps.** After drafting or substantive refinement, suggest an optional `$kk:clarify-docs` invocation naming the created or materially revised documents, before the `$kk:review-design` recommendation. An unchanged resume skips the clarification suggestion. Follow the selected process file for review recommendation and implementation handoff.

Clarification is a separate user-selected editing workflow: this skill neither loads its procedure nor runs it automatically. Drafting still owns clear explanations and preservation of required sections, profile topics, decisions, task state and links. A clarification suggestion does not replace design review; neither recommendation executes a review or establishes independent verification.

## Ideas and Prototypes

_Use this to develop an idea into a written design/specification and implementation plan._

**For example:** Help me turn this idea into a written design, implementation plan, and task list before we start coding.

**Your job:** Help me turn it into a fully formed design, spec, implementation plan, and task list.

See [idea-process.md](./idea-process.md).

## Continue WIP Feature

_Use this to resume work on a feature that already has design docs and a task list in `/docs/feat/wip/`._

**For example:** Let's continue working on the auth system.

**Your job:** Review the current state of the feature, understand what's been done and what's next, then proceed with implementation.

See [existing-task-process.md](./existing-task-process.md).
