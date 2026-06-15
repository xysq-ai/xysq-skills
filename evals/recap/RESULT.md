# Eval Results: recap skill

Fixture `now`: 2026-06-15T12:00:00Z. 7-day window starts 2026-06-08T12:00:00Z.

---

## Eval 1 - "catch me up on the auth work this week"

### Scripted assertions

| Script | Result | Exit code |
|---|---|---|
| assert_time_window.py (7d) | PASS | 0 |
| assert_structure.py (recap) | PASS | 0 |

### Grader verdict

Memories available (in-window, after post-filter): idx 0 (Jun 15 - hotfix deploy), idx 1 (Jun 14 - token-refresh endpoint), idx 2 (Jun 14 - Priya+Jordan session-store), idx 4 (Jun 8 - load test 500 RPS), idx 6 (Jun 14 - HMAC-SHA256 decision), idx 17 (Jun 12 - action: write unit tests).

Claim-by-claim:
- "auth service hotfix was deployed to production this morning (Jun 15)" - PASS: idx 0 confirms
- "auth team completed the token-refresh endpoint and added retry logic on 503 responses" - PASS: idx 1
- "Priya and Jordan paired on the auth session-store migration" - PASS: idx 2
- "resolved the Redis key-expiry edge case...agreed on the TTL strategy" - PASS: idx 2
- "task was logged to write unit tests for the token refresh endpoint" - PASS: idx 17
- "auth service load test passed at 500 RPS with p99 under 80ms" - PASS: idx 4
- "HMAC-SHA256 for auth token signing instead of RSA...to reduce latency" - PASS: idx 6
- Next step "Write unit tests for the auth token refresh endpoint" - PASS: grounded in idx 17

No out-of-window content (idx 5 Jun 7 pytest refactor and idx 15 May 15 OAuth2 blocker not mentioned).

```json
{"grounding": "PASS", "usefulness": "PASS", "evidence": "All 8 substantive claims trace directly to recalled memories. Time filter correctly excludes idx 5 (Jun 7) and idx 15 (May 15). Multi-person requirement (Priya + Jordan) covered. Concrete next step grounded in idx 17."}
```

### Comparator verdict

With-skill output: 4-segment structure, time-bounded to 7d, Priya+Jordan named, concrete next step (write unit tests), HMAC-SHA256 rationale in Why section. No fabrication.

Baseline output: covers all the same events but adds idx 5 (pytest refactor, Jun 7 - outside window) and idx 15 (OAuth2 scope review blocker, May 15 - well outside window). Missing the 4-segment structure. Next step is vague ("completing unit tests and following up on scope reviews"). The scope review mention is an out-of-window contamination from the baseline's lack of time discipline.

```json
{
  "winner": "A",
  "reason": "With-skill output (A) correctly excludes out-of-window items (pytest refactor Jun 7, OAuth2 blocker May 15) while baseline (B) surfaces both. A also uses the required 4-segment structure and ends with a specific, grounded next step. B's next step is vague and one of its mentions (OAuth2 scope review blocker) is from outside the 7-day window.",
  "grounding_a": "PASS",
  "grounding_b": "FAIL",
  "ungrounded_claims_a": [],
  "ungrounded_claims_b": ["OAuth2 scope review waiting on security team availability - this is from idx 15, May 15, outside the 7-day window for a 'this week' query"]
}
```

---

## Eval 2 - "what happened on the eventstore project this week"

### Scripted assertions

| Script | Result | Exit code |
|---|---|---|
| assert_time_window.py (7d) | PASS | 0 |
| assert_structure.py (recap) | PASS | 0 |

### Grader verdict

Memories available (in-window, after post-filter): idx 3 (Jun 12 - batch-write merged to staging), idx 7 (Jun 12 - Elasticsearch decision), idx 8 (Jun 8 - reversed to Postgres FTS).
Out-of-window trap: idx 14 (May 16 - schema migration blocked on DBA sign-off).

Claim-by-claim:
- "eventstore batch-write endpoint was merged and deployed to staging on Jun 12" - PASS: idx 3
- "Elasticsearch was initially chosen for full-text query support" - PASS: idx 7
- "then reversed in favour of Postgres FTS (Jun 8)" - PASS: idx 8
- "Elasticsearch's operational overhead is too high for the current team size" - PASS: idx 8
- Next step "Confirm the Postgres FTS implementation is underway...verify batch-write endpoint is stable in staging before promoting" - PASS: grounded in idx 8 (reversal needs follow-through) and idx 3 (staging)

The schema migration blocker (idx 14, May 16) was correctly excluded.

```json
{"grounding": "PASS", "usefulness": "PASS", "evidence": "All substantive claims trace to recalled memories idx 3, 7, 8. The out-of-window trap (idx 14, DBA sign-off blocker from May 16) is correctly excluded. The 4-segment structure is used (no 'Who' section - correctly omitted when solo/unknown). Concrete next step grounded in the Elasticsearch reversal and staging deploy."}
```

### Comparator verdict

With-skill output: time-bounded, no DBA blocker mention, clean 4-segment structure, next step grounded in the reversal.

Baseline output: includes the schema migration DBA blocker (idx 14, May 16 - outside 7d window). This is out-of-window contamination. The note "older blocker - schema migration has been waiting on DBA sign-off...since mid-May" explicitly identifies this as older, but still includes it without the skill's discipline. No 4-segment structure. Next step not explicitly called out.

