---
name: prep
description: "Assemble context for an upcoming meeting or call: prep me for my call with Acme, brief me before the standup, what do I know about X. Topic-scoped and forward-facing, pulls context regardless of age."
---

## When this fires
The user is about to enter a meeting, call, or sync and wants a briefing: "I have
a meeting about X - what do I know", "prep me for my call with Acme", "what's the
context for the auth sync", "brief me before the standup", "what should I know
going into the design review". The anchor is a named topic, person, or event, not
a time window.

## How to recall
Use the `recall` tool. Query: the topic, project name, or person the meeting
concerns. Pull broadly (raise `top_k`, and raise `budget` to "mid" for deeper
coverage) - do NOT restrict by time window; relevant context may be months old.
Favor recent results when ranking but do not exclude older background. If the
topic names a person, also recall with that person's name to surface relationship
context and open threads.

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
Return a briefing with up to four sections (omit any with no recalled content):

1. **Background** - what this topic or person is about, the core context.
2. **Recent activity** - what has happened lately relevant to the meeting.
3. **Open threads** - unresolved questions, pending decisions, outstanding asks.
4. **Anything needing a decision** - items the user may need to resolve, based on
   what is logged.

If the vault has nothing on the topic, say "I don't have anything logged on
<topic>. Want me to search a related term?"

<!-- version: 5 -->
