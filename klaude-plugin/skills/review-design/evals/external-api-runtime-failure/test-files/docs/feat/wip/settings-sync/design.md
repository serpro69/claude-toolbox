# Settings sync

> Status: designed
> Created: 2026-10-20
> Implementation: [implementation.md](implementation.md)

## Problem and outcome

Settings saved through `src/settings.py` stay on the machine that saved them. Users who work on two machines re-enter the same values on each. After this feature, a successful save on one machine is pushed to the configured provider, and a second machine that reads from the same provider sees the new values within one sync interval.

## Architecture

A new `SettingsSync` service in `src/settings_sync.py` (to be created) subscribes to successful saves in the existing `Settings` class (`src/settings.py`) and pushes the changed keys to `Provider.apply`. A failed push is retried up to 3 times with exponential backoff; after the third failure the push is dropped and a warning is logged so the user can trigger a manual sync.

The `Settings` class keeps its current contract: `save()` returns `{"ok": True}` only when the provider reports the values as applied.

## Assumptions

- `Provider.apply` is idempotent for the same key/value pair, so a retried push cannot double-apply.
- A sync interval of 30 seconds is acceptable; there is no real-time requirement.

## Not Doing

- Conflict resolution between two machines editing the same key: last write wins in this iteration, and the follow-up feature will add vector clocks if users report lost edits.
- Encrypting settings in transit: the provider transport already uses TLS.
