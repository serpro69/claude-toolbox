# Task 12 preflight observations

These are loading/setup checks, not behavioral acceptance.

- Baseline bundle: 435 retained files; archive
  `645174753421c14bfb525c8060c9d313b0bfa5a6f486413590444930fc937131`;
  retained manifest `0dedccb8cdb3825f3531d851b5fd83ac9938538c22a3d9c6e299a67b53edf230`.
- Candidate 1 bundle: 443 retained files; archive
  `8d819205782ff4eebdbf48fbc8e56b9612789703039f2fcd2989347b44355f4a`;
  retained manifest `d553b6a3b41d88a62f635756816f9ea2ec3037d79c562c43d89393efd80c6b98`.
- Two [state probes](state-probe/summary.json) passed indexing/search, absent
  foreign markers and unavailable vault checks. Their stores are never reused.
- [First baseline probe](binding-baseline/manifest.json) exhausted API connection
  retries in the sandbox and exited 1; no measured scenario ran.
- [Candidate probe](binding-candidate1/manifest.json) completed through approved
  network access. Main events 12/13 invoke the registered skill, 15/18 return the
  selected root, 25–36 return required instruction files. Events 45/59 link the
  named reviewer; child 51/52 and 54/55 return common method and entry-point bytes.
- A prepared baseline retry (`binding-baseline2/`) was rejected before launch
  by automatic approval review: mutable inputs were not revalidated at launch,
  so actual outgoing inputs were insufficiently bounded. The controller was
  corrected and mutation-tested; no indirect retry bypassed that rejection.
- [Fresh baseline probe](binding-baseline3/manifest.json) used the corrected
  launch guard and approved network access. Main 11/12 invoke the skill, 14/17
  return its root, 24–29 return required instructions. Named reviewer 38/53 and
  child entry-point read 44/45 establish loading. Returned actor messages on both
  successful probes identify `claude-opus-4-8`; helper Haiku usage in runtime
  accounting is not a substitute actor/reviewer model.

The prepared fixtures and copied bundles were manifest-verified. Independent
review subsequently strengthened snapshot-to-revision manifest binding; the
measurement freeze uses that correction. Preserve both preflight freezes and
all attempts. Exact submitted prompt/parity limits remain as declared.
