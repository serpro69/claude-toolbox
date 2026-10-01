1. The feature lets users keep working while a CSV export is prepared. Current synchronous exports make users wait on the request, especially for large exports.

2. A user selects rows, starts an export, continues working, and downloads the CSV when ready. The CSV must contain the originally selected rows in their original column order.

3. Continued work and later download are accepted intent; CSV fidelity is the only agreed acceptance criterion. Arun’s background queue and download token are proposed, unapproved options. The feature is not implemented; current source is revision `export-2.1`.

4. Notifications are out of scope. No performance target or row cap has been agreed.

5. Mira must decide download expiry before implementation; no duration is agreed. After she records that decision, the export maintainers choose the mechanism.
