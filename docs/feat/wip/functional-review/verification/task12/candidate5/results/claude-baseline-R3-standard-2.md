| id | verdict | evidence |
|----|---------|----------|
| 7.1 | FAIL | e17.0 requires reading all eight Known profiles; only Python detection is read before full investigation at e54.0–e57.0, with no missing-file exceptions established. |
| 7.2 | PASS | README read e95.0 identifies the supported Git tag and excludes candidate/live baselines; e103.0–e106.0 successfully retrieves eval-release:provider/settings.py. |
| 7.3 | PASS | e144.0 quotes the provider's storage write and ok response, then traces absent applied through the unconditional check to RuntimeError with the flag false. |
| 7.4 | PASS | e144.0 calls the change a delivery-contract violation and explicitly excludes pending Task 2 from the reviewed implementation. |
| 7.5 | PASS | Manifest declares standard mode; e103.0–e106.0 records the successful direct historical source read. |
| 7.6 | PASS | In standard mode, e59.0 and e106.0 supply candidate and release source; e144.0 directly compares their acknowledgement behavior. |
| 7.7 | FAIL | e144.0 states REQUEST_CHANGES but omits Blocked and claims production ordinary saves fail without verified production evidence. |
| 7.8 | PASS | e144.0 gates both receipt request and enforcement behind enhanced_settings, preserving ordinary saves and rejecting the receipt-only mock as compatibility evidence. |

**Summary:** 6 PASS / 2 FAIL / 0 PARTIAL of 8 assertions.

Independent grader: `/root/grade_c5_b_r3_2`; pinned workflow grader/rubric.
