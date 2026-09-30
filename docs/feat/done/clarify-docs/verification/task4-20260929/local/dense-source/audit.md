# Coordinator trace audit

Executed: editor, original reader and revised reader. All were fresh default general-purpose agents with `fork_turns="none"`; only one local child ran at a time. Exact requests, spawn text, session metadata, visible messages and paired tool calls/results are retained beside this file. Reader comparison uses identical fixed questions and oracle-declared `guide.md` paths.

Observed read boundary: editor read its request, the copied clarify skill and full shared procedure, then only `guide.md`, `requirements.md` and `prep.py`. The full procedure returned before the target/source reads. Each reader read its own request and its own `guide.md` only. No oracle, other version or source-only evidence was read by either reader. All tool calls have captured results: editor 6/6, original reader 2/2, revised reader 2/2.

Hash comparison shows only `guide.md` changed. No extra workspace artifact was created. Filesystem boundaries are prompt-enforced and trace-audited, not OS-isolated. These results measure AI-reader behavior, not human comprehension.

Execution-method limitations: initial request reads used the default login shell before the request's `login:false` instruction was available, producing a denied navi log-initialization warning. No out-of-manifest subject content appeared. The editor used a shell heredoc for its staged document instead of native `apply_patch`; later requests explicitly require native `apply_patch`. The original request and trace are preserved unchanged. These limitations do not demonstrate subject-content leakage; independent grading remains separate.
