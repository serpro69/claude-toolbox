I’m using the supplied `/kk:implement` and `/kk:document` instructions to trace the completion paths. I’ll keep this read-only and report the automatic calls and clarity-pass counts for each case.


| Case | Remaining automatic workflow | Automatic clarity passes |
|---|---|---|
| **1. Plan complete** | [plan-mode.md](/tmp/clarify-task4/instructions/skills/implement/plan-mode.md) prescribes `/kk:test` → `/kk:document` → brief reflection → mark the feature header `done`. | **1** when documentation outputs are drafted or updated; **0** if there are no outputs to edit. |
| **2. Standalone complete** | [implement/SKILL.md](/tmp/clarify-task4/instructions/skills/implement/SKILL.md) requires checking the remaining Required Outputs, then ends. Its continuation and completion steps apply only to plan mode; [standalone-mode.md](/tmp/clarify-task4/instructions/skills/implement/standalone-mode.md) adds no documentation completion call. | **0**. Documentation is not automatically invoked in this case. |
| **3. Task 1 complete; Task 2 pending** | [plan-mode.md](/tmp/clarify-task4/instructions/skills/implement/plan-mode.md) prescribes checking Task 1’s Required Outputs, selecting Task 2, reloading context and repeating execution, testing and review. Feature completion—including documentation—waits until all tasks are complete and verified. | **0** from finishing Task 1 alone. |

A **separate explicit documentation request** for the standalone correction would invoke [document/SKILL.md](/tmp/clarify-task4/instructions/skills/document/SKILL.md). That invocation applies the shared clarity procedure **once after all selected documentation updates**, regardless of the number of files; it skips the pass when there are no outputs to edit.

The document skill uses the shared procedure directly: it does **not** invoke `/kk:clarify-docs` or another writing skill. Its fidelity check is in-session; further project-required review remains with the caller.

No routes were executed.
