---
title: Benchmarks
description: >-
  How the Agentstakk review step compares with plain Claude Code on the same
  model, on synthetic evals and on real reviews replayed from capy.
---

# Benchmarks

Agentstakk runs code review as one step of the development workflow:
`/kk:implement` finishes each task with `/kk:review-code`. These benchmarks
measure that step against plain Claude Code on the same model. Scripts, data,
transcripts and grades are in
[serpro69/agentstakk-bench](https://github.com/serpro69/agentstakk-bench).

## Results

| Benchmark | Inputs | Result |
|---|---|---|
| Synthetic evals | 5 fixtures, each with one seeded defect and its contract in a README | No difference: both found every defect |
| capy replay | 5 real review dispatches from [capy](https://github.com/serpro69/capy), replayed from archived sessions | Plain Claude Code found **36%** of the findings the review reported and the author kept, and no real issue the review missed |

Small fixtures with an explicit contract make every defect obvious, so they
can't separate the two. Real tasks can.

## The capy replay

capy was built with Agentstakk, and every one of its tasks went through
`/kk:review-code`. capy's session vault keeps the full transcripts. From each
of five isolated reviews, the benchmark takes:

- the exact diff the reviewer received;
- what the review reported;
- which findings the author fixed or kept, and which they rejected.

Plain Claude Code then reviewed the same staged change twice. It ran headless
on the original session's model (Opus 4.6), without the Agentstakk plugin,
skills, hooks or MCP servers, and got the same task context.

| | Plain Claude Code, Opus 4.6, 2 runs per case |
|---|---|
| Valid findings found | 10 of 28 (36%), 13 of 28 with partial matches |
| Real issues the review missed | 0 |
| Extra findings | 5 minor, 5 dubious |

The findings came from both of the review's reviewers:

- 11 of 14 from the internal Claude reviewer, which runs the profile checklists;
- 3 only from the external model (Gemini via PAL).

One of those three was the only security finding, a field written to the
search index without secret sanitisation. Both plain runs approved that change.

## Limits

- **Sample.** Five cases, two plain runs each, and results varied between
  runs. On one case, the two runs found 1 and 3 of 5 findings.
- **Answer key.** It comes from the review being measured. The fair claim is
  "plain found 36% of what the review found", not a symmetric recall
  comparison.
- **Harness.** The plain runs used today's Claude Code, which includes
  built-in review tooling the original sessions didn't have. That favours
  plain.

The [benchmark README](https://github.com/serpro69/agentstakk-bench#readme)
lists every caveat, and
[RESULTS.md](https://github.com/serpro69/agentstakk-bench/blob/master/capy-replay/RESULTS.md)
has every finding.
