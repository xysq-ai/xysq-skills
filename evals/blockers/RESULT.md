# blockers skill eval - RESULT

**Overall gate: PASS**

now=2026-06-15T12:00:00Z | fixture: fixture_vault.json (62 facts, indices 0-25)

---

## Resolved-pair headline check

**The key discrimination this skill must make:**

- idx 11 (memory_kind:blocker, 2026-06-12): "Blocked on the vendor contract for search rollout - legal review has not started yet."
- idx 12 (memory_kind:event, 2026-06-05): "Legal cleared the vendor contract. Search rollout blocker is resolved."

Note: the resolution (idx 12) was logged EARLIER in calendar time than the blocker (idx 11). This tests whether the skill uses content-based resolution detection rather than naive chronological order.

| Output | Resolved blocker dropped? |
|--------|--------------------------|
| with-skill (all evals) | YES - explicitly states resolution signal detected, blocker excluded |
| baseline eval 1 | NO - lists search rollout as "currently blocked", recommends following up with legal |
| baseline eval 2 | NO - lists search blocker as active alongside other unresolved blockers |

---

## Eval 1: "what is blocking the search rollout"

### Scripted assertions
| Script | with-skill | baseline |
|--------|-----------|---------|
| assert_time_window (30d) | PASS | PASS |
| assert_structure (blockers) | PASS | PASS |

### Grader (grounding + usefulness)
**with-skill:**
- GROUNDING: PASS - every claim (resolution signal, idx 11 origin, idx 12 clearance) traces to recalled memories
- USEFULNESS: PASS - correctly outputs "No active blockers" for search, explains the resolution, offers to check other projects

**baseline:**
- GROUNDING: FAIL - states "legal review has not started yet" (idx 11 text) while ignoring idx 12 which says it was cleared; recommends following up with legal team despite memory showing it was already resolved
- USEFULNESS: FAIL - misleads the user by listing a resolved blocker as active

### Comparator (blind A vs B)
```json
{
  "winner": "A",
  "reason": "A (with-skill) correctly processes the resolution signal from idx 12 and outputs 'No active blockers' for search. B (baseline) lists the search rollout as currently blocked and recommends following up with legal, directly contradicting the recalled memory that states the blocker is resolved. A single ungrounded claim in B is disqualifying.",
  "grounding_a": "PASS",
  "grounding_b": "FAIL",
  "ungrounded_claims_a": [],
  "ungrounded_claims_b": ["legal review has not started yet (ignores resolution signal)", "follow up with the legal team to check the status (legal already cleared it)"]
}
```

---

## Eval 2: "show me all current blockers across projects"

### Scripted assertions
| Script | with-skill | baseline |
|--------|-----------|---------|
| assert_time_window (30d) | PASS | FAIL - idx 15 (auth OAuth2, 2026-05-15, 31d) and idx 16 (warehouse, 2026-05-01, 45d) leaked |
| assert_structure (blockers) | PASS | PASS |

### Grader (grounding + usefulness)
**with-skill:**
- GROUNDING: PASS - billing (idx 13, 20d), eventstore (idx 14, 30d boundary inside), both within window; search resolved and dropped; out-of-window items excluded
- USEFULNESS: PASS - lists what is blocked and what each item waits on; resolved blocker explicitly excluded with reason

**baseline:**
- GROUNDING: FAIL - lists idx 11 (search) as active despite idx 12 resolution; also lists idx 15 and idx 16 which are outside the 30d window
- USEFULNESS: FAIL - 5-item list contains 1 resolved and 2 out-of-window items; user cannot trust the list

### Comparator (blind A vs B)
```json
{
  "winner": "A",
  "reason": "A correctly applies resolution detection (search blocker dropped), respects the 30d window (idx 15 and idx 16 excluded), and lists only billing and eventstore as active. B includes a resolved blocker (search) and two out-of-window items (auth, warehouse), failing both grounding and the time-window scripted assertion.",
  "grounding_a": "PASS",
  "grounding_b": "FAIL",
  "ungrounded_claims_a": [],
  "ungrounded_claims_b": ["search rollout currently blocked on vendor contract (resolved in idx 12)", "auth OAuth2 scope review blocked (31d, outside 30d window)", "warehouse data pipeline blocked (45d, outside 30d window)"]
}
```

