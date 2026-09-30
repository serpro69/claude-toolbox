1. This work helps readers recognize archived entries while retaining access to their destinations. Hiding entries was rejected because readers still need their links. **Sources:** `design.md` introduction and “Rejected Alternatives.”

2. Each archived entry should display `Archived` beside its existing title and link. Active entries should remain unchanged. **Source:** `design.md` → “Label contract.”

3. The selected work is manual editing of `catalog.md`, followed by verification; there is no runtime application to implement. Overall status is **in progress**: Task 1, checking existing archive state, is done; Task 2, adding labels, and Task 3, final verification, are pending. The documents do not establish that labels have been added or tested. **Sources:** `implementation.md` introduction and “Assumptions”; `tasks.md` → Tasks 1–3.

4. Filtering, automatic archival, and color changes are outside the selected work. Hiding archived entries is a rejected alternative. **Sources:** `implementation.md` → “Not Doing” and “Rejected Alternatives.”

5. Catalog maintainers must choose a color after checking contrast; that decision remains open and does not block text labels. Next, the implementer inspects the catalog, adds labels while preserving titles, links, and active entries, then completes final verification using `/kk:test`, `/kk:document`, `/kk:review-code`, and `/kk:review-spec`. No individual implementer or completion date is specified. **Sources:** `implementation.md` → “Open decision,” “Implementation steps,” and “Assumptions”; `tasks.md` → Tasks 2–3.
