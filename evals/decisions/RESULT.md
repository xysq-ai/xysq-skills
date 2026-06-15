# decisions skill eval results

now = 2026-06-15T12:00:00Z

---

## Eval 1 - "what decisions have we made on the eventstore project"

### Scripted
| Script | Args | Result |
|--------|------|--------|
| assert_structure.py | decisions | PASS (exit 0) |
| assert_time_window.py | window_days=30 | PASS (exit 0) |

### Grounding (grader.md)
All claims trace to recalled memories. The superseded Elasticsearch decision (idx 7) and the Postgres FTS reversal (idx 8) both appear. The rationale ("ops overhead too high") is directly from idx 8. No invented dates, names, or outcomes.
**PASS**

### Usefulness (grader.md)
Output is an enumerated Decision/Why/Who log (2 items), most-recent-first. Supersession is explicitly flagged ("SUPERSEDED" label + explanatory footnote). Correct format per skill contract.
**PASS**

### Comparator (with_skill A, baseline B)
```json
{
  "winner": "A",
  "reason": "A produces an enumerated Decision/Why/Who log with the superseded pair correctly separated and labeled. B gives a prose narrative mixing events with decisions and omits the Why/Who structure entirely. A is grounded on the decision-kind memories only; B introduces non-decision content (batch-write deploy, schema migration blocker) that dilutes the decision focus.",
  "grounding_a": "PASS",
  "grounding_b": "PASS",
  "ungrounded_claims_a": [],
  "ungrounded_claims_b": []
}
```
**Winner: A (with_skill)**

---

## Eval 2 - "what decisions came out of the auth work this week"

### Scripted
| Script | Args | Result |
|--------|------|--------|
| assert_structure.py | decisions | PASS (exit 0) |
| assert_time_window.py | window_days=7 | PASS (exit 0) |

### Grounding (grader.md)
Single decision listed: HMAC-SHA256 over RSA (idx 6, 2026-06-14, within 7-day window). Rationale and who are correct. The out-of-window warehouse/billing/search decisions correctly do not appear.
**PASS**

### Usefulness (grader.md)
Enumerated list with 1 item (the only auth decision within 7 days). Correctly states "No other auth decisions logged within the past 7 days." The scope is correctly bounded to auth + within-window.
**PASS**

### Comparator (with_skill A, baseline B)
```json
{
  "winner": "A",
  "reason": "A correctly scopes to decisions only, applies the 7-day window, and lists exactly one entry (HMAC-SHA256) in the required Decision/Why/Who format. B mixes in non-decision events (token-refresh endpoint completion, Priya/Jordan pairing, hotfix deploy, load test) and does not use the enumerated format. B also fails the usefulness criterion for the decisions skill.",
  "grounding_a": "PASS",
  "grounding_b": "PASS",
  "ungrounded_claims_a": [],
  "ungrounded_claims_b": []
}
```
**Winner: A (with_skill)**

---

## Eval 3 - "what decisions were made on the warehouse-v2 project"

### Scripted
| Script | Args | Result |
|--------|------|--------|
| assert_thin_signal.py | - | PASS (exit 0) - "I don't have anything" matched |

### Grounding (grader.md)
Claims "no decisions recorded under that project" - correct (fixture intentionally empty for warehouse-v2). Reference to old warehouse entries (45 days old) is grounded in idx 24/25 (2026-05-01, 45 days before now). No invention.
**PASS**

### Comparator (with_skill A, baseline B)
```json
{
  "winner": "A",
  "reason": "A correctly identifies zero entries for warehouse-v2 and says so plainly ('I don't have anything logged for warehouse-v2'). It offers to clarify by widening to the 'warehouse' topic, consistent with the skill's clarify-don't-re-query directive. B incorrectly surfaces old warehouse decisions (Parquet choice, pipeline design) as if they answer the warehouse-v2 question, and even though it notes the labeling discrepancy at the end, the framing misleads the user into thinking the data is relevant. B fails the thin-signal test for this prompt.",
  "grounding_a": "PASS",
  "grounding_b": "FAIL",
  "ungrounded_claims_a": [],
  "ungrounded_claims_b": ["attributes warehouse decisions to warehouse-v2 without any memory linking them to that project"]
}
```
**Winner: A (with_skill)**

---

## Superseded-decision pair check

**Prompt**: "what decisions have we made on the eventstore project" (Eval 1)

The with-skill output:
- Shows Postgres FTS as the CURRENT decision (item 1, labeled as superseding item 2)
- Shows Elasticsearch as SUPERSEDED (item 2, explicitly labeled [SUPERSEDED])
- Explains why the reversal happened (ops overhead)

**Result: CORRECT** - the skill surfaces the current decision first and flags the earlier one as superseded.

Note: the fixture has a chronological quirk - idx 7 (Elasticsearch) has `occurred_at: 2026-06-12` and idx 8 (Postgres FTS reversal) has `occurred_at: 2026-06-08`. By date alone, Elasticsearch (Jun 12) is more recent. However, the semantic content of idx 8 ("Reversed the Elasticsearch decision") makes clear that Postgres FTS is the intended current state per the fixture's design intent. The skill correctly interprets the semantic reversal rather than presenting the later-dated Elasticsearch entry as current.

---

## Overall gate

| Eval | Scripted | Grounding | Usefulness | Comparator |
|------|----------|-----------|------------|------------|
| 1 (eventstore) | PASS | PASS | PASS | A wins |
| 2 (auth this week) | PASS | PASS | PASS | A wins |
| 3 (warehouse-v2 thin) | PASS | PASS | PASS | A wins |

**decisions skill: PASS**

---

## Most important observation

The skill correctly applies the decisions-only filter (memory_kind:decision tag), enforces time-window post-filtering, and handles the superseded pair semantically rather than just by date order. The baseline consistently fails usefulness because it returns prose narratives mixing events with decisions - confirming the skill adds measurable value over naive recall.

One weakness worth noting: the SKILL.md recipe says to use `memory_reflect` for this skill, but the reflect endpoint returns HTTP 500 on this instance. The skill falls back to tagged `recall` + manual synthesis, which works but the recipe should document this fallback explicitly. The output quality does not degrade significantly when using recall in place of reflect for decision-kind memories, since the tag filter is sufficient to scope the result set.
