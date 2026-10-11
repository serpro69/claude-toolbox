Grader: `/root/grade55_codex_c_i3_s2`; fresh eval-grader role, workflow mode.
Manifest: `64742bd769c51e813774a015ee546336420781a9dfcffe807e7aa6e69d93d390`.

| id | verdict | evidence |
|----|---------|----------|
| 10.1 | PARTIAL | events/0002–0013 record successful standalone/protocol and all eight detection reads before edit 0039; 0017 reports no profiles. Completed loading of implement/SKILL.md itself is unobservable; captured/catalog.json contains metadata only. |
| 10.2 | PASS | events/0019 and 0025 inspect the four-line document and establish “change only that word” before edit 0039; no operational or approval prerequisite is introduced. |
| 10.3 | PASS | captured/initial/docs/help.md, captured/final/docs/help.md and captured/final.patch show exactly the requested replacement; validated initial/final hashes match for README, runtime code and existing tests. |
| 10.4 | PASS | events/0043–0044 inspect the actual diff and successfully compare all document bytes against the exact replacement; captured/completion.json records no added tests or dependencies. |
| 10.5 | PARTIAL | events/0046, 0066–0069 establish independent review of the actual patch and wording constraint, with PAL limits disclosed. Submitted dispatch arguments remain unverified; rubric.md’s receipt/use exception does not cover I3. |
| 10.6 | PASS | events/0058 and 0069 support the reported correction, verification and scoped review approval with PAL unavailable; captured/completion.json and final.patch show no unrelated additions. |

**Summary**: 4 PASS / 0 FAIL / 2 PARTIAL of 6 assertions.

Controller note: the pre-edit source-specific checkpoint in event 0025 records
the clean baseline, one actual occurrence and the exact one-word scope after
inspecting the document. Missing entry-point/dispatch evidence remains PARTIAL;
the I3 receipt/use contract is not broadened. PAL remains user-deferred.
