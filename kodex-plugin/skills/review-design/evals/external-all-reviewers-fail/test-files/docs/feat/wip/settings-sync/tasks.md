# Tasks: settings sync

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Status: pending
> Not Doing: conflict resolution between machines, transit encryption

## Task 1: Add the save hook

- **Status:** pending
- **Size:** S
- **Can run in parallel with:** —

### Subtasks

- [ ] 1.1 Add `on_saved(callback)` to `Settings` in `src/settings.py` → verify: callbacks run after a successful save only.

## Task 2: Sync service

- **Status:** pending
- **Depends on:** Task 1
- **Size:** M

### Subtasks

- [ ] 2.1 Create `src/settings_sync.py` with `SettingsSync.push(keys)` → verify: each key reaches `Provider.apply`.
- [ ] 2.2 Implement the retry loop → verify: a transient provider failure is retried.
- [ ] 2.3 Register the service at startup → verify: a save on one machine appears on the provider.

## Dependency Graph

```text
Task 1 --> Task 2
```
