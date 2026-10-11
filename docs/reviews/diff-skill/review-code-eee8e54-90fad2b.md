# diff-skill: review-code (eee8e54e → 90fad2be)

## Summary

**Recommendation: keep both commits; restore one small deletion-planning instruction.** The functional-review method was preserved, and the refactor improves consistency independently of the model. It is not literally lossless: `59581e1c` drops the explicit requirement to supply verification checkpoints for warranted removals. That warrants a small follow-up, not reverting the instruction packaging, scenario reporting, or clean-review closure changes.

**Code-review assessment: COMMENT.** P0: 0; P1: 0; P2: 0; P3: 1. **Strict instruction-diff verdict: Degraded**, narrowly: 1 minor instruction degradation, 0 substantiated complexity regressions. The categorical diff verdict is a preservation check, not a recommendation to revert the overall change.

Reviewed on 2026-10-11 using `/kk:review-code` and `/kk:diff-skill`. Comparison: `eee8e54e` (parent of `59581e1c`) → `59581e1c` → `90fad2be`. These are the requested commits, not a comparison with the feature's much earlier evaluation baseline. The working tree initially had no reported changes. No operative source or historical evaluation evidence was edited, and no new model evaluations were launched.

The feature's two principal skills are `/kk:review-code` and `/kk:implement`. Only `/kk:review-code` is directly rewritten in these commits. `/kk:implement` inherits the additive shared packet-read option; its entry point and both mode procedures are unchanged. `/kk:review-spec` was also checked as a shared-protocol consumer. See the companion [implementation-skill report](implement-eee8e54-90fad2b.md) and [spec-review report](review-spec-eee8e54-90fad2b.md).

## Degradations

### P3 — Preserve verification checkpoints for justified removal recommendations

