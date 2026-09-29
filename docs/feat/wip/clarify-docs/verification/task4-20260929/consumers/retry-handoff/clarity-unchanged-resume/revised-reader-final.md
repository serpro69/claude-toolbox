1. The work helps readers recognize archived entries while preserving destinations they still need. Hiding entries was rejected because it would remove those links. (`design.md`, opening purpose and “Rejected Alternatives,” lines 3, 18–20.)

2. Each archived entry should show **Archived** beside its existing title and link. Active entries should remain unchanged, including byte-identical titles, links, and text. (`design.md`, “Label contract,” lines 5–8; `implementation.md`, lines 6–9.)

3. The selected work is manual editing of `catalog.md`, followed by verification; there is no runtime app. The overall status is in progress: Task 1 verified consistent archive-state markers and is done; Task 2, adding labels, is pending and ready to implement; Task 3, final verification, is pending. (`design.md`, lines 7–8; `implementation.md`, lines 3–4; `tasks.md`, lines 5, 8–33.)

4. Filtering, automatic archival, and color changes are excluded. Hiding archived entries is a rejected alternative. (`design.md`, “Not Doing” and “Rejected Alternatives,” lines 14–20.)

5. Catalog maintainers still need to choose a color after checking contrast; the specific color and timing are unknown. That decision does not block text labels. Next comes Task 2, followed by Task 3: run `/kk:test`, `/kk:document`, `/kk:review-code`, and `/kk:review-spec`, confirming passing checks and documentation consistent with the contract. No owner for Tasks 2–3 is named. (`design.md`, “Open decision,” lines 22–25; `tasks.md`, “Task 2,” “Task 3,” and “Dependency Graph,” lines 17–38.)
