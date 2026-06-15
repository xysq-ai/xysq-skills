# Eval results: actionables skill

Fixture now: 2026-06-15T12:00:00Z. Bank: fixture-eval-bank (62 facts).

---

## Eval 1 - "what are my open action items for billing"

**Scripted:**
- `assert_time_window.py window=30`: PASS (no out-of-window leaks in with-skill output)
- `assert_structure.py actionables`: PASS (bullet list present)

**Grader (with-skill):** GROUNDING PASS / USEFULNESS PASS
All four claims traceable to recalled memories. Two billing actions (idx 18, idx 19) correctly surfaced within window. Out-of-window warehouse item (idx 20, 45d) explicitly flagged as out-of-scope rather than silently included.

**Comparator:** Winner = WITH-SKILL (A)
Baseline (B) leaked the out-of-window 45-day warehouse item into a billing-scoped response without labeling it out-of-scope. Both grounded; A wins on scope discipline.

---

## Eval 2 - "show me all open actions including old ones"

**Scripted:**
- `assert_structure.py actionables`: PASS (bullet list present)

**Grader (with-skill):** GROUNDING PASS / USEFULNESS PASS
All 4 action items from the fixture surfaced (idx 17, 18, 19, 20). Warehouse pipeline migration (idx 20, 45d) placed first under "Long-pending" header with "Oldest open item" label. Active group (idx 17) correctly separated.

**Comparator:** Winner = WITH-SKILL (A)
Baseline (B) listed the 45-day item last with a weak aside. With-skill surfaced it first, prominently, with explicit long-pending label. Both grounded; A wins on prioritization.

---

## Eval 3 - "do I have any open actions on the warehouse-v2 project"

**Scripted:**
- `assert_thin_signal.py`: PASS (phrase "I don't have anything logged" detected)

**Grader (with-skill):** GROUNDING PASS / USEFULNESS PASS
Correctly reported no warehouse-v2 content. Distinguished "warehouse" from "warehouse-v2". Offered to search broader. Matches skill contract ("No open actionables logged").

**Comparator:** Winner = WITH-SKILL (A)
Baseline (B): GROUNDING FAIL. Surfaced a memory_kind:event and a memory_kind:decision from the "warehouse" topic (not warehouse-v2) as if they were open action items for warehouse-v2. This is misleading - events and decisions are not actionables. With-skill correctly delivered thin-signal.

---

## KEY CHECK: long-pending item (idx 20, warehouse pipeline, 45 days old)

- **With-skill (eval 2):** SURFACED prominently. Listed first under "Long-pending", labeled "~45 days ago" and "Oldest open item". Correctly excluded from eval 1 (billing, 30d window).
- **Baseline (eval 2):** Listed last, mentioned briefly as "has been open for quite a while". Not flagged as long-pending or given priority position.

The skill recipe (oldest unresolved first, explicit long-pending group) worked as designed for this fixture.

---

## Actionables vs Blockers distinction

With-skill output in eval 2 explicitly says: "For items stuck waiting on someone else (e.g. vendor spec, ops rotation), ask for blockers instead."

The recalled actionables are work the user OWNS - unit tests, PR merge, ops follow-up, pipeline migration. They are logically distinct from blockers (idx 11-16, memory_kind:blocker) which were not recalled because the tag filter `memory_kind:action` excluded them. The skill recipe correctly separates these domains.

However, there is a recipe weakness: some actionables in the fixture overlap semantically with blockers (e.g. "follow up with ops to rotate Stripe sandbox credentials" is an action, but the underlying blocker is "Stripe sandbox credentials are expired, waiting on ops" - idx 13). The skill surfaces the action correctly, but a user reading the output might wonder whether they are blocked or whether they own the resolution. The skill could optionally note when an action has a corresponding blocker memory.

---

## Overall gate

| Eval | Scripted | Grading | Comparator |
|------|----------|---------|------------|
| 1    | PASS     | PASS    | WITH-SKILL wins |
| 2    | PASS     | PASS    | WITH-SKILL wins |
| 3    | PASS     | PASS    | WITH-SKILL wins |

**actionables: PASS**

All three evals pass scripted assertions. With-skill wins all three comparator rounds. Long-pending item (>30d, still open) is surfaced prominently when no time window is applied, and correctly excluded when a topic+window scope is active. Output is distinctly forward-looking and user-owned, not a duplicate of blockers.

### Recipe weakness observed

The skill recipe says to use `tags: ["memory_kind:action"]`. The backend returns duplicate entries (e.g. "User plans to follow up with ops..." and "User plans to follow up with ops... | Involving: user" are the same fact under two synthesis variants). The recipe does not instruct deduplication. A naive implementation without deduplication would produce a doubled list. The eval outputs above deduplicated by content; the recipe should explicitly say "deduplicate by content before rendering".
