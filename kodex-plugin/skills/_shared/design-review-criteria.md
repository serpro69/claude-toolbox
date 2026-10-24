## Design review criteria

Shared checks for reviewing a feature's design documents: `design.md`, `implementation.md` and `tasks.md` under its feature directory. Every reviewer, internal or external, reads this file and the shared verification policy (supplied alongside it) before opening the documents they assess. These files are methodology, not review targets.

The documents are proposals. Code they describe as to-be-created or to-be-modified is planned work: assess whether the plan is specific enough, never report that the code does not exist yet. Where a document references code, patterns or files that it says already exist, verify them against the repository with read-only inspection and report inaccurate references.

Finding type codes name the category a check produces: `INCOMPLETE` (insufficient detail), `INCONSISTENT` (documents contradict), `TECH_RISK` (unaddressed failure mode, scalability or edge case), `MISSING` (absent cross-cutting concern), `AMBIGUOUS` (several reasonable readings) and `STRUCTURE` (convention not followed). A reviewer with its own output contract keeps its native format and severity and may cite the code as the category.

### Scope

- Review only the documents in scope. A document that is out of scope or missing is neither reviewed nor reported as a defect of the others; skip the checks conditioned on it and report the omission as a coverage limit.
- Checks marked with a document name apply only when that document is in scope.

### Document quality

Evaluate each in-scope document:

- **Completeness** — Is the design detailed enough for an experienced developer with zero codebase context? Are file paths, function names and components explicitly named where appropriate?
- **Clarity** — Are requirements unambiguous? Could a developer follow the plan without asking clarifying questions?
- **Internal consistency** — Does each document agree with itself (a design that says "3 endpoints" then describes 2)?
- **Convention adherence** — Does the document structure follow the expected conventions? Are sections well organized?
- **Subtask quality** (`tasks.md`) — Are subtasks specific enough? Do they name the file, function or component being touched? Are dependencies between tasks correct?
- **Assumptions and Not Doing** (`design.md`) — Is there an **Assumptions** section with specific, testable assumptions rather than vague hedges ("the API is fast enough")? Is there a **Not Doing** section whose exclusions carry rationale? Either section missing → `STRUCTURE`.
- **Task format conventions** (`tasks.md`):
  - **Not Doing** in the header metadata. Missing → `STRUCTURE`.
  - **Size tags** on every task. Missing → `STRUCTURE`. A task tagged L that has not been broken down → `STRUCTURE`.
  - **Vertical slicing** — tasks that look like horizontal layers ("all models", "all endpoints", "all tests", or completing an entire architectural layer without a testable user-facing path) → `TECH_RISK`.
  - **Parallel markers** (`Can run in parallel with:`) on every task. Missing → `STRUCTURE`.
  - **Dependency graph** section. Missing → `STRUCTURE`.

### Technical soundness

Evaluate the proposed architecture:

- **Viability** — Will the design actually work? Are there logical flaws in the approach?
- **Edge cases and failure modes** — Which unaddressed scenarios could break the implementation?
- **Trade-offs** — Are trade-offs stated and well reasoned? Are there simpler alternatives not considered?
- **Scalability** — Does the design consider growth? Are there bottlenecks?
- **Testing strategy** — Apply the loaded verification policy to coverage, acceptance gates, comparisons and stopping conditions. Challenge disproportionate verification as well as missing consequential checks.
- **Migration and rollback** — If the feature changes existing behavior, is there a migration path? Can it be rolled back?
- **Assumptions testability** (`design.md` Assumptions) — Are assumptions specific enough to be tested or falsified? "The API is fast enough" → `AMBIGUOUS`; "the external API responds within 200ms at p99" → pass.
- **Not Doing validity** (`design.md` Not Doing) — Are exclusions genuine scope decisions rather than deferred critical requirements? An exclusion that would block the feature from being usable → `TECH_RISK`.

### Feature value

- Does the feature improve the situation for its end users, and does the approach solve the stated problem rather than an adjacent one?
- Is success observable: would anyone be able to tell that it worked?
- Unstated or unverifiable value → `AMBIGUOUS`; a consistent design that does not deliver its stated value → `TECH_RISK`.

### Cross-document consistency

When more than one document is in scope:

- Do `design.md` and `implementation.md` agree on architecture, file structure and approach?
- Do the task descriptions in `tasks.md` reflect what `design.md` and `implementation.md` specify?
- Are there requirements in one document that another does not address?

### Self-check

For each candidate finding: re-read the relevant section; ask "Could I be misreading the document?" and check other sections for context that addresses the concern; ask whether it is genuinely a problem or a different-but-valid approach; state the confidence and the reasoning behind it; drop findings that do not survive.