**Location:** [review-process.md:71](../../../klaude-plugin/skills/review-code/review-process.md#L71). Introduced in `59581e1c`; retained in `90fad2be`.

**Before:** the generic removal rule required reviewers to “provide concrete follow-up steps with checkpoints (tests/metrics).”

**After:** the replacement correctly requires a demonstrated current cost or defect, preserves required behavior, protects pending scaffolding, and retains “safe delete now” versus “defer with plan.” It omits the explicit steps/checkpoints requirement.

**Why this is a loss:** when a justified removal is recommended on a diff without a removal-plan profile, the reviewer no longer has a direct requirement to explain how to validate that deletion. For example, a shell-script review can propose deleting a demonstrably redundant implementation without naming a smoke check. The generic findings template asks for a suggested fix, but does not require a validation checkpoint for it. This concerns a warranted recommendation, not speculative cleanup or a clean review.

**Mitigating coverage:** programming-language and Kubernetes profiles retain their removal-plan templates. Shared change context also retains verification conditions for materially deferred work, and the functional method requires checking proposed corrections against invariants. These make the gap small; they do not universally restore the removed reporting requirement, particularly for immediate removal recommendations without a relevant template.

**Minimal repair:** append to the new removal rule: “For warranted removals, provide concrete steps and proportionate validation checkpoints.” Keep the new evidence threshold and pending-work protection.

**Profile:** skill-md · **Checklist:** skill-quality-checklist.md · **Trigger:** SKILL.md / nearest skill-root adjacency. **Confidence:** 95% in the textual omission; its effect on any particular model is unmeasured. This is nonblocking instruction preservation feedback, not a demonstrated unsafe deletion.

## Neutral Changes and Improvements

| Obligation or behavior | Before → after | Assessment |
| --- | --- | --- |
| Establish intent and requirement authority; preserve invariants | Retained in shared change context, the functional method and investigation phase | Preserved |
| Trace changed paths through unchanged consumers; examine failure, retry, intermediate and final states | Retained; now tied to a compact contract/source → state → transition → expected/actual → evidence record | Improved traceability; no fixture-specific answer added |
| Historical source and provenance | Shared context, isolated handoff and PAL protocol retain actual-source, baseline identity and missing-evidence requirements | Preserved |
| Compatibility and delivery assessment | Supported / Blocked / Unknown / Not applicable, independent-delivery constraints, inherited-defect attribution and qualified verdicts remain | Preserved |
| Profile detection | Same Known profiles, authoritative signals, bounded routing, conservative conditional loading and returned-content requirements | Preserved; packet packaging does not replace detection |
| Instruction loading | Complete original bodies can arrive in bounded packets; indexes, load/skip decisions and always-load membership are checked | Useful structural improvement; no instruction summarization |
| No-profile review | Common methodology remains required; domain guidance is not fabricated | Preserved, with an added negative-control eval |
| Python/helper unavailable or unsupported packaging | Direct reads remain available with the same scope and completion rules | Preserved fallback |
| Task scope versus Git selection | Early Git metadata selection is explicitly separated from later task-document investigation | Clearer ordering; requirements still get read |
| SOLID, security, quality and self-check | Category guidance, severity, confidence and false-positive self-check remain | Preserved |
| Removal recommendations | Evidence threshold and pending-scaffold protection are strengthened | Improvement, subject to the small checkpoints omission above |
| Clean-review closure | Unconditional next-step confirmation/menu removed; scoped verdict and coverage can finish the review | Improvement: completion no longer manufactures work |
| Real defects and required evidence | Supported action remains reportable; material unknowns and unmet hard requirements still prevent unconditional approval | Preserved |
| Existing implementation authorization | A caller's authorized fixes can proceed without redundant confirmation; review-only work still does not authorize edits | Improved consistency |
| Isolated review | Independent evidence, equivalent source/criteria, additional-source requests, native PAL findings, coverage disclosure and annotation rules remain | Preserved |
| Knowledge indexing | Systemic P0/P1 indexing remains required | Preserved |

The narrower recommendation language is not a blanket prohibition on maintainability improvements. The unchanged SOLID paragraph still asks reviewers to explain cohesion/coupling improvements and outline a minimal safe split. The functional method still asks reviewers to challenge complexity by identifying its cost and a simpler behavior-preserving alternative. The new language removes unsupported suggestions, not these evidence-backed review responsibilities.

The scenario-record change removes the sentence about avoiding exhaustive category enumeration, but proportionality survives: small changes may use one sentence, compatibility assessment selects relevant combinations rather than a Cartesian product, and source expansion stops once the identified contract question is resolved. I do not classify that rewording as a separate loss.

## Complexity Assessment

The packet mechanism adds a 161-line helper, a 45-line procedure and a new preparation route. `/kk:review-code`'s reachable Markdown grows from 9 files / 74,809 bytes to 10 files / 81,366 bytes, counting linked shared files through their skill paths. That is real maintenance overhead; it is not a reduction in instruction volume.

It buys fewer separate instruction-navigation calls and mechanical checks that every index entry has a decision and every always-load entry is selected. Detection predicates remain in their authoritative prose; they were not duplicated in Python. Packets preserve original source bodies, source locations and hashes, and retain a direct-read fallback. These properties justify the added mechanism. I found no introduced contradiction or lost review responsibility that warrants classifying the packaging itself as a complexity regression.

The helper validates packaging and membership only. It does not prove the actor understood the instructions, made the right predicate decisions, or waited before investigating. Both the code and prose explicitly say this. The remaining ordering failures are therefore an observed limit of the mechanism, not evidence that the method was weakened. The separate ordering-hook proposal is not implemented by these commits and is not needed to decide whether to retain their operative instruction improvements.

## Commit-Level Recommendation

- **`59581e1c`: keep.** The packet mechanism preserves instruction content and strengthens structural completeness; the scenario record ties coverage to actual requirements. Restore the generic removal-validation sentence. Added capture infrastructure and retained evidence make a wholesale revert broader than an instruction rollback.
- **`90fad2be`: keep.** Clean-review closure resolves the conflict between “recommend only substantiated work” and an obligatory remediation menu. The task-scope timing clarification reinforces an existing ordering requirement. Neither change weakens hard requirements, evidence limits or review-only authorization boundaries.

## Model Selection and Evaluation Limits

The current [project setting](../../../.claude/settings.json) selects `claude-opus-5-5`, but [the successor capture runner](../../feat/wip/functional-review/verification/task12/rework/capture.py#L52) explicitly constructs `--model claude-opus-4-8[1m]`. The driver calls that runner. Reusing it does not automatically inherit the new project model setting. The retained candidate-6 launch metadata also records the old model.

This is an operational observation for the next evaluation, not a newly introduced instruction defect: the historical runs deliberately pinned the old actor configuration. Preserve those records. A new comparison needs a separately declared/frozen runner configuration with the intended model, and verification of actual parent/reviewer model identity.

The retained [candidate-5 results](../../feat/wip/functional-review/verification/task12/candidate5/results.md) report 37 PASS / 3 FAIL; [candidate-6 results](../../feat/wip/functional-review/verification/task12/candidate6/results.md) report 11 PASS / 1 FAIL for R5. They are development measurements with incomplete gates, not proof of general reliability. Both compare against the earlier `c2d28c9e` baseline, not directly against `eee8e54e`. Their totals cannot isolate the effect of these two commits, and they do not show that changing the model would eliminate the remaining failures.

For this keep/revert decision, the stronger evidence is the instruction comparison: the changes have model-independent reasons to exist. A model upgrade is a reason to rerun the comparison, not by itself a reason to revert the refactor.

## Scope, Verification and Evidence Limits

- Walked both `/kk:review-code` instruction graphs from SKILL.md using Git blobs, resolving symlinks at each revision and ignoring fenced examples/external links. Compared the intermediate commit too. No reachable Markdown file was removed, and there are no missing Markdown-link targets on either side.
- Compared the complete reachable `/kk:implement` and `/kk:review-spec` instruction sets, reading unchanged shared text once. Reviewed changed canonical instruction bodies, the packet helper, its tests and two added eval definitions. Checked relevant feature requirements and retained result summaries. This is not a line-by-line audit of thousands of archived event/evidence files or all capture-lifecycle code.
- Active review profiles: skill-md and python. Loaded universal/provider/plugin skill checklists and Python security, SOLID, quality and removal guidance. Other known profile signals do not apply to these operative targets. Supplemental profile-index inspection checked packaging membership, not Kubernetes behavior.
- `bash test/test-review-instructions.sh`: all 9 packet tests passed.
- Packet index/source check: all 38 entries across all 7 populated Known-profile review-code indexes matched and their source bodies were available. `k8s-operator` lacks this phase in both revisions; that is not introduced by these commits.
- `bash test/test-plugin-structure.sh`: 223 assertions passed.
- `make plugin-graph`: Go tests and broken-edge/orphan validation passed. The existing graph cycle warning remains.
- `make generate-kodex`: passed in a disposable export using Python 3.12, including generator tests, plugin structure and 29 Codex-structure assertions. All 902 tracked generated entries matched `90fad2be` byte-for-byte. Initial attempts hit missing export metadata and then the host Python 3.10's missing TOML parser; completing the export and selecting the already-installed Python 3.12 resolved those setup failures without source edits.
- No live model eval, PAL call or new behavioral-acceptance claim. Confidence is high in the preservation comparison and moderate in predicting improved compliance across models.

No P0/P1 systemic findings to index. The minor instruction-preservation pattern is eligible for `/kk:diff-skill` knowledge indexing. Recommended source follow-up remains review feedback; it has not been applied.

## Post-review Fix Status

The user subsequently authorized both fixes. On 2026-10-11, the working tree restored the removal-validation sentence and regenerated the Codex counterpart. The successor capture runner now pins `claude-opus-5-5` for the main actor and subagents, updates prepared launch metadata consistently, and preserves historical evidence. See the [runner follow-up record](../../feat/wip/functional-review/verification/task12/rework/README.md). The commit-range assessment above remains a record of the originally reviewed revisions.
