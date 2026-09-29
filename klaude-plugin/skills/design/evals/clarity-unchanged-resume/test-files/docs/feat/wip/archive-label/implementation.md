# Archive-label implementation

Follow the accepted [label contract](design.md#label-contract). Task 1 verified that
catalog.md identifies archived entries consistently; Task 2 is ready to implement.

1. Add the word Archived beside each archived entry in catalog.md → verify: every
   archived entry displays that word and retains its original title and destination.
2. Leave active entries unchanged → verify: compare the diff with the archive-state
   markers and confirm active titles, links and text are byte-identical.
3. Run the [final verification task](tasks.md#task-3-final-verification) → verify:
   checks pass and documentation matches the accepted contract.

Color changes remain out of scope. Catalog maintainers will choose a color only
after checking contrast; the text-label task does not depend on that decision.
