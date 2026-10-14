# Fact-flip propagation

A shared producer guard. Any producer skill that maintains durable artifacts runs this guard whenever a previously recorded fact is contradicted.

## Motivating failure (F2 — non-propagated correction)

In the field, a recorded fact flipped: an enforcement table that earlier artifacts asserted existed turned out to have been deleted. The correction was applied to **one low-traffic page** — while **four auto-loaded context files kept asserting the stale fact**. Every downstream consumer that loaded one of those four files inherited the contradiction, and the "corrected" page was the least likely of the five to be read.

The lesson: a correction applied at the point of discovery is not propagated. Recorded facts are copied, cited, and cached across a workspace; flipping one occurrence leaves every other occurrence lying. A single correction is a **local** edit to a **non-local** fact.

## The rule — flip every occurrence in the same session

When a recorded fact is contradicted — a claim you or a prior run wrote is now shown false — the correction is not done until every assertion of the old fact is fixed:

1. **Name the old fact precisely.** State the stale claim in the terms it was recorded in (the entity, the table, the invariant, the status marker) so it can be searched for.
2. **Search the whole workspace.** Grep the durable docs, the kit pages, auto-loaded context files, and any indexed knowledge for **every** assertion of the old fact — not just the page you found it on. Search for the fact's synonyms and aliases, not only its exact wording.
3. **Fix every occurrence in the same session.** Update each assertion to the corrected fact, or delete it where it no longer applies. Do not defer any occurrence to "later" — later is where F2 lives.
4. **Record the flip where it will be seen.** Note what changed and why, so a consumer who cached the old fact upstream can reconcile.

A correction that touches one occurrence and leaves the rest is not a partial fix; it is a new contradiction.

## Self-check

- Did I search the **whole workspace** — durable docs, context files, indexed knowledge — or only the page where I noticed the contradiction?
- Did I search for the fact's aliases and synonyms, not just its verbatim wording?
- Is every occurrence fixed **this session**, with none deferred?
