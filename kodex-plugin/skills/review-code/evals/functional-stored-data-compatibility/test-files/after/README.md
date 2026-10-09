# Saved destinations

Python 3.9+, standard library only. Run `python3 -B -m unittest discover -s tests`.

Destination records can use legacy top-level `address` or current nested
`destination.address`. New writes use the nested shape. Background migration
runs in bounded batches while reads remain available; a deployment must read
both shapes until migration finishes. Existing addresses must be preserved.

`data/records.json` is a supported mixed snapshot. `api.list_destinations`
serves all saved records through the same reader. `migrate_batch` changes up to
its limit per invocation; there is no startup migration gate. The store is a
local JSON model, with no production environment or external database required.
