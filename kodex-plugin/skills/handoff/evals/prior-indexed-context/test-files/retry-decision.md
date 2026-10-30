# Retry decision

Use one attempt until the service supports idempotency keys. Repeating a timed-out
submission can create a duplicate parcel. Preserve the 20-second timeout.
