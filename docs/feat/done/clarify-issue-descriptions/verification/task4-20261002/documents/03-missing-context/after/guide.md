# Export storage

The export feature is intended to give service owners a downloadable record of
completed orders. Under the accepted contract, each export request creates one CSV
and returns its download link. Scheduled exports are outside this increment.

Implementation is not supplied, so this guide describes the accepted contract;
running behavior has not been verified.

Cleanup timing and retention duration cannot yet be documented because the
retention decision in `retention.md` is unavailable. The data steward must supply
that decision before cleanup behavior can be documented.
