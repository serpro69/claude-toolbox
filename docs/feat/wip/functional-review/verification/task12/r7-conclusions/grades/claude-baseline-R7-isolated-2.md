| id | verdict | evidence |
|----|---------|----------|
| 14.1 | FAIL | Main reads the full diff at e77/e80 after the checklist index e73, without reading the four resolved checklists; their successful reads e92–e101 belong to the child. |
| 14.2 | FAIL | e104/e107 inspect `save` and MemoryTransport, but e142 and captured/report.md omit inferred normalization intent and an explanation of preserved internal whitespace and payload shape. |
| 14.3 | FAIL | captured/report.md uses passing local tests to support shipping without distinguishing the Git review base and MemoryTransport from a released/deployed provider baseline. |
| 14.4 | FAIL | e142 answers “Probably yes” and “fine to ship”; missing server rules are acknowledged, but deployment is not assessed as Unknown with a bounded evidence-gathering action. |
| 14.5 | FAIL | The child returns COMMENT at e120, but the final report e142 replaces it with “Probably yes” and conditional shipping advice rather than an unambiguous non-approval verdict. |
| 14.6 | PASS | e113 searches existing callers; e142 identifies caller input and undocumented empty/null-name contract questions, offering small guard/test changes without access or rollout demands. |
| 14.7 | FAIL | manifest.json declares isolated mode; e86 dispatches `kk:code-reviewer`, but event-index.json contains no PAL dispatch/result, and e85/e142 disclose that PAL never ran. |

**Summary**: 1 PASS / 6 FAIL / 0 PARTIAL of 7 assertions.
