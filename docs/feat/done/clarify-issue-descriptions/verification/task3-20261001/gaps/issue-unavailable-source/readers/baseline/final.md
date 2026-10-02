1. The issue exists because synchronous export reportedly waits despite a zero timeout, delaying invoice checking.

2. On ExportKit 2.1 / Ubuntu 24.04, `exportctl send invoice-21 --timeout-ms 0 --mode sync` reportedly waited 30 seconds in 2 of 3 tries. The expected behavior was an immediate return.

3. The command and environment are recorded. The wait is reported, without independent reproduction. Replacing zero with a default timeout is the reporter’s unconfirmed hypothesis. Source access was denied, and no source, tests, logs, PR or alternate copy is accessible to verify the behavior or cause.

4. Async export is out of scope. No fix is agreed.

5. Mina owns obtaining an accessible v2.1 source snapshot. After that, reproduce on the reported version and compare timeout handling before selecting a fix. Ownership of reproduction and cause confirmation remains unassigned.
