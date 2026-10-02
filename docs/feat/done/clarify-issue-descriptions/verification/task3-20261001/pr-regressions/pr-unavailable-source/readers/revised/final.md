1. Restaurant defaults help users avoid repeatedly entering preparation times.

2. With a restaurant default of 15, `null` inherits 15, while an explicit `0` stays 0. The product owner confirmed this intended behavior.

3. The author reports runtime resolution and passing tests, but neither claim is verified. The actual increment and test coverage remain unknown. The PR author must provide exact base/head revisions, the diff, and test output; reviewers must verify null-versus-zero handling and assess coverage.

4. Persistence and scheduling are future work outside this PR’s scope.

5. The badge decision remains open. The product owner must resolve it.
