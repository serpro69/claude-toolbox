I’ll read the three supplied documents and answer the five questions using their stated details.


1. The work helps contributors recognize archived entries while scanning the catalog, without opening each entry. *(design.md, “Purpose and planned behavior”)*

2. Archived entries should retain their existing title and clickable destination, remain visible, and display **Archived** beside the link. Active entries retain their title and link without a label. *(design.md, “Purpose and planned behavior”; implementation.md, “Label archived entries”)*

3. This increment includes inspecting existing archive markings, adding text labels to `catalog.md`, checking the complete catalog and rendered Markdown, and completing documentation and reviews. The design is accepted; implementation has not started, and both tasks are pending. *(design.md, status; implementation.md, “Label archived entries” and “Final verification”; tasks.md, Tasks 1–2)*

4. Filtering, hiding entries, automatic archival, and color changes are excluded. The work introduces no dependencies, generation automation, application code, or automated test suite for this change. *(design.md, “Accepted decisions and constraints,” “Not Doing,” and “Rejected Alternatives”; implementation.md, “Scope and starting point” and “Label archived entries”)*

5. Color remains undecided; catalog maintainers will choose it after checking site contrast, independently of this text-only change. The archive-marking convention and entry inventory remain unverified: the contributor must inspect the catalog, and maintainers must resolve any ambiguous status before affected entries are labeled. The recommended next action is `/kk:review-design archive-label`, which has not run. Then Task 1 implements and checks labels; Task 2 performs verification, documentation, and reviews, recording results and unavailable checks before completion. *(design.md, “Assumptions” and “Open color decision”; implementation.md, “Final verification”; tasks.md, Tasks 1–2)*
