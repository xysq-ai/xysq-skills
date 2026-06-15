---
title: Triggering Eval - Recall Skill Library
date: 2026-06-15
method: description-routing judgment (judge model reasons as routing model would)
---

# Triggering Evaluation

## Skill Descriptions Under Test

| Skill | Description (verbatim) |
|-------|------------------------|
| recap | "Synthesize what happened in a time window - catch me up, what did I work on, what happened this week, what's been going on, weekly recap, daily summary, what did I do yesterday. Fire even when the word recap is not used: any request for a period summary or progress narrative triggers this. Prefer this over decisions (choices only) or actionables (future tasks)." |
| decisions | "Extract choices and calls made in a time window: what did we decide, what decisions were made last week, why did we pick X, what calls did I make, what was resolved. Pick this over recap when the focus is specifically on choices and rationale, not general progress. Pick this over blockers (which is about what is stuck, not what was decided)." |
| actionables | "Surface open tasks, pending items, and stated priorities: what's pending, what do I need to do, what's been sitting too long, my open items, my priorities, what should I work on, what's on my plate. Pick this over recap (which covers the past) and over blockers (items STUCK waiting on someone external). This is forward-looking work the user owns." |
| blockers | "List what is stuck and what or who each item waits on: what am I blocked on, what's waiting on someone, what's stuck, what's holding things up, what's on hold. Pick this over actionables when the item CANNOT proceed - it is waiting on a person, approval, or external dependency. Pick this over recap (which is a past narrative, not a current status scan)." |
| prep | "Assemble context for an upcoming meeting or call: I have a meeting about X what do I know, prep me for my call with Acme, what's the context for the topic sync, brief me before the standup, what should I know going into the design review. Pick this over recap (past window narrative) because prep is topic-scoped and forward-facing - pulls context regardless of age." |

---

## Confusion Matrix (should_trigger queries only, n=50)

Rows = intended skill. Columns = predicted routing.

| Intended \ Predicted | recap | decisions | actionables | blockers | prep | none/other |
|---|---|---|---|---|---|---|
| **recap** (n=10) | **10** | 0 | 0 | 0 | 0 | 0 |
| **decisions** (n=10) | 0 | **10** | 0 | 0 | 0 | 0 |
| **actionables** (n=10) | 0 | 0 | **10** | 0 | 0 | 0 |
| **blockers** (n=10) | 0 | 0 | 0 | **10** | 0 | 0 |
| **prep** (n=10) | 0 | 0 | 0 | 0 | **10** | 0 |

Diagonal sum: 50 / 50. No off-diagonal entries.

---

## Per-skill Should-Trigger Accuracy

| Skill | Correct | Total | Accuracy |
|-------|---------|-------|----------|
| recap | 10 | 10 | 100% |
| decisions | 10 | 10 | 100% |
| actionables | 10 | 10 | 100% |
| blockers | 10 | 10 | 100% |
| prep | 10 | 10 | 100% |
| **Overall** | **50** | **50** | **100%** |

---

## Should-Not-Trigger Routing (negatives)

All 50 negative queries (10 per skill) route cleanly to a different skill or none. No skill fires incorrectly for its own negatives. Predicted routing for negatives:

**recap negatives:**
- "what decisions have we made on auth" - decisions
- "list all open action items for billing" - actionables
- "what are we blocked on right now" - blockers
- "show me what is still stuck on the search rollout" - blockers
- "prep me for my 1:1 with Sam" - prep
- "what do I need to know before meeting Dana" - prep
- "log a new decision about the eventstore schema" - decisions (see note A)
- "what actions are still open from last month" - actionables
- "are there any unresolved blockers on billing" - blockers
- "what is Sam's role on the Q3 roadmap" - none/xysq (see note B)

**decisions negatives:** all route to recap (4), actionables (2), blockers (2), prep (2). Clean.

**actionables negatives:** all route to decisions (3), recap (3), blockers (2), prep (2). Clean.

**blockers negatives:** all route to decisions (2), recap (4), actionables (2), prep (2). Clean.

**prep negatives:** all route to decisions (3), recap (3), actionables (2), blockers (2). Clean.

---

## Near-Miss Flags (queries that warrant attention even if correctly routed)

