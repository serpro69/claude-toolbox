# Source-disagreement: executable-example rerun

Date: 2026-09-29. The preceding two attempts are preserved. The second reader
explicitly compared immediate 20 with required next-day activation, but the editor
and reader left actual existing-order behavior unknown. The initial fixture showed
only lookup and creation functions, without the default-change operation itself.

This attempt adds `default_change_example()` to the supplied synthetic `prep.py`.
It creates an inherited order at 15, changes the restaurant default to 20, and
returns both the new lookup and saved order value. Running the fixture directly
checks and prints `{'new_lookup': 20, 'old_order': 15}` (exit 0). This is fixture
evidence, not a production feature or an additional skill instruction.

Before spawning any session for this attempt, the eval and oracle were snapshotted
under grader-inputs/. The explicit question from retry1, all assertions, expected
answers, protected claims and baseline defects remain unchanged. Only the supplied
implementation evidence is strengthened. The original guide remains unchanged.
The editor is given the same request and operative skill, with no hints about the
expected answer or earlier attempts. Both readers are fresh and receive identical
questions with only their artifact path differing.
