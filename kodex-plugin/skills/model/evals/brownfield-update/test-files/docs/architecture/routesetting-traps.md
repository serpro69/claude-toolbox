# Routesetting — divergences & traps

> **Freshness:** This page is `proposed` until reviewed by a human other than its author — it is **not** self-certified. Check staleness by re-running `$kk:review-architecture` against the Derived-from anchors at consumption time.

Only facts no single file reveals: divergences between the stated rules and the code (`D#`), and cross-file hazards (`P#`). Numbering is stable; retired numbers are not reused.

### D1 — Grade-before-open declared but unenforced

Rule L1 says a route must carry a grade before it opens. `gym/route.go` `OpenRoute`
checks the route's state and wall assignment but never its grade — an ungraded route
opens without error. The rule is intent; the code does not implement it.

**Retires when:** `OpenRoute` gains a grade check, or L1 is withdrawn.

### P1 — Free-text grade vs. display scale

`Route.Difficulty` is written as free text — `gym/grading.go` `SetGrade` accepts any
string — while `DisplayGrade` only recognizes values in `Scale` and silently shows an
unrecognized value raw. Neither file alone reveals that a typo at set time reaches the
route card unflagged.

**Retires when:** grades are validated against `Scale` at the write path, or `DisplayGrade` rejects unknown values.

---
**Derived-from:** `gym/route.go` · `gym/grading.go`
