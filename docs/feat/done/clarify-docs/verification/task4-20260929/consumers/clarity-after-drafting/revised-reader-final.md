1. This work helps contributors recognize archived entries without opening each entry. It adds a visible **Archived** label to the manually maintained catalog.  
   Pointer: `design.md`, “Purpose and planned behavior,” lines 10–14.

2. An archived entry should retain its existing title and clickable destination, remain visible, and display **Archived** beside its link. An active entry retains its title and link without a label.  
   Pointers: `design.md`, lines 10–12; `implementation.md`, line 18.

3. Included work is to verify existing archive markings, label archived entries in `catalog.md`, inspect the diff, preview the Markdown, and complete applicable checks, documentation, code review, and specification review. The design is accepted; implementation and both tasks remain pending. No catalog edit has been delivered.  
   Pointers: `design.md`, lines 3 and 14; `tasks.md`, “Task 1” and “Task 2,” lines 9–36.

4. Filtering or hiding entries, automatic archival, and color changes are excluded. Titles and destinations must remain unchanged. Dependencies, catalog-generation tooling, and a new automated test suite are also outside this edit.  
   Pointers: `design.md`, “Accepted decisions and constraints” and “Not Doing,” lines 20–35; `implementation.md`, lines 21 and 29–33.

5. Color remains undecided: catalog maintainers should choose it after checking the site’s contrast; it does not block text labels. The catalog’s marking convention and entry inventory are unverified. The implementing contributor must inspect them and obtain maintainers’ resolution of any ambiguous status before labeling affected entries. Next comes the recommended `/kk:review-design archive-label`, which has not run, followed by implementation and final verification. Availability of the site’s rendering workflow is also unknown; unavailable checks must be recorded.  
   Pointers: `design.md`, “Assumptions” and “Open color decision,” lines 27–29 and 43; `implementation.md`, lines 19 and 35–39.