---

## Eval 3: "is anything blocking the warehouse-v2 work"

### Scripted assertions
| Script | with-skill | baseline |
|--------|-----------|---------|
| assert_thin_signal | PASS - contains "I don't have much" | FAIL - no thin-signal phrase |

### Grader (grounding + usefulness)
**with-skill:**
- GROUNDING: PASS - notes older warehouse blocker (idx 16) may exist, correctly does not claim it is warehouse-v2; no invented claims
- USEFULNESS: PASS - acknowledges thin signal, outputs "No active blockers logged for warehouse-v2", offers to check actionables

**baseline:**
- GROUNDING: marginal PASS - references real memories (idx 16, idx 20) but hedges with "may be related" which is unverifiable speculation; does not fail hard on any specific unsupported claim
- USEFULNESS: FAIL - no thin-signal acknowledgement, speculates about connection to warehouse-v2 that is not in any memory

### Comparator (blind A vs B)
```json
{
  "winner": "A",
  "reason": "A correctly identifies thin signal and says so explicitly ('I don't have much on warehouse-v2'), meeting the assert_thin_signal requirement. A also offers a concrete next step (check actionables). B fails the thin-signal check, speculates about warehouse-v2 being related to a warehouse pipeline blocker without any memory evidence, and does not offer actionable guidance.",
  "grounding_a": "PASS",
  "grounding_b": "PASS",
  "ungrounded_claims_a": [],
  "ungrounded_claims_b": ["may be related to warehouse-v2 (no memory connects the general warehouse blocker to warehouse-v2)"]
}
```

---

## Summary table

| Eval | Scripted (with-skill) | Scripted (baseline) | Grounding (with) | Grounding (base) | Usefulness (with) | Usefulness (base) | Comparator |
|------|----------------------|---------------------|------------------|-----------------|-------------------|-------------------|------------|
| 1 | PASS | PASS | PASS | FAIL | PASS | FAIL | A (with-skill) |
| 2 | PASS | FAIL | PASS | FAIL | PASS | FAIL | A (with-skill) |
| 3 | PASS | FAIL | PASS | PASS | PASS | FAIL | A (with-skill) |

---

## Overall gate

**PASS**

The `blockers` skill:
1. Correctly DROPS the resolved blocker (idx 11 / search vendor contract) in all evals.
2. Correctly identifies the resolution signal from idx 12 despite the unusual chronology (resolution logged 7 days earlier than the blocker entry).
3. Respects the 30d time window in eval 2, excluding idx 15 (31d) and idx 16 (45d).
4. Acknowledges thin signal for warehouse-v2 (eval 3) and offers a next step.
5. Wins the blind comparator in all 3 evals.

The baseline fails on the headline discrimination in both eval 1 and eval 2 (resolved blocker listed as active), fails time window in eval 2, and fails thin-signal in eval 3.

### Key observation

The resolved-pair (idx 11 + idx 12) uses an unusual ordering: the resolution event (idx 12, 2026-06-05) was logged EARLIER in calendar time than the blocker (idx 11, 2026-06-12). This is a stress test for date-naive resolution logic. The with-skill output correctly uses the content signal ("Search rollout blocker is resolved") rather than timestamp ordering to determine resolution status. The baseline failed this test in both evals where search was a relevant topic.

### Recipe weakness noted

The skill recipe says "If a recalled memory signals the blocker was resolved (e.g., a follow-up note says 'unblocked', 'approved', 'done'), do NOT list it as active." This is correct in principle, but the resolution detection is entirely left to the LLM's reading of the retrieved texts - there is no structured resolution field in the memory schema. If a resolution note uses language that does not obviously signal resolution (e.g., "contract signed" without mentioning the blocker), detection could fail. The recipe would benefit from a note to look for topic-matching events as well as explicit resolution language.
