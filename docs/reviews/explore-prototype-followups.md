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
- **Closing figures refresh only on docs deploys.** The docs workflow counts
  them from a capy clone (`scripts/mkdocs/capy_stats.py`); a released docs
  version keeps the figures it was built with, dated by its as-of line. The
  front-matter snapshot (672 commits, 37 ADRs, 27 finished feature records, as
  of 2026-11-14) is only the fallback; refresh it by hand if a deploy reports
  "Kept the snapshot capy figures". The hook was exercised locally (snapshot,
  live counts, missing clone, repo without capy's layout), not yet in CI.
- **Excerpt fidelity is checked by hand-run script only.** Every excerpt was
  verified against `origin/master` of its repo (30 fragments, 0 mismatches).
  When editing an excerpt, re-check it against the source line by hand. The
  docs workflow's capy clone could support a CI check (a blob-less clone
  fetches file contents on demand), but none is built yet.
- **Independent review is deferred** to the end of prototyping, at the user's
  request.

## Previous version

The earlier scroll-driven Three.js journey (an invented "Fieldnotes" feature,
laptop dive, pawns, booth and marbles) was removed in this rebuild after an
external review found that the first screen didn't explain the product and
that every artifact was invented. It's preserved in git history at `a9023188`
on `temp_docs` if the laptop dive is ever wanted back as an opener.
