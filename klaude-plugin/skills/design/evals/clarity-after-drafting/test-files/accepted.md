# Accepted archive-label idea

The catalog maintainer wants contributors to recognize archived entries without
opening each entry. Success: every archived entry in the static catalog displays
the word Archived, while active entries have no label. The catalog is manually
maintained in catalog.md; no runtime application exists in this workspace.

HMW framing, contributor persona, success condition and constraints are approved.
This is a simple single-path change. The chosen direction is a textual label beside
each archived entry. Hiding archived entries was rejected because readers still need
their links. The design presentation is approved; fact-checking alternatives is not
requested. Do not introduce dependencies or automate catalog generation.

Constraints: keep existing destinations and titles. An archived entry stays visible
and clickable. Only label text is in this increment; color is undecided. Owner:
catalog maintainers; next step: choose a color after checking the site's contrast.
Assumption: authors already mark archived entries consistently. Verify that before
implementation. Not Doing: filtering, automatic archival, color changes.

Produce a small label-edit task with concrete verification and a final verification
task. Preserve the distinction between accepted requirements and future edits.
