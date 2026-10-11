I fixed the typo in `docs/help.md:3`: "suported" is now "supported" and the rest of the line is unchanged. It was the only "suported" in the repo.

```
-The local greeting command is suported on Python 3.9 and newer.
+The local greeting command is supported on Python 3.9 and newer.
```

**Tests:** I didn't run any, because Bash is blocked in this session. The only test, `tests/test_greet.py`, checks the greeting function and doesn't read `docs/help.md`, so this change can't affect it. No new test makes sense for a spelling fix in a doc.

**Review:** only partly done.
- **Code-reviewer sub-agent:** approved with no findings.
- **pal codereview:** didn't run because the pal server failed to connect. If you want the second reviewer, reconnect it and re-run `/kk:review-code`.
- Nothing was worth saving to the knowledge base: no review issues and no new project conventions.

The change is in your working tree on `master` and isn't committed. Should I commit it, or leave it as is?
