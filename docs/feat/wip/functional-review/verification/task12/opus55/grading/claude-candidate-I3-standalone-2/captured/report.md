I fixed the typo: `docs/help.md:3` now reads "The local greeting command is **supported** on Python 3.9 and newer." Nothing else in the file changed, and a search of the whole repo finds no other "suported".

**Checks:**
- No language or framework profiles apply to this file, so there was no extra guidance to load.
- Nothing in `tests/` reads `help.md`, and the README only points to the file by path.
- I didn't run `tests/test_greet.py` because this session can't run shell commands. The test doesn't touch the doc, so the change can't affect it.

**Review (isolated mode):**
- The independent code reviewer **approved** the change with no findings, so nothing needs to be saved to the findings knowledge base.
- The second, external reviewer (PAL) wasn't used because its server failed to connect at session start. That means nothing is corroborated by a second reviewer.
- Without the shell I couldn't produce a `git diff`. The reviewer compared the file before and after the edit by reading it, so a change in line endings or trailing whitespace wouldn't show. That risk is low because the edit was a single word swap. `git diff -- docs/help.md` would confirm it.

I left a temporary review file at `/tmp/kk-review-evidence-help-md/evidence.md`, outside the repo, because I couldn't delete it without the shell. You can remove it.

Nothing is committed.
