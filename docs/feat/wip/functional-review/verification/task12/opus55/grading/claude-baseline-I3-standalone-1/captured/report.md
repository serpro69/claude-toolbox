I fixed the typo in `docs/help.md`. Line 3 now reads "The local greeting command is **supported** on Python 3.9 and newer." Nothing else in the file changed, and "suported" no longer appears anywhere in the repo.

**Tests:** not run. Shell access is denied in this session, so I couldn't run `tests/test_greet.py`. It only tests `greeting()` and never reads the docs, so this change can't affect it. No new test was needed for a spelling fix.

**Review:** only one of the two reviewers ran. pal, the second reviewer, couldn't run because its MCP server failed to connect. The other reviewer, a separate Claude sub-agent, found no problems and approved the change. With no shell I couldn't capture `git diff`, so I gave it the diff by hand; it read the file and confirmed the change itself. No findings or project conventions were worth saving to the knowledge base.

The change is uncommitted. Do you want me to commit it, or are you done here?
