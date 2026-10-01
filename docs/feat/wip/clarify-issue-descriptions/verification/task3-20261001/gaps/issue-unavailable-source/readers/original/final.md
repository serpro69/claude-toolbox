1. The issue exists because requesting a zero timeout sometimes produces a 30-second wait, delaying invoice checking.

2. On ExportKit 2.1 / Ubuntu 24.04, `exportctl send invoice-21 --timeout-ms 0 --mode sync` reportedly waited 30 seconds in 2 of 3 attempts. Immediate return was expected.

3. The command and environment are recorded. The observed behavior is reported, with no independent reproduction established. Replacing zero with a default is a suspected cause, not confirmed. The v2.1 source still needs to become accessible.

4. Async export is out of scope. No fix has been agreed.

5. Mina owns obtaining accessible v2.1 source. Once available, the next steps are to reproduce on the reported version and compare timeout handling before choosing a fix. Nobody owns reproduction or cause confirmation yet.
