# Parcel client

The transport has no idempotency keys. The pending review covers a change from
three attempts to one to prevent duplicate parcel creation. Timeout stays at 20.
