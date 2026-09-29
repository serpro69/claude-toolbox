1. **Why this exists:** Import preview helps operators catch CSV errors before applying an import by showing valid and invalid row counts without writing rows. (`design.md`, **Context**)

2. **Representative case:** A three-row CSV with one invalid row reports two valid rows and one invalid row, writing zero rows. CSV columns must remain `id,name`; operators may download diagnostics, which do not authorize applying rows. This is the planned contract; no implementation source was supplied. (`design.md`, **Context**, **Decision**)

3. **Current increment:** Preview-only delivery, accepted by Mira on 2026-09-01. Task 1 is in progress: column parsing is recorded as complete, while returning valid and invalid counts remains pending. The recorded progress cannot be verified from implementation source. Enablement requires support-owner approval of the sample-file walkthrough. (`tasks.md`, **Task 1: Preview**; `design.md`, **Decision**, **Deployment gate**; `entry.md`, **Resume**)

4. **Outside this increment:** Applying imports remains future work and disabled. Task 2, Apply, is pending and depends on Task 1. (`design.md`, **Consequences**; `tasks.md`, **Task 2: Apply**)

5. **Still needing a decision:** Product owns the unresolved duplicate-row policy, which must be decided before implementing apply. Support-owner approval is also required before enabling preview; the files do not state whether that approval has occurred. (`design.md`, **Context**, **Deployment gate**; `tasks.md`, **Task 2: Apply**)
