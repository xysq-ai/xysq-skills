<!-- SHARED RECALL RECIPE (CHAT) - embed into each chat recall skill -->

## Grounding discipline
Answer ONLY from what `recall` returns. Write grounded, clean prose - a natural
summary, not a citation dump. Do NOT inline citations. When the vault has little
on the topic, say so plainly ("I don't have much on X") rather than inventing
detail.

## Time-window handling
`recall` has NO server-side date filter. To honor "since yesterday / last week /
this month": put the relative phrase in the query text, over-fetch (raise
`top_k`), then post-filter results by their `occurred_at`, keeping only those
inside the target window. Translate the user's phrase into both the query wording
and the post-filter bounds.

## Tag-filtered recall
When a `memory_kind:*` tag keys this skill, pass it in the recall `tags` to get
the pre-classified slice; fall back to untagged semantic recall if it yields too
little.

## Deduplicate before rendering
`recall` may return the same underlying fact as several near-identical chunks.
Collapse these to one item before rendering - never show the same fact twice.

## Clarify, don't re-query
If recall is empty or low-confidence for an ambiguous prompt, ASK the user a
clarifying question. Do not silently re-run recall with reworded queries hoping
something hits.

## Tone vs. structure
Keep the chat's default tone (tight prose, no headers-heavy dumps), but follow
this skill's output structure below.
