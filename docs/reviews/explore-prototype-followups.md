# Explore page follow-ups

## Current page (2026-11-14): real catches from capy

The Explore page was rebuilt as a cold open plus five chapters, each one real
catch from capy's records (capy was built from start to finish with
claude-toolbox). The user approved the chapter content before the rebuild and
chose capy as the single source. Content lives in the front matter of
`docs/explore/index.md`; see "Interactive field guide" in
`docs/contributing/architecture.md` for the structure and editing rules.

Known gaps:

- **Not checked on real devices.** Verified in headless Brave only, at
  1440×1000, 820×1180 and 390×844 (mobile emulation), with JavaScript disabled
  and with reduced motion. Light scheme was checked without JavaScript only:
  the test profile kept a stored dark palette for the scripted runs.
- **Three pane commands are inferred, and the pane says so.** The records for
  `one-reader` (`/kk:design`), `symlink` (`/kk:review-code:isolated`) and
  `default-wait` (`/kk:review-spec:isolated`) describe the review or design
  step but don't quote the command. If a record turns up that quotes it, drop
  `inferred: true`.
- **Closing figures are a snapshot** (capy as of 2026-11-14: 672 commits, 37
  ADRs, 27 finished feature records). CI has no capy checkout, so they can't be
  computed at build time. Update the numbers and the date by hand.
- **Excerpt fidelity is checked by hand-run script only.** Every excerpt was
  verified against `origin/master` of its repo (30 fragments, 0 mismatches).
  There's no CI check because CI has no capy checkout; when editing an excerpt,
  re-check it against the source line by hand.
- **Independent review is deferred** to the end of prototyping, at the user's
  request.

## Previous version

The earlier scroll-driven Three.js journey (an invented "Fieldnotes" feature,
laptop dive, pawns, booth and marbles) was removed in this rebuild after an
external review found that the first screen didn't explain the product and
that every artifact was invented. It's preserved in git history at `a9023188`
on `temp_docs` if the laptop dive is ever wanted back as an opener.
