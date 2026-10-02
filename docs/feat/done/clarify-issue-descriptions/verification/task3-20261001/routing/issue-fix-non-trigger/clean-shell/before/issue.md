# Bug: zero timeout replaced

Read-only offline issue for https://github.example.invalid/acme/export/issues/24.

`resolve_timeout(0)` currently returns 30 but must return 0. Only `None` should select the default 30; positive values such as 5 must be preserved. Fix timeout.py. No external dependencies or live tracker access are needed.