```json
{
  "winner": "A",
  "reason": "With-skill output (A) correctly excludes the May 16 DBA blocker that is outside the 7-day window. Baseline (B) includes it despite the user asking specifically 'this week'. A uses required 4-segment structure; B is unstructured prose. A's next step is explicit and grounded; B has no dedicated next step.",
  "grounding_a": "PASS",
  "grounding_b": "FAIL",
  "ungrounded_claims_a": [],
  "ungrounded_claims_b": ["schema migration has been waiting on DBA sign-off for a new partitioning strategy since mid-May - this is idx 14 (May 16), outside the 7-day window for a 'this week' query"]
}
```

---

## Eval 3 - "what happened on the warehouse-v2 project this week"

### Scripted assertions

| Script | Result | Exit code |
|---|---|---|
| assert_thin_signal.py | PASS | 0 |

### Grader verdict

Recall returns warehouse memories (idx 16, 20, 24, 25) but all have `mentioned_at` of 2026-05-01 - 45 days outside the 7-day window. "warehouse-v2" as a specific project label has no memories at all. With-skill output correctly acknowledges no in-window memories and offers to widen the window.

```json
{"grounding": "PASS", "usefulness": "PASS", "evidence": "Output correctly identifies no in-window content for warehouse-v2. No fabrication. The offer to widen the window matches the skill's prescribed fallback when the window yields nothing."}
```

### Comparator verdict

With-skill output: honest, brief, offers alternatives.

Baseline output: surfaces warehouse facts (Parquet decision, pipeline design, blocker from May 1) and presents them as context, noting they are from early May. While it acknowledges "no recent movement this week", it still narrates the old memories as active context - which misrepresents them for a "this week" query. A user reading baseline might think these facts are informative background; a user asking "this week" just wants to know nothing happened.

```json
{
  "winner": "A",
  "reason": "With-skill output (A) correctly says it has nothing logged for warehouse-v2 this week and offers to widen scope. Baseline (B) surfaces 45-day-old warehouse memories in detail, misleadingly presenting them as relevant to a 'this week' query. A is grounded on the empty result; B is technically grounded in older facts but misapplied to the wrong time scope.",
  "grounding_a": "PASS",
  "grounding_b": "PASS",
  "ungrounded_claims_a": [],
  "ungrounded_claims_b": []
}
```

Note: baseline grounding is technically PASS (all claims trace to memories), but the comparator still prefers with-skill because time-scope discipline is higher-priority than pure grounding when the query specifies "this week".

---

## Time-window trap analysis

The fixture contains deliberate out-of-window traps:
- idx 5 (Jun 7, auth pytest refactor) - 8 days before now, outside 7d window
- idx 15 (May 15, auth OAuth2 blocker) - 31 days before now
- idx 14 (May 16, eventstore DBA blocker) - 30 days before now

With-skill outputs excluded all three. Baseline outputs included idx 5+15 (eval 1) and idx 14 (eval 2).

## Empty-topic analysis (eval 3)

The "warehouse-v2" topic has zero in-window memories. With-skill output correctly said "I don't have anything logged" rather than fabricating or surfacing old warehouse memories. Baseline narrated old warehouse facts in detail.

---

## Overall gate: recap PASS

| Eval | Scripted | Grounding | Usefulness | Comparator winner |
|---|---|---|---|---|
| 1 (auth this week) | PASS | PASS | PASS | with_skill |
| 2 (eventstore this week) | PASS | PASS | PASS | with_skill |
| 3 (warehouse-v2 empty) | PASS | PASS | PASS | with_skill |

**recap PASSES the acceptance gate.** All scripted assertions pass (3/3), grounding holds on all three outputs, and the comparator prefers with-skill over baseline on every eval. The single most important observation: the time-window post-filter is the skill's core differentiator - every baseline failure was caused by surfacing out-of-window content that the skill correctly excluded.

---

## assert_time_window script limitation

The script detects leaks via exact 6-word prefix matching against fixture content. Both baseline files paraphrase out-of-window memories rather than quoting them verbatim, so the script returns PASS for baselines too. The comparator analysis above identifies the baseline time-scope failures based on semantic content. This means `assert_time_window.py` is only a reliable gate against verbatim copy-through, not against paraphrased out-of-window content. A fuzzy or embedding-based check would be more robust.

---

## Skill weakness notes (for future improvement)

1. The skill recipe says to use `memory_reflect` for the synthesized narrative. The eval used `memory_recall` + manual synthesis, which works but deviates from the recipe. The reflect path should be tested separately to verify the 4-segment output contract holds when reflect is used.

2. The recipe does not specify what to do when `occurred_start` is null on reflect results (which it is in this fixture). The post-filter falls back to `mentioned_at`. The skill description says "citation `occurred_start` (reflect)" but doesn't document this fallback. This could cause silent failures in production if the field population is inconsistent.

3. The "Who was involved" segment instruction says "omit if solo or unknown" - this is correct but the skill should clarify whether "unknown" means no names appear in any recalled memory, or that the user is the only actor. The eval had a clear case (eval 2) where no collaborators appeared and the section was correctly omitted.
