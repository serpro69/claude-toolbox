# Grader calibration controls

These are synthetic controller/grader records, never actor fixtures. Exclude this entire directory with the actor bundle's `evals/` exclusion. Do not stage it under a subject workspace or expose expected grades to the grader being tested.

Pin the concrete eval-grader instructions. For each workflow directory (`early-edit`, `missing-events`, `ordered`, `complete-omission`, `requested-only`), validate every hash in its manifest, then dispatch a fresh independent grader with **Grading mode: workflow**, the pinned instructions, manifest and its listed rubric/assertions. Evidence paths are relative to that manifest's directory. Retain dispatches, hash validation, exact grader output and the grader instruction hash. These are synthetic calibration results, not actor behavioral acceptance.

For the `component` directory, dispatch two fresh graders with its assertions and reviewer output: one with mode omitted, the other with **Grading mode: component**. Supply no manifest or workflow rubric. Both must preserve legacy input requirements and return the same grades.

After each grader returns, the controller compares its table with [expected-verdicts.json](expected-verdicts.json). Never include that file in the tested grader's read manifest or prompt. The negative records distinguish a false final claim from actual ordering, missing events from a complete omitted action, and a requested/denied read from a successful returned read. No runtime execution is needed to construct these records.

A later receipt/use fallback needs additional negative and positive controls before use: parent claims/correct findings without linked independent receipt cannot pass; complete linked receipt/use can satisfy only the revised assertion, leaving exact prompt content unverified. These revision-1 controls do not activate that fallback.
