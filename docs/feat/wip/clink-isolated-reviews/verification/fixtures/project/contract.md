# Contract

Project receipt: `MOSS-HARBOR-826`.

`retry_delay(attempt)` accepts nonnegative integer attempts and returns seconds. Attempt zero must return 5; later attempts return 10. Existing callers may pass zero.

The design proposal must retain that contract. It does not promise implemented code.
