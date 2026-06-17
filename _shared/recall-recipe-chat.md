<!-- SHARED RECALL RECIPE (CHAT) - embed into each chat recall skill -->

## Grounding discipline
Answer ONLY from what `recall` returns. Write grounded, clean prose - a natural
summary, not a citation dump. Do NOT inline citations. When the vault has little
on the topic, say so plainly ("I don't have much on X") rather than inventing
detail.

## Time-window handling
For "since yesterday / last week / this month", pass `occurred_after` (and
optionally `occurred_before`) as ISO dates (YYYY-MM-DD) on the `recall` call -
the tool filters server-side to that window. Translate the user's relative phrase
into concrete ISO bounds relative to today. Also keep the relative phrase in the
query text so ranking stays aligned.

## Shaping the query
The `recall` tool has no tag filter - express the kind of memory you want in the
query wording itself. For decisions, include words like "decision, decided,
chose, rationale, why"; for blockers, "blocked, waiting on, stuck, on hold"; for
open tasks, "todo, action item, pending, next step". Recall is semantic, so
strong topical wording is how you narrow results.

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
