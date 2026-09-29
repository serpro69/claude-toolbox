# External review

Model: gemini-3.1-pro-preview. Continuation: 0c1cbd9d-ce15-4666-86d0-76dd334b6234.

The native external review follows. Its patch-capture observation refers to the initial incomplete temporary artifact; the complete 97-file patch was supplied in the continuation and used by the code reviewer. Task status remained in-progress while behavioral grading ran.

This is an exceptionally well-executed implementation that thoroughly fulfills the requirements outlined in the design and implementation plans. You successfully extended the clarity workflow to handle PR drafts and audience access constraints without falling into the trap of over-engineering or introducing unnecessary dependencies.

Here is the review of the provided changes:

### Findings

[LOW] `docs/feat/wip/clarify-docs/tasks.md:18` – Task 2 tracker status is left as "in-progress" with unchecked boxes.
→ **Fix:** Since the provided patch implements the complete scope of Task 2 (PR drafts, destination visibility, and evals), update the status to `done` and check off the items for this task before finalizing the PR.
```markdown
 ## Task 2: Clarify PR drafts without leaking private context

-**Status:** in-progress
+**Status:** done
 **Depends on:** Task 1
```

[LOW] `/tmp/clarify-docs-task2-review.patch:557` – The generated patch file contains trailing script errors (`zsh:2: command not found: git`).
→ **Fix:** While this does not affect the repository's code, ensure the tool or script generating your patches has `git` correctly in the `$PATH`. This will prevent malformed patch files or silently dropped diff chunks in future automated pipeline runs.

---

### Overall Code Quality Summary
The implementation is highly pragmatic and strictly adheres to the architectural boundaries defined in the feature specs. The logic regarding PR scope resolution and destination visibility is translated into clear, unambiguous prompt instructions rather than overly complex code logic. The evaluation suite is comprehensive, utilizing well-designed synthetic fixtures and an excellent `trap` system to isolate and verify specific LLM failure hypotheses (such as hallucinating runtime verification or leaking data by simply deleting a private citation).

### Top Priority Fixes
- Update the `tasks.md` status to `done` and check off the completed Task 2 items to close out the mid-implementation tracking.
- Resolve the missing `git` command error in your local patch generation environment to ensure clean output artifacts moving forward.
- *(No further technical fixes are required; the implementation is logically and structurally sound).*

### Positive Aspects
- **Precise Security & Visibility Rules:** The ordered visibility constraints in `_shared/document-clarity.md` correctly separate tracked PR-head files from explicit audience restrictions and unverified external links. You explicitly instructed against the dangerous pattern of LLMs assuming that deleting a private citation makes the underlying fact public.
- **Scope Discipline:** The instructions actively prevent scope creep, explicitly forbidding the tool from mutating remote PRs, inventing runtime evidence for contract-only PRs, or making external writes.
- **Outstanding Test Design:** The `eval.json` traps correctly map to realistic AI failure modes (e.g., "Smooths unverified remote claims into facts" and "Trusts the stack label instead of actual base/head"). This is top-tier prompt evaluation design.
- **Concise Prompt Engineering:** You managed to cover complex PR orientation and privacy limits while staying lean and well within your whitespace-delimited instruction budget.
