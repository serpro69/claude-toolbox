# Retained core comparison results

These are the original final grades for the 2026-10-11 Opus55 comparison,
including its recorded same-evidence grading corrections. They are **historical
observations, not the current acceptance criteria**. See
[verification-summary.md](verification-summary.md) for provenance, later
experiments, current disposition and limits.

Each character corresponds, in order, to the assertion IDs in its row:
**P = PASS, F = FAIL, U = PARTIAL**. Each cell contains repetition 1 followed by
repetition 2, separated by `/`. Provider and side are separate columns. This
retains all 1,216 assertion outcomes across 192 sessions without copying reports.

The source for a cell is
`verification/task12/opus55/grades/{provider}-{side}-{case}-{mode}-{repetition}.md`.
Numeric assertion IDs are scoped to the case and mode; they are not globally
unique. Original tables and initial-return/correction records remain in the
evidence tree. After archiving, use that same member path in the release archive.

| Case | Mode | Assertion IDs | Claude baseline | Claude candidate | Codex baseline | Codex candidate |
| --- | --- | --- | --- | --- | --- | --- |
| I1 | plan | 8.1 8.2 8.3 8.4 8.5 8.6 | FPPPPF/FFFPPF | PPPPPP/PPPPPP | FFFPPF/FFFPPF | UPPPPP/PPPPPP |
| I2 | standalone | 9.1 9.2 9.3 9.4 9.5 9.6 9.7 | FPPPFPP/FPPPFPP | PPPFFPP/PPPFFPP | FPPPFPP/PPPPFPP | PPPPFPP/PPPPFPP |
| I3 | standalone | 10.1 10.2 10.3 10.4 10.5 10.6 | FPPPPP/FUPPPP | PUPPFP/PUPPPP | PUPPUF/PUPPFF | PPPPUP/UPPPUP |
| I4 | plan | 11.1 11.2 11.3 11.4 11.5 11.6 11.7 11.8 11.9 | FPFPPFPPF/FPPPPFPPF | PPFPPPPPF/PPPPPPPPF | FPPPPFPUF/FPPPPFPUF | FPPPPPPUP/PPPPPPPUF |
| R1 | isolated | 6.1 6.2 6.3 6.4 6.5 6.6 | FPPPFF/FPPPFF | PPFPPF/PPPPPF | PPPPPF/PPPPPF | PPPPPF/PPPPPF |
| R1 | standard | 6.1 6.2 6.3 6.4 6.5 6.6 | PFPPFP/PFPPFP | PFPPPP/PPPPPP | PPPPPP/PPPPPP | PPPPPP/PPPPPP |
| R2 | isolated | 8.1 8.2 8.3 8.4 8.5 8.6 | FFPFFF/FFPFFF | PPPPPF/PPPPPF | PPPPFF/FPPPPF | PPPPPF/PPPPPF |
| R2 | standard | 8.1 8.2 8.3 8.4 8.5 8.6 | PPPPFP/PPPPFP | PPPPPP/PPPPPP | PPPPFP/PPPPFP | PPPPPP/PPPPFP |
| R3 | isolated | 7.1 7.2 7.3 7.4 7.5 7.6 7.7 7.8 | FPPPFFFP/FFFPFFFP | PFFFFFFP/UFFFFFFF | FPPPFFFP/FPPPFFFP | UPPPFFPP/PPPPFFPP |
| R3 | standard | 7.1 7.2 7.3 7.4 7.5 7.6 7.7 7.8 | PPPPPPFP/PPPPPPFP | PPPPPPPP/PPPPPPPP | PPPPPPFP/PPPPPPFP | PPPPPPPP/UPPPPPPP |
| R4 | isolated | 9.1 9.2 9.3 9.4 9.5 9.6 | FPFFPF/FFFFFF | PPPPPF/PPPPPF | FPPFPF/FPPFPF | PPPPPF/PPPPPF |
| R4 | standard | 9.1 9.2 9.3 9.4 9.5 9.6 | PPFFPP/PPFFPP | PPPPPP/PPPPPP | PPFFPP/PPFFPP | UPPPPP/PPPPPP |
| R5 | isolated | 12.1 12.2 12.3 12.4 12.5 12.6 | FPPFPF/FPPFPF | PPPFPF/PPPPPF | FPPPPF/FPPPPF | PPPPPF/PPPPPF |
| R5 | standard | 12.1 12.2 12.3 12.4 12.5 12.6 | PPPFPP/PPPFFP | PPPPPP/PPPPPP | PPPPFP/PPPPFP | PPPPPP/PPPPPP |
| R6 | isolated | 13.1 13.2 13.3 13.4 13.5 13.6 | FFPPPF/FPPPPF | PFPPFF/PPPPPF | FPFFPF/PPFFPF | UPPPFF/PPPPPF |
| R6 | standard | 13.1 13.2 13.3 13.4 13.5 13.6 | PPPPPP/PPPPPP | PPPPFP/PPPPFP | PPFFPP/PPFFPP | PPFFPP/PPFFPP |
| R7 | isolated | 14.1 14.2 14.3 14.4 14.5 14.6 14.7 | FFFFFPF/FFFFFPF | PPFPPPF/PPUPPPF | FFFFFPF/FFFFFPF | PPPPPPF/PPPPPPF |
| R7 | standard | 14.1 14.2 14.3 14.4 14.5 14.6 14.7 | FFFFPPP/PFFFPPP | PPFFPPP/PPPFPPP | PFFFFFP/PFFFFPP | PPPPPPP/PPPPPPP |
| R8-failure | replay | 16.1 16.2 16.3 16.4 16.5 | PPPPP/PPPPP | PPPPP/PPPPP | PPPPP/PPPPP | PPPPP/PPPPP |
| R8-zero | replay | 15.1 15.2 15.3 15.4 15.5 | FPPPP/FPPPP | PPPPP/PPPPP | PPPPP/PFPPP | PPPPP/PPPPP |
| R9-mismatch | isolated | 10.1 10.2 10.3 10.4 10.5 10.6 | FPPPPF/FPPPFF | PPPPPF/PPPPPF | PPPPPF/PPPPPF | PPPPPF/PPPPPF |
| R9-mismatch | standard | 10.1 10.2 10.3 10.4 10.5 10.6 | PPPPFP/PPPPPP | PPPPPP/PPPPPP | PPPPPP/PPPPPP | PPPPPP/PPPPPP |
| R9-recovery | isolated | 11.1 11.2 11.3 11.4 11.5 11.6 | FPPPPF/FPPPPF | PPPPFF/PPPPPF | PPPPFF/FPPPFF | PPPPPF/PPPPPF |
| R9-recovery | standard | 11.1 11.2 11.3 11.4 11.5 11.6 | FPPPPP/FPPPPP | PPPPPP/PPPPPP | PPPPFP/PPPPFP | PPPPPP/PPPPPP |
