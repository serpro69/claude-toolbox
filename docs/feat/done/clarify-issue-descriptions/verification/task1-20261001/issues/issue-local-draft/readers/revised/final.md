1. The issue exists because synchronous export reportedly ignores `--timeout-ms 0` and waits 30 seconds, delaying maintainers checking a ready invoice.

2. On ExportKit 2.3.1, macOS 15 arm64, running `exportctl send invoice-17 --timeout-ms 0 --mode sync` with invoice-17 ready reportedly waited 30 seconds in 3/3 attempts. Expected behavior was no wait.

3. Source inspection found `return timeout_ms or 30000`, which replaces zero with 30000 and conflicts with the stated contract. This supports a suspected cause but does not establish causation. No execution evidence is supplied, and the reproduction was not run during the edit. Behavior on the reported build remains unconfirmed.

4. Asynchronous export is outside this issue.

5. Mina must confirm behavior on the reported build before a fix is chosen. The draft does not identify who owns choosing or implementing the fix.
