---
name: brainstorm
description: |
  TRIGGER when: asked to brainstorm, think through, explore, or pressure-test a technical idea or decision through conversation. Interviews adaptively, asks one question at a time, and closes with a chat recap.
  For technical products, architecture, infrastructure, tools, operations, and engineering workflows. Written design/specification and task-list requests belong to /kk:design; durable domain glossary/reference kits to /kk:model; implementation and fixes to /kk:implement. Not for nontechnical brainstorming.
---

# Brainstorm a Technical Idea

Help the user reach their next decision: pursue, discard, narrow, or investigate an idea. Match depth and vocabulary to their needs, whether they are a developer, architect, or anyone thinking through a technical topic. An implementation-ready specification is not required.

Keep the working context and result in the conversation. Research is read-only through project files and web sources; do not search knowledge stores or session vaults, index memory, create project files, saved notes, temporary interview artifacts or task records, or mutate external resources. This boundary covers the skill's actions, not the host application's transcript storage.

## Workflow

**Mandatory order — instructions before engagement.** The entry steps are strictly sequential: fully load this SKILL.md and both references below before researching project content, refining the idea, or asking interview questions. After loading, repeat the interview/research loop as needed, then close at sufficient clarity for the user's next decision.

1. **Load reasoning references.** Read [shared-ideation-frameworks.md](shared-ideation-frameworks.md) and [shared-idea-refinement-criteria.md](shared-idea-refinement-criteria.md). They supply lenses, not a mandatory questionnaire: apply relevant alternatives, constraint mapping, failure scenarios, and assumption audits. Product-market, adoption, differentiation, and MVP questions are context-dependent; omit them when they do not help the technical decision.

2. **Establish the current decision.** Use the idea and context already supplied. Ask a framing question only to resolve a real ambiguity about the problem or next decision; no ceremonial confirmation, persona interview, or numerical success metric is required. If the requested output is ambiguous between conversation and a written artifact, clarify that output before assuming permission to create anything.

3. **Interview and investigate.** Keep settled decisions, assumptions, open questions, and their dependencies in conversational context.
   - Ask one question at a time: the highest-value question whose prerequisites are understood. Prefer meaningful choices when useful; explain a recommendation when evidence supports one. Use open questions when choices would bias the answer.
   - Challenge contradictions and weak assumptions directly and constructively. Explore relevant alternatives and their costs rather than endorsing the first proposal. When a premise changes, reopen the affected conclusions while preserving unrelated settled decisions.
   - Read relevant project files, documentation, or web sources when evidence could change the advice. Target the current uncertainty; a repository and an initial broad inspection are not prerequisites. Research a discoverable fact instead of asking the user to repeat it. Distinguish observed evidence, assumptions, recommendations, and user decisions. When evidence is unavailable, state the uncertainty and its effect on the decision; continue useful discussion that does not depend on it.

4. **Converge and close in chat.** Stop when the idea, rationale, meaningful trade-offs, material uncertainties, and next decision are clear enough. Do not exhaust every branch or turn a blocking unknown into a premature recommendation to build. Recap settled decisions with their rationale, open assumptions that could change direction, details that can wait, and the next decision or investigation. If the user stops early, give a truthful partial recap without further interrogation or claiming the idea is validated.

Written planning may be a useful next step: suggest `/kk:design` when appropriate, but do not load or invoke it, begin implementation, or create artifacts automatically. A later user request to write or build starts that workflow. The recap supplies context for its confirmations; it does not waive `/kk:design`'s gates or prevent decisions from being revisited.

## Inspiration

The prerequisite-aware interview and separation of researched facts from user decisions draw on [Matt Pocock's grilling skill, pinned at `85f83d3`](https://github.com/mattpocock/skills/blob/85f83d3fde1d3a90d5c9a657f6998c79a6c37308/skills/productivity/grilling/SKILL.md). This workflow adapts those ideas to one question at a time and decision-level closure; the source is attribution, not a runtime instruction dependency.
