# Workspace preferences

Python 3.9+, standard library only. Run `python3 -B -m unittest discover -s tests`.

Saving preferences is a serialized operation identified by a caller-supplied
operation ID. A failed save can be retried with the same ID and edited values;
success means the latest submitted values are active. Repeating a completed ID
returns its receipt. A fresh operation ID must perform a fresh save, even for
the same workspace. Recovery records remain available for audit after completion.

The provider replaces preferences idempotently. A receipt write can fail after
the provider has applied values. The in-memory store models that boundary; no
threads, process restart, network service or exactly-once external effect is promised.
