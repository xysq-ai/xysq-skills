---
name: actionables
description: "Surface open tasks, pending items, and stated priorities: what's pending, what do I need to do, what's been sitting too long, my open items, my priorities, what should I work on, what's on my plate. Pick this over recap (which covers the past) and over blockers (items STUCK waiting on someone external). This is forward-looking work the user owns."
---

## When this fires
The user wants a forward-looking list of open tasks and priorities: "what's
pending", "what do I need to do", "what's been sitting too long", "my open
items", "my priorities", "what should I work on next", "what's on my plate".
Choose this over recap (past narrative) and over blockers (items that cannot
proceed - waiting on someone or something external).

## How to recall
Use the `recall` tool. Query: the user's stated topic plus task-shaped keywords
("todo, action item, pending, priority, next step") - the wording is how you
narrow to open work. Do NOT restrict by time window - actionables can be old;
pull broadly (raise `top_k`, and raise `budget` to "mid" for deeper coverage)
and surface long-pending items prominently.

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
Return a prioritized list of open items. Group as:

1. **Long-pending** - items logged more than a week ago with no resolution signal.
2. **Active** - items logged recently and still open.
3. **Stated priorities** - anything the user explicitly flagged as high priority.

For each item: one-line description, date first logged, and any noted deadline or
priority signal. If nothing is found, say "No open actionables logged." and offer
to search by topic.

<!-- version: 3 -->
