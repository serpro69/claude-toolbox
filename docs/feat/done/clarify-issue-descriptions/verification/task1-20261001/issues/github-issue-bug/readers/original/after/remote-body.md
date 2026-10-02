# REPLAY broken?? retries????

Something in seen_receipts maybe? UI is separate, not asking for that here. Bea
needs to check the old version again with receipt logging; retry loop seems guilty
but that is a guess. [Requirements](repository/requirements.md) say one receipt for
a completed job. [Current source](repository/replay.py) is around now too.

On QueueKit 1.4.2, Linux x86_64: seed completed job-42, then run
`queuectl replay job-42 --retry 1 --timeout-ms 250`. Let the first receipt time out
at 250 ms. I got two receipts in 2 of 5 attempts, wanted one. I did not test 1.5.0.
This makes operators unsure whether a completed job was handled twice.

- [x] Capture reporter environment
- [ ] Bea: repeat on 1.4.2 with receipt logging

This is a report, not a delivered fix.
