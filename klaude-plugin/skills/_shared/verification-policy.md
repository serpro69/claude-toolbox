# Proportionate verification

Verification supports a decision about agreed behavior. Exhaustive instruction
compliance can reject useful agent outcomes and encourage ever longer prompts
without improving the product.

- Tie checks and blocking criteria to an explicit requirement or consequential
  risk. Separate material failures, quality observations, and evidence limits.
  Optional advice, report formatting and harmless procedural variation are not
  automatic blockers. An accurately explained bug can suffice without a proposed
  follow-up; the human or implementing agent can choose the next action.
- Preserve applicable repository checks and explicit acceptance requirements.
  Test deterministic invariants directly. For LLM evaluations, assess semantic
  outcomes across representative cases and report variability and uncertainty;
  two successes do not establish reliability, and one failure does not establish
  a regression. A demonstrated serious failure can still justify stopping.
- Before changing instructions to fix an eval, inspect the fixture, grader and
  actual consequence. Accept valid alternative approaches. Require exact wording
  or tool order only where it protects a stated contract. Include a benign control
  when a change could produce unnecessary work or false blockers.
- Declare the comparison, decision criteria and bounded effort before measuring.
  Compare a targeted instruction change with its immediate predecessor under
  matching conditions; a pre-feature baseline answers a broader question.
  Keep all attempts. Expand sampling only to answer a named uncertainty that
  could change the decision, not until a run happens to pass.
- Missing tools or traces limit the claim; they are neither proof of failure nor
  successful verification. Distinguish unavailable execution from an available
  required check left undone. Never claim unrun tests passed.
- Prefer existing focused checks. Broaden for affected shared behavior, concrete
  unresolved risks or required release checks. Stop after sufficient verification
  unless new changes or evidence justify more. Consider replacing or removing
  instructions before adding obligations; count the full loaded guidance and
  workflow cost, not only the edited paragraph.
- Grade observations separately from adoption. A FAIL remains a FAIL under its
  rubric without automatically vetoing the feature. When authorized to correct an
  unjustified gate, record the superseding decision and update live completion
  criteria; retain historical grades. Do not keep a retired gate blocking under
  another name or silently weaken a real requirement.
