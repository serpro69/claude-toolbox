1. The work helps readers recognize archived entries while preserving access to their destinations. Hiding those entries was rejected because readers still need their links. (`design.md`, opening and “Rejected Alternatives”)

2. Each archived entry should display the literal text `Archived` beside it, separate from its existing title and link. The title, link text and destination must stay intact. Active entries remain unchanged. (`implementation.md`, “Implementation steps,” steps 1–3)

3. The selected work is manual editing of `catalog.md` to add text labels, followed by verification. Overall status is **in-progress**: Task 1, checking archive-state consistency, is recorded as done; Task 2, adding labels, and Task 3, final verification, are pending. Actual implementation results are unverified in these documents because `catalog.md` was not supplied. (`tasks.md`, status and Tasks 1–3; `implementation.md`, “Assumptions”)

4. Filtering, automatic archival and color changes are excluded. There is no runtime application to build, and hiding archived entries is a rejected alternative. (`design.md`, “Label contract,” “Not Doing” and “Rejected Alternatives”)

5. Catalog maintainers still need to choose a color after checking contrast; the color and timing are unspecified. That decision does not block text labels. Next comes Task 2, then Task 3, which calls for `/kk:test`, `/kk:document`, `/kk:review-code` and `/kk:review-spec`. No assignee for those tasks is identified. (`implementation.md`, “Open decision”; `tasks.md`, Tasks 2–3 and “Dependency Graph”)
