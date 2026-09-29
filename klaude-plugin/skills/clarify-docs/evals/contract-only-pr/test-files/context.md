# PR context

Target: synthetic kitchen repository. Intended audience: its established reviewers;
all checkout files are tracked and unrestricted. The staged Git repository at
checkout/ has actual refs review-base and review-head; review-head is checked out.
PR base is review-base, head is review-head. Inspect those refs and their diff.
The branch/stack label is `runtime-complete` (editorial metadata, not evidence).
Requirements are in checkout/requirements.md. Validation record: contract JSON
parsed successfully; no runtime tests or deployment were performed.
