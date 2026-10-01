1. Large synchronous exports keep users waiting. The feature would let users continue working while an export is prepared and download it later.

2. A user starts an export of selected rows, keeps working, then downloads a CSV containing those rows in their original column order. Today, CSV generation is synchronous.

3. The continuation-and-download outcome is accepted. The only agreed acceptance criterion is preservation of selected rows and column order. Arun proposed a background queue and download token, but Mira has not approved that mechanism. Nothing is implemented; no runtime test results are available.

4. Notifications are out of scope. Performance targets and row caps remain unagreed; the artifact does not explicitly exclude them.

5. Mira must decide download expiry before implementation. After that, the export maintainers choose the mechanism.
