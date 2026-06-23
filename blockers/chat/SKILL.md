---
name: blockers
description: "List what is stuck and what or who each item waits on: what am I blocked on, what's waiting on someone, what's stuck, what's holding things up, what's on hold. Pick this over actionables when the item CANNOT proceed - it is waiting on a person, approval, or external dependency. Pick this over recap (which is a past narrative, not a current status scan)."
---

## When this fires
The user wants to know what cannot move forward right now: "what am I blocked
on", "what's waiting on someone", "what's stuck", "what's holding things up",
"what's waiting for approval", "what's on hold". Choose this over actionables
specifically when the item is stuck waiting on an external dependency, person, or
approval - not just unstarted.

## How to recall
Use the `recall` tool. Query: the user's stated topic plus blocked-shaped
keywords ("blocked, waiting on, stuck, on hold") - the wording is how you narrow
to stuck items. Do NOT restrict by time window. If a recalled memory signals the
blocker was resolved (a follow-up says "unblocked", "approved", "done"), do NOT
list it as active. If the result is thin, broaden the query and raise `budget` to "mid".

<!-- recall-recipe-chat embedded below -->

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

## Output contract
Return a list of active blockers only (skip anything with a resolution signal).
For each:

- **Blocked item** - what cannot proceed.
- **Waiting on** - the person, approval, or dependency holding it up.
- **Since** - when the block was logged (if available).

If no active blockers are found, say "No active blockers logged." and offer to
check actionables for items that may be stalled without an explicit blocker tag.

<!-- version: 5 -->
