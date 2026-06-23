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
Use the `recall` tool. Query: the user's stated topic plus decision-shaped
keywords ("decision, decided, chose, rationale, why") - the wording is how you
narrow to choices. For a relative window, pass `occurred_after`/`occurred_before`
(ISO dates) so the tool filters server-side. If the result is thin, broaden the
query and raise `budget` to "mid".

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
Return an enumerated list, most-recent-first. For each item:

- **Decision** - what was decided, in one sentence.
- **Why** - the stated rationale (omit if not logged).
- **Who** - who made or approved the call (omit if solo or unknown).

If the window yields no decisions, say "No decisions logged for <window>." and
offer to widen the window or check a specific topic.

<!-- version: 5 -->
