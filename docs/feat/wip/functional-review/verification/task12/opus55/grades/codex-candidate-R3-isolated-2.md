Grader: `/root/grade55_codex_c_r3_i2`; fresh eval-grader role, workflow mode.
Manifest: `304d90367b39f72f9d8013567cef388e68376e411623a8140901689abb3be631`.

| id | verdict | evidence |
|----|---------|----------|
| 7.1 | PASS | Main instruction reads (`events/0007.json`–`0019.json`) precede investigation (`0022.json`); child instruction reads (`0043.json`–`0050.json`) precede contracts/source (`0052.json`). Routing used filenames and metadata (`0014.json`). |
| 7.2 | PASS | `events/0022.json` discovers the README’s release contract; `0024.json` retrieves `eval-release` revision `22140737b2bc5792b535f3f8ce16f7fa162101db` and provider source. `0054.json` distinguishes release, review base, candidate and deployment evidence. |
| 7.3 | PASS | `events/0040.json` cites `client.py:5` and historical release evidence, tracing applied settings followed by `RuntimeError` with `enhanced_settings=False`; `0030.json` reproduces that outcome. |
| 7.4 | PASS | `events/0040.json` identifies an introduced violation of independent release requirements and keeps Task 2 outside scope; `0072.json` explicitly rejects pending Task 2 as satisfying current delivery requirements. |
| 7.5 | FAIL | `events/0027.json` materializes historical source outside the worktree; `0058.json` and `0062.json` establish named-reviewer source/provenance receipt. Retained protocol calls contain no PAL invocation, and `0040.json` explicitly reports only one reviewer. |
| 7.6 | FAIL | The linked reviewer uses the historical comparison in `events/0072.json`, following receipt in `0058.json` and `0062.json`; `0040.json` confirms no second-reviewer corroboration, and no PAL result appears in retained calls. |
| 7.7 | PASS | `events/0040.json` reports `REQUEST_CHANGES`, marks supported-provider compatibility “blocked,” and states that live deployment was not assessed. |
| 7.8 | PASS | `events/0040.json` proposes preserving legacy success handling and testing applied values plus caller success; it identifies the updated mock as hiding the regression and supports compatibility with the historical-provider execution in `0030.json`. |

**Summary**: 6 PASS / 2 FAIL / 0 PARTIAL of 8 assertions; required PAL participation was omitted, while exact submitted handoff plaintext remains unverified.

Controller note: PAL remains user-deferred; no missing component is waived.
