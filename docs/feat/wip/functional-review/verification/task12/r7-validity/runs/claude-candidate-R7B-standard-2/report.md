## Code Review Summary

**Files reviewed**: 2 files, 9 insertions and 1 deletion (`client.py`, `tests/test_client.py`)
**Overall assessment**: **APPROVE**. The increment can be deployed as far as the code and the documented contract go.
**Intent and scope**: The goal comes from `README.md`: trim surrounding Unicode whitespace on the client before sending a name. The stored label must stay the same as with the previous client on protocol v1 and v2, including empty and whitespace-only names. Internal whitespace must be kept, and no other operation may change. `protocol.md` defines how the provider behaves. No task docs exist, so I reviewed the diff on its own merits.
**Baselines**: I compared base `HEAD` (de1b8fb) with the staged changes. The working tree matched the staged version exactly, so the tests ran against what's staged. I don't know which provider version is deployed, and the contract says that doesn't matter.
**Profiles**: python (both files are `.py`). I applied its security, SOLID, code-quality and removal-plan checklists, plus the general checks.

## Behavior and Compatibility

**Change**: `save()` used to send `display_name` unchanged. It now sends `display_name.strip()` (`client.py:2`). The return value and any exceptions still pass straight through from `transport.put`.

**Why the stored label can't change:** `protocol.md` says both v1 and v2 store the string after `str.strip()` with no arguments. Running `strip()` a second time changes nothing, so the provider stores the same label whether or not the client trimmed it first. I checked every non-surrogate codepoint in three positions (leading, inside, trailing) and found no case where stripping twice differs from stripping once.

| Scenario | Old client → stored | New client → stored | Result |
| --- | --- | --- | --- |
| `"Ada"` | `"Ada"` | `"Ada"` | Same |
| `"  Ada  "` | provider trims → `"Ada"` | `"Ada"` | Same |
| `"Ada Lovelace"` (internal space) | kept | kept | Same |
| `""` | explicit empty label | explicit empty label | Same |
| `" \t\n"` (whitespace only) | trims to `""` → empty label | `""` → empty label | Same |
| `"\u00a0Ada\u3000"` (non-ASCII whitespace) | `"Ada"` | `"Ada"` | Same |
| Successful response / transport error | passed back / raised | passed back / raised | Same |

**Compatibility conclusions**
- **New client, v1 provider:** Supported. String values never reach v1's `null` → 422 path.
- **New client, v2 provider:** Supported. String values never reach v2's `null` → remove-label path.
- **Mixed versions or rollback to the old client:** Supported. Stored labels are the same either way, and there's no data migration or flag.
- **Non-string input (e.g. `None`):** Not applicable. The README puts other types outside the contract. For the record, `None` now fails with `AttributeError` before any request is sent, where it used to send `null`. That change isn't covered by the contract, so it isn't a finding.

**Evidence and limits**
- **Tests:** I ran `python3 -B -m unittest discover -s tests -v` and all 3 passed, including the 4 new cases in `test_normalized_requests`.
- **Request shape only:** The tests check what the client sends, not what gets stored. The test transport doesn't implement a provider, so the "same stored label" conclusion rests on `protocol.md` plus the idempotence check, not on a real provider.
- **Python version:** I only ran on Python 3.15.0. The README promises 3.9+. As far as I know, the set of characters `str.strip()` removes has been the same since well before 3.9, but I didn't run 3.9–3.14 to confirm.
- **Not assessed:** As you asked, I deployed nothing and didn't check the deployed provider version or environment health.

---

## Findings

### P0 - Critical
None.
### P1 - High
None.
### P2 - Medium
None.
### P3 - Low
None.

I found nothing under any checklist category: security (no injection, secrets or unsafe input handling), SOLID (single-purpose function, transport injected), code quality (no swallowed exceptions; empty and whitespace-only strings tested), or removal. The knowledge base had no prior review findings or language idioms to compare against. No findings to index.

The change meets the documented contract, and I'm not recommending any changes.
