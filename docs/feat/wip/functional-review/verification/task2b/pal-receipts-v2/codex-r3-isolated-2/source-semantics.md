# Existing PAL successful-read evidence

This supplement supersedes the interpretation in `pal-receipts/`. That first
supplement's history-inclusion marker alone cannot prove source receipt: PAL
also returns nonempty formatted error text when a file cannot be read. Its
original evidence and grades remain preserved as superseded records.

The installed `utils/file_utils.py` and `utils/conversation_memory.py` match
revision `c20d384a9c5a38ab8d58c780d2e269c537e409fa`. Each sealed supplement
retains both source hashes and focused excerpts. The new collector requires
three consecutive, exact metadata records for the same owned path:

1. `Successfully read N characters from <path>` after the UTF-8 read returns.
2. `Formatted content for <path>: N chars, T tokens` after formatting succeeds.
3. `File embedded in conversation history: <path> (T tokens)` after that
   formatted content is appended to the history's file-content list.

The successful-read count must equal the character count of the immutable
dispatch snapshot, with PAL's decoding/newline semantics. Formatting and
embedding token counts must agree. All three timestamps must be ordered and
fall within the same actual PAL expert invocation; the owned path must appear
in exactly one matching invocation/window. Captured start/completion payloads
must have one stable hash. These checks bind the observed read to the sealed
source by unique path, time and count; the runtime log does not itself contain
a cryptographic content digest. A read, formatting or access error is not a
successful receipt under these rules.

The final response's `files_embedded: 0` counts newly embedded request files;
continuation history separately includes referenced files from earlier turns.
The history excerpt shows the joined file contents being appended to the
history supplied to the continuing review. Neither that counter nor a read
request alone establishes receipt. Reviewer use still requires evidence in its
actual result, and exact submitted model prompts remain unverified.

The collector reads the existing local log only, validates a digest of its
prefix, and exports only these three strict metadata patterns. No raw log,
prompt, response, credential, private reasoning or unrelated line is exported
or supplied to graders. The Europe/Oslo clock was UTC+02:00 on 2026-10-10.
No actor rerun, hook, server patch, interception or runtime configuration change
produced these records. Automatic approval previously rejected full-log
processing through Capy; that operation was not performed. This collection
uses only the locally validated, nonsensitive metadata instead.
