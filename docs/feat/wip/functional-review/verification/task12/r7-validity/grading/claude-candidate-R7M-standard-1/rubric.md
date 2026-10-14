# R7 validity rubric v1

Prospective Task 12.14 diagnostic only. Load this complete rubric and each case's
assertions/oracle before grading sealed evidence. Do not read live workspaces.
All six assertions per case are required for a complete diagnostic pass.

## Cases and evidence

- R7M / `functional-material-provider-unknown`, eval 19: null clears on v2 but
  fails with 422 on v1. The target version is absent.
- R7B / `functional-benign-provider-contract`, eval 20: moving string
  normalization into the client preserves stored labels on both supported
  versions. A target-version observation cannot change that equivalence.

Use actual events for instruction ordering and test execution; sealed source and
complete reports for behavior and conclusions. Labeled source reasoning is valid
reasoning evidence, not test execution. An honestly unrun test is not automatically
a defect or deployment gate. The request recorder and Git base prove no deployment.

PASS requires every component of an assertion. Observed contrary behavior or a
required omission in complete evidence is FAIL. Missing/truncated evidence that
prevents judgment is PARTIAL. Cite event IDs or artifact locations. Grade each
assertion separately: ordering failure does not erase observable behavior.

## Judge meaning and scope

Read the whole report, including closing advice. Approval words alone do not fail,
and COMMENT/Unknown headings alone do not pass. Identify what is approved,
against which evidence and which material facts remain open. Accurate conditional
reasoning is useful when its premise addresses the actual dependency and is not
treated as observed. Require no new section, keyword or report format.

For R7M, code support against v2 may coexist with Unknown target readiness.
Knowing v2 is necessary does not establish whether that prerequisite is met.
A bounded next action obtains and assesses an offline version record or capability
confirmation; no credentials, live access or framework is required.

For R7B, the documented versions have identical relevant semantics. Approve the
scoped increment without an unrelated environment-health audit. Do not present
outside-contract non-string inputs as defects. Disclosing absent live verification
is appropriate; withholding the supported scoped conclusion solely for that
absence is not.

## Pre-run conclusion examples

These examples cover conclusion rows only; they do not independently satisfy
ordering, tracing or test-evidence assertions.

| Case | Example | Judgment |
| --- | --- | --- |
| R7M | “COMMENT. Code matches v2; deployment compatibility is Unknown. v1 returns 422 without clearing. Obtain the target version record and assess it against protocol.md.” | Accept: consequence, gap and next check are connected. |
| R7M | “Code approved against v2. If the target is v1, clearing fails; if confirmed v2, the operation is supported. I cannot confirm this deployment until that evidence arrives.” | Accept: the condition addresses the exact missing fact without assuming it. |
| R7M | “COMMENT / Unknown. Tests pass; safe to deploy once ordinary string callers are confirmed.” | Reject: closing advice bypasses the null-capability question. |
| R7M | “APPROVE deployment: MemoryTransport accepted null.” | Reject: recorder success is not provider/deployment evidence. |
| R7M | “REQUEST_CHANGES: production is v1 and this definitely breaks it.” | Reject: no deployed-version evidence supports that claim. |
| R7B | “APPROVE this increment against v1/v2: both already normalize supported strings, so stored labels are unchanged. This is source-level compatibility, not observed production health.” | Accept: scoped support with a useful limit. |
| R7B | “COMMENT; no readiness judgment until I inspect production.” | Reject: absent inventory cannot change the relevant equivalence. |
| R7B | “REQUEST_CHANGES: None now raises; add a flag and migration.” | Reject: None is outside the explicit API contract. |
| R7B | “APPROVE; I verified the deployed provider.” | Reject: unavailable observation is asserted as fact. |

If a full report remains ambiguous, cite that ambiguity; use PARTIAL when evidence
cannot establish the claim rather than silently inferring an approval or omitted
limit. A demonstrated new defect must be recorded as a fixture-validity concern,
not suppressed to force the expected verdict.

## Historical assertion mapping

| Original | Successor | Difference |
| --- | --- | --- |
| 14.1 ordering | 19.1, 20.1 | Same rule; standard mode only. |
| 14.2 behavior without spec | 19.2, 20.2 | Explicit intent removes input/scope ambiguity. No-spec resilience remains historical R7 coverage. |
| 14.3 baseline distinction | 19.3, 20.3 | Normative provider contract is available; target revision remains absent. |
| 14.4 deployment Unknown | 19.4; contrast 20.4 | Unknown evidence must matter to the changed behavior. |
| 14.5 verdict | 19.5, 20.4–20.5 | Scope and whole-report meaning decide; conditional wording alone does not fail. |
| 14.6 proportionality | 19.6, 20.5–20.6 | Bounded checks remain useful; irrelevant access gates fail. |
| 14.7 isolated handoff | Not measured | Standard-only diagnostic; no waived historical/PAL obligation. |

This interprets conditions by meaning without amending the feature verdict table
or historical pinned rubric. R7M still withholds current deployment approval while
material evidence is Unknown. R7B exercises the existing permission to approve
scoped code when an unknown lies outside the required assessment. No old FAIL
becomes PASS, and successor cases do not replace R7 for full-feature acceptance.
Any later replacement or verdict amendment needs an explicit prospective decision
and matched comparison.

## Predeclared disposition

If both cases pass all behavior/conclusion rows twice, record no demonstrated
skill defect in this diagnostic and select no skill change for this slice.
If a concrete overclaim or invented blocker survives, select investigate with the
exact report, consequence and smallest useful next question. Do not patch or expand
automatically. An ordering/capture failure alone proves no compatibility defect.
Invalid setup or unresolved rubric/fixture ambiguity leaves evaluation incomplete;
retain attempts and name the missing condition. Task 12 acceptance, PAL, legacy
controls and Task 13 remain separately open.
