---
name: prep
description: "Assemble context for an upcoming meeting or call: I have a meeting about X what do I know, prep me for my call with Acme, what's the context for the topic sync, brief me before the standup, what should I know going into the design review. Pick this over recap (past window narrative) because prep is topic-scoped and forward-facing - pulls context regardless of age."
---

# prep

## When this fires
The user is about to enter a meeting, call, or sync and wants a briefing: "I have
a meeting about X - what do I know", "prep me for my call with Acme", "what's the
context for the auth sync", "brief me before the standup", "what should I know
going into the design review". The anchor is a named topic, person, or event, not
a time window.

## How to recall
Use the `recall` tool. Query: the topic, project name, or person the meeting
concerns. Pull broadly (raise `top_k`) - do NOT restrict by time window; relevant
context may be months old. Favor recent results when ranking but do not exclude
older background. If the topic names a person, also recall with that person's name
to surface relationship context and open threads.

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
Return a briefing with up to four sections (omit any with no recalled content):

1. **Background** - what this topic or person is about, the core context.
2. **Recent activity** - what has happened lately relevant to the meeting.
3. **Open threads** - unresolved questions, pending decisions, outstanding asks.
4. **Anything needing a decision** - items the user may need to resolve, based on
   what is logged.

If the vault has nothing on the topic, say "I don't have anything logged on
<topic>. Want me to search a related term?"

<!-- version: 2 -->
