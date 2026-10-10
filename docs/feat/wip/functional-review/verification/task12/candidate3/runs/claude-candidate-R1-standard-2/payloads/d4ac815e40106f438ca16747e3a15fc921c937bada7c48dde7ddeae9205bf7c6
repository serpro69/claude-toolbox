# Workspace associations

Python 3.9+, standard library only. Run `python3 -B -m unittest discover -s tests`.
A workspace has one active setup association. Setup jobs can fail after creating
a pending record. Another setup can complete before the failed job's queued
cleanup runs. Completed associations are consumed by `active_connection`.
Cleanup removes the failed setup's pending record and any association it owns.
The store models serialized operations; concurrency and external services are
outside this change.
