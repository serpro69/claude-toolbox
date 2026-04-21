---
name: design
description: |
  Use in pre-implementation (idea-to-design) stages to understand spec/requirements and create a correct implementation plan before writing actual code.
  Turns ideas into a fully-formed PRD/design/specification and implementation-plan. Creates design docs and task lists in docs/wip/.
---

# Task Analysis Process

**Goal: Before writing any code, make sure you understand the requirements and have an implementation plan ready.**

## Conventions

Read capy knowledge base conventions at [shared-capy-knowledge-protocol.md](shared-capy-knowledge-protocol.md).

Profile detection is delegated to [shared-profile-detection.md](shared-profile-detection.md). When an active profile contributes a `design/` subdirectory (e.g., `${CLAUDE_PLUGIN_ROOT}/profiles/k8s/design/`), its `questions.md` feeds the idea-refinement question pool and its `sections.md` lists required sections the design document must cover. Both the idea-to-design and continue-WIP flows consult the shared procedure; see each flow's workflow file for the specific integration points.

## Ideas and Prototypes

_Use this for ideas that are not fully thought out and do not have a fully-formed design/specification and/or implementation-plan._

**For example:** I've got an idea I want to talk through with you before we proceed with the implementation.

**Your job:** Help me turn it into a fully formed design, spec, implementation plan, and task list.

See [idea-process.md](./idea-process.md).

## Continue WIP Feature

_Use this to resume work on a feature that already has design docs and a task list in `/docs/wip/`._

**For example:** Let's continue working on the auth system.

**Your job:** Review the current state of the feature, understand what's been done and what's next, then proceed with implementation.

See [existing-task-process.md](./existing-task-process.md).
