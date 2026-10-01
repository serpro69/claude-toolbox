1. The issue exists because synchronous export reportedly waits 30 seconds despite `--timeout-ms 0`, delaying maintainers checking a ready invoice. The stated contract requires zero to mean no wait; missing or null values use the 30,000-millisecond default.

2. On ExportKit 2.3.1, macOS 15 arm64, with invoice-17 ready, `exportctl send invoice-17 --timeout-ms 0 --mode sync` reportedly waited 30 seconds in all three attempts. Zero wait was expected.

3. The command and environment are recorded. The artifact states that the supplied source snapshot uses `timeout_ms or 30000`, converting zero to 30,000 and supporting the suspected cause. Runtime behavior on the reported build remains unconfirmed.

4. Asynchronous export is explicitly outside this issue. No other exclusions are stated.

5. Mina must confirm the behavior on the reported build. A fix will be chosen after confirmation; ownership of choosing or implementing it is not stated.
