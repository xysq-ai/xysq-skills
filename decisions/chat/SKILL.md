---
name: decisions
description: "Extract choices and calls made in a time window: what did we decide, what decisions were made last week, why did we pick X, what calls did I make, what was resolved. Pick this over recap when the focus is specifically on choices and rationale, not general progress. Pick this over blockers (which is about what is stuck, not what was decided)."
---

## When this fires
The user wants an enumerated list of choices made in a window: "what did we
decide", "what decisions were made last week", "why did we pick X", "what calls
did I make", "what did we settle on", "what was agreed". Choose this over recap
when the focus is specifically on choices and their rationale.

## How to recall
Use the `recall` tool with `tags: ["memory_kind:decision"]`. Query: the user's
stated topic or "decisions and choices" for the window. For a relative window,
over-fetch and post-filter by `occurred_at`. If the tag-filtered result is thin,
fall back to untagged recall with the same query and filter for decision-shaped
content.

<!-- recall-recipe-chat embedded below -->

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

## Output contract
Return an enumerated list, most-recent-first. For each item:

- **Decision** - what was decided, in one sentence.
- **Why** - the stated rationale (omit if not logged).
- **Who** - who made or approved the call (omit if solo or unknown).

If the window yields no decisions, say "No decisions logged for <window>." and
offer to widen the window or check a specific topic.

<!-- version: 2 -->