### Flag 1: actionables queries with temporal phrasing (LOW RISK)

Queries: "what tasks are still open from last week", "any pending to-dos from the last month", "what actions are still open from the search rollout"

These carry "from last week / last month" phrasing that superficially resembles recap's time-window trigger. The deciding signal is "still open / pending" - forward-looking residuals, not a past narrative. The actionables description explicitly covers this ("what's been sitting too long") and recap description explicitly defers to actionables for future tasks.

Verdict: correctly routes to actionables. No fix needed. Risk is very low because "still open / pending" language dominates.

### Flag 2: decisions "log/capture/record" store operations (LOW RISK)

Queries: "log the decision to use Postgres FTS for eventstore", "capture a decision: switching to HMAC for tokens", "record that we reversed the Elasticsearch decision"

These are write/store operations, not recall queries. The decisions description says "Extract choices and calls made" - extraction language - which technically describes recall. However, the description also gives concrete example phrases like "what did we decide / what was resolved" that don't match "log / capture / record". A routing model could plausibly fire the decisions skill (since the subject is explicitly a decision and no other skill covers decision-logging), or route to the core xysq memory skill (retain).

In practice the model would likely fire decisions because the word "decision" appears prominently and no other skill competes for it. But the description does not clearly invite store operations. If the library evolves to include a store vs. retrieve distinction, this could misfire. For now the risk is contained because the decisions skill DOES handle logging in its body - only the description is silent on it.

Suggested minor edit: add "log a decision, capture a call" to the decisions description to make store operations explicit. See Recommendation 1 below.

### Flag 3: blockers vs. actionables on "waiting" language (LOW RISK)

Query: "what is still waiting on billing"

"Waiting on" sits at the boundary between "pending" (actionables) and "blocked waiting on external" (blockers). The blockers description uses the exact phrase "what's waiting on someone" which matches "waiting on billing". Actionables description explicitly carves this out: "over blockers (items STUCK waiting on someone external)". Routes correctly to blockers.

No fix needed. The mutual carve-outs are doing their job.

### Flag 4: "what is Sam's role on the Q3 roadmap" (none/xysq)

This negative in the recap file is a factual point-query, not a summary lens. None of the five skill descriptions cover it. It would correctly not fire recap (no time window, no narrative). It could weakly attract prep if the model pattern-matches "Q3 roadmap discussion" to an upcoming meeting context, but no meeting is stated. Correctly routes to none/xysq core. No fix needed.

---

## Verdict

**PASS.**

All 50 should_trigger queries route to the correct skill (100%). All 50 should_not_trigger queries route away from their host skill (100%). The confusion matrix is a perfect diagonal. No systematic off-diagonal cluster exists between any pair.

The five descriptions are well-separated. The cross-skill carve-outs ("pick this over X when...") in each description are effective and mutually consistent - every boundary pair (recap/decisions, recap/actionables, actionables/blockers, recap/prep) is addressed bidirectionally.

---

## Recommendations

### Recommendation 1 - decisions description (OPTIONAL, low urgency)

**Current:** "Extract choices and calls made in a time window: what did we decide, what decisions were made last week, why did we pick X, what calls did I make, what was resolved."

**Suggested:** "Extract or log choices and calls made in a time window: what did we decide, log a decision, capture a call, what decisions were made last week, why did we pick X, what was resolved."

**Rationale:** Three of the 10 should_trigger queries are store operations ("log", "capture", "record"). The description's current language only covers extraction/recall. Adding store examples makes the description accurate for write operations and prevents a future routing model from preferring the core xysq `memory_retain` skill for decision-logging queries.

### Recommendation 2 - No other changes needed

All other descriptions are correctly scoped and well-differentiated. The temporal anchor (recap/decisions), forward vs. past (actionables/recap), stuck vs. pending (blockers/actionables), and topic-scoped vs. time-scoped (prep/recap) distinctions are all cleanly expressed and non-overlapping.

---

## Method Notes

- Judge model: claude-sonnet-4-6 (the routing model itself)
- Routing decision: purely from skill descriptions (frontmatter `description:` field) as a routing model would see them
- No external API calls, no vault data
- 100 total queries evaluated (50 should_trigger + 50 should_not_trigger across 5 skills)
