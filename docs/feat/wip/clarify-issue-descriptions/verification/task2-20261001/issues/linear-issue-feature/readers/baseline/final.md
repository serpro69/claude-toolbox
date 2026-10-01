1. Large CSV exports currently run synchronously and keep users waiting. The feature would let users continue working while an export is prepared.

2. A user starts an export of selected rows, continues working, and later downloads a CSV containing the originally selected rows in their original column order.

3. The continuation-and-download outcome is accepted. The only agreed acceptance criterion concerns CSV contents and column order. Arun’s background queue and download token are proposed, not approved. The feature is not implemented.

4. Notifications are explicitly out of scope. No performance target or row cap has been agreed; the draft does not explicitly exclude them.

5. Mira must decide download expiry before implementation. Maintainers can then choose the mechanism.
