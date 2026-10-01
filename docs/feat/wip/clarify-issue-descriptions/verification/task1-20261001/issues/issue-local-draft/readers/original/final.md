1. The issue exists because synchronous export ignores a requested zero wait, delaying maintainers checking a ready invoice.

2. On ExportKit 2.3.1, macOS 15 arm64, running `exportctl send invoice-17 --timeout-ms 0 --mode sync` with invoice-17 ready waited 30 seconds in all three attempts. Expected: zero wait.

3. The command and environment are recorded. The three waits are reported; Mina’s confirmation on the reported build is pending. Replacement of zero by the default is suspected but unverified. The artifact states that requirements define zero as “don’t wait.”

4. Async export is outside this issue.

5. Mina must confirm the behavior on the reported build. A fix will be chosen after confirmation; ownership of choosing or implementing that fix is not specified.
