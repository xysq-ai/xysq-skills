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
activity" for the window. For "why" context, also recall with
`tags: ["memory_kind:decision"]`; for "what happened" detail, also recall with
`tags: ["memory_kind:event"]`. For a relative window, over-fetch (`top_k`) and
post-filter by `occurred_at`.

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
Return up to four segments - tight and readable:

1. **What happened** - key events and milestones in the window.
2. **Why** - decisions or rationale behind the work (omit if nothing recalled).
3. **Who was involved** - collaborators or stakeholders (omit if solo or unknown).
4. **Suggested next step** - one concrete forward action based on what was logged.

If the window yields nothing, say: "Nothing logged for <window>. Want me to widen
the window or search by topic instead?"

<!-- version: 2 -->
