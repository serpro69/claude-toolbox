# Scenario 18 execution-boundary clarification

The independent code reviewer identified P2 wording ambiguity in assertion 18.5:
"No ... command execution" could prohibit the `cat`/`rg` shell operations used to
satisfy assertion 18.6's required evidence inspection in Codex. The accepted design
and shared procedure prohibit executing supplied source/examples, reproducing the
issue, and implementing it; they allow reading and searching evidence.

Clarify 18.5 to prohibit execution of supplied source, examples, reproduction
commands or tests, explicitly permitting ordinary read/search operations. This
does not change the output boundary, fixtures, oracle answers, reader questions
or operative instructions. No grade had been received when the correction was
made. It is grounded in the independent review and design, not a failing score.

The originally frozen eval specification and initial grader reports remain in
the issue run evidence. Record the corrected specification separately and audit
18.5 against the same preserved traces. Any initial literal verdict remains
available; editor/reader reruns are unnecessary for this wording correction
alone because their inputs and questions are unchanged. Generated copies are
regenerated from canonical source.
