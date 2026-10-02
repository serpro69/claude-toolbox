# Grader trace audit

The independent default grader ran in fresh thread
01a0fbc5-b45e-7330-b698-251b588d7a78 with fork_turns=none and no override. Its
saved prompt and pre-dispatch JSON match byte-for-byte (one terminal LF), and
the dispatch receipt/ciphertext links to the incoming task. The complete visible
export has 19 tool calls with 19 responses, a final answer and completion event.
Model/settings match the editor/readers: gpt-6-astra, max effort, default mode.

The grader loads its manifest at ordinal 14, protocol/cohort/current instructions
at 19, and every fixed eval/oracle at 24 before artifact judgment. All filesystem
reads are from the exact manifest, plus the explicitly permitted self-authored
verdict. It never reads native logs, canonical outside paths, installed skills,
or temporary workspaces. All shell calls use login:false. The only write is
native apply_patch at 129 creating grading/verdicts.json. Two internal progress
messages go to the parent; there is no external/network call or delegation.

Ordinal 32 contains a truncated aggregate metadata presentation, which is retained
unchanged. Recovery is explicit in subsequent reads/checks: ordinal 45 rereads
the source/reader/manifest maps; 50/55 load all relevant artifact and answer bytes;
62/69 inspect every editor call, output and visible message; 83 does the same for
all readers. Exact already-read instruction/artifact strings are replaced only
with verified byte-equality markers in those presentations. Ordinal 92 reads all
287 allowlisted files and independently recomputes hashes, snapshots, complete
decoded trace coverage, call/response pairing, finals, prompts, settings and
dispatch linkage. Ordinal 99 distinguishes derived JSON whitespace from retained
original visible-record bytes and inspects retry/slot evidence; 106 replays all
eight patches, checks decoded trace equality and the invalid attempt; 120 checks
all incoming author/recipient links. Thus the initial truncated aggregate is not
the sole evidence for any grading conclusion. No final editor/reader output is
truncated or missing.

The final validation at 136 confirms all 47 fixed assertion IDs exactly once,
47 PASS / 0 FAIL / 0 PARTIAL, and valid evidence references/ordinals. The
coordinator independently checked the saved JSON against the frozen cohort and
confirmed every assertion has a rationale and evidence. No operative fix is
requested. The invalid initial case-17 editor and unlaunched case-18 scheduling
attempt stay separate from the final PASS totals.
