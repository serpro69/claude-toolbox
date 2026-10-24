# Implementation: settings sync

> Design: [design.md](design.md)

## Files

- `src/settings.py` (existing): add an `on_saved(callback)` hook to `Settings`; call every registered callback after `save()` returns `{"ok": True}`.
- `src/settings_sync.py` (new): `SettingsSync` with a provider reference, `push(keys)` and the retry loop.

## Task 1: Save hook

1. Add `on_saved(callback)` to `Settings` in `src/settings.py`, storing callbacks in a list.
2. After a successful `save()`, call each callback with the saved keys. Callback exceptions are logged and do not change the save result.

## Task 2: Sync service

1. Create `src/settings_sync.py` with `SettingsSync(provider)`.
2. `push(keys)` calls `Provider.apply` for the given keys. On failure, retry until the push succeeds, sleeping 30 seconds between attempts, so no change is ever lost.
3. Register `SettingsSync.push` through `Settings.on_saved` at application startup.
