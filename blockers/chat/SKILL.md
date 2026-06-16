---
name: blockers
description: "List what is stuck and what or who each item waits on: what am I blocked on, what's waiting on someone, what's stuck, what's holding things up, what's on hold. Pick this over actionables when the item CANNOT proceed - it is waiting on a person, approval, or external dependency. Pick this over recap (which is a past narrative, not a current status scan)."
---

# blockers

## When this fires
The user wants to know what cannot move forward right now: "what am I blocked
on", "what's waiting on someone", "what's stuck", "what's holding things up",
"what's waiting for approval", "what's on hold". Choose this over actionables
specifically when the item is stuck waiting on an external dependency, person, or
approval - not just unstarted.

## How to recall
Use the `recall` tool with `tags: ["memory_kind:blocker"]`. Query: the user's
stated topic or "blocked items waiting on external dependency". Do NOT restrict by
time window. If a recalled memory signals the blocker was resolved (a follow-up
says "unblocked", "approved", "done"), do NOT list it as active. If the
tag-filtered result is thin, fall back to untagged recall shaped around "blocked",
"waiting", "stuck", "on hold".

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
Return a list of active blockers only (skip anything with a resolution signal).
For each:

- **Blocked item** - what cannot proceed.
- **Waiting on** - the person, approval, or dependency holding it up.
- **Since** - when the block was logged (if available).

If no active blockers are found, say "No active blockers logged." and offer to
check actionables for items that may be stalled without an explicit blocker tag.

<!-- version: 1 -->
