1. **Why this exists:** Operators need to catch CSV mistakes before applying an import. Preview observes candidate rows without committing durable rows. *(design.md, Context)*

2. **Representative case:** A three-row CSV containing one invalid row produces counts of two valid and one invalid, while writing zero rows. *(design.md, Context)*

3. **Current increment:** Deliver preview only, accepted by Mira on 2026-09-01. CSV columns must remain `id,name`; accepting those columns is complete, while returning valid and invalid counts remains unfinished. Operators may download diagnostics. Preview can be enabled only after the support owner approves the sample-file walkthrough; approval status is unstated. *(design.md, Decision and Deployment gate; tasks.md, Task 1: Preview; entry.md, Resume)*

4. **Outside this increment:** Applying imports remains future work and disabled. Task 2, Apply, is pending and depends on Task 1. Downloading diagnostics does not authorize applying rows. *(design.md, Context, Decision and Consequences; tasks.md, Task 2: Apply)*

5. **Remaining decision:** Product must decide the duplicate-row policy before apply is implemented. The files specify neither the policy nor a decision date. Support-owner approval is also required before enabling preview, but the files do not establish whether it has occurred. *(design.md, Context and Deployment gate; tasks.md, Task 2: Apply)*
