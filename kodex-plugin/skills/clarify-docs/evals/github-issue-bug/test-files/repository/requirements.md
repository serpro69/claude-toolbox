# Replay receipt requirement

A completed job must emit one receipt even when delivery is retried. This issue
concerns duplicate receipts, not the status UI. The requirement predates 1.4.2.
The root cause is undecided; Bea owns repeating the old-version report with receipt
logging. No new acceptance threshold or implementation choice has been accepted.
