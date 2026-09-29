# Export storage

The accepted export contract gives service owners a downloadable record of
completed orders. Each requested export will create one CSV and return its download
link. Scheduled exports are outside this increment. Implementation was not supplied,
so this describes the accepted contract, not verified running behavior.

Cleanup timing cannot yet be documented because the required retention decision in
`retention.md` is unavailable. The data steward must supply that decision before
cleanup behavior can be documented; no retention duration can be inferred.
