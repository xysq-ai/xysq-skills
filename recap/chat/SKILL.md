---
name: recap
description: "Synthesize what happened in a time window - catch me up, what did I work on, what happened this week, what's been going on, weekly recap, daily summary, what did I do yesterday. Fire even when the word recap is not used: any request for a period summary or progress narrative triggers this. Prefer this over decisions (choices only) or actionables (future tasks)."
---

## When this fires
The user wants a narrative summary of activity over a time window: "catch me up",
"what did I work on this week", "what happened in the auth project", "give me a
weekly recap", "what did I do yesterday". Fire even when the word "recap" is not
used - the signal is a time-bounded progress narrative.

## How to recall
Use the `recall` tool. Default query: the user's stated topic or "recent
activity" for the window. For "why" context, recall again with
decision/rationale keywords ("decision, decided, chose, why"); for "what
happened" detail, recall with event/milestone keywords. For a relative window,
pass `occurred_after`/`occurred_before` (ISO dates) so the tool filters
server-side; raise `budget` to "mid" for deeper coverage when the question needs it.

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
Return up to four segments - tight and readable:

1. **What happened** - key events and milestones in the window.
2. **Why** - decisions or rationale behind the work (omit if nothing recalled).
3. **Who was involved** - collaborators or stakeholders (omit if solo or unknown).
4. **Suggested next step** - one concrete forward action based on what was logged.

If the window yields nothing, say: "Nothing logged for <window>. Want me to widen
the window or search by topic instead?"

<!-- version: 3 -->
