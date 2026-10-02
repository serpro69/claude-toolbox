1. The issue exists because a requested zero timeout reportedly causes a wait, delaying invoice checking.

2. Running `exportctl send invoice-21 --timeout-ms 0 --mode sync` on ExportKit 2.1 / Ubuntu 24.04 reportedly waited 30 seconds in 2 of 3 attempts. An immediate return was expected.

3. The command and environment are recorded; the behavior has not been independently verified. Replacing zero with a default timeout is the reporter’s unconfirmed suspicion. Source access was denied, and no source, tests, logs, PR or alternate copy was accessible. The cause and fix remain unknown.

4. Async export is out of scope.

5. Mina must obtain an accessible v2.1 source snapshot. A reproduction and cause-confirmation owner still needs assignment. Once source is available, reproduce on the reported version and compare timeout handling before choosing a fix.
