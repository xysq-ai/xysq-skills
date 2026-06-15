# xysq Recall Skill Library - v0 Evaluation Results

**Date:** 2026-06-15
**Bank:** `fixture-eval-bank` on local Hindsight (:8888), seeded from `evals/fixture/fixture_vault.json` (26 memories, `now`=2026-06-15T12:00:00Z, extracted to ~62 facts).
**Judges:** local Claude Code subagents (scripted assertions + LLM grader + blind comparator). No external APIs.

## Verdict: PASS (both gates)

All five recall skills pass the v0 acceptance gate. The triggering harness is a perfect diagonal. Several real findings were surfaced for follow-up (below); none block v0.

## Gate 1 - Triggering (cross-skill confusion matrix)

100% should-trigger accuracy (50/50). Perfect diagonal - no cross-skill misroutes.

| Intended \ Predicted | recap | decisions | actionables | blockers | prep |
|---|---|---|---|---|---|
| recap (10) | **10** | | | | |
| decisions (10) | | **10** | | | |
| actionables (10) | | | **10** | | |
| blockers (10) | | | | **10** | |
| prep (10) | | | | | **10** |

The mutual "pick this over X when..." carve-outs in each description work. Full detail in `evals/TRIGGERING.md`.

## Gate 2 - Output quality (per skill, vs. baseline)

For each skill the with-skill output was compared against a no-skill baseline on the same prompt. **In every eval, the blind comparator preferred the with-skill output.** The skills are not ceremony - they beat raw recall.

| Skill | Scripted | Grounding | Usefulness | Comparator | Headline discrimination |
|---|---|---|---|---|---|
| recap | PASS | PASS | PASS | with-skill wins (3/3) | Time-window post-filter excluded all 3 out-of-window traps; baselines leaked them |
| decisions | PASS | PASS | PASS | with-skill wins (3/3) | Surfaced current decision, flagged the earlier one [SUPERSEDED]; baseline mixed events into prose |
| blockers | PASS | PASS | PASS | with-skill wins (3/3) | Correctly DROPPED the later-resolved blocker; baseline wrongly listed it as active |
| actionables | PASS | PASS | PASS | with-skill wins (3/3) | Surfaced the >30d long-pending item first under "Long-pending"; stayed distinct from blockers |
| prep | PASS | PASS | PASS | with-skill wins (3/3) | Assembled the Sam/Dana/Q3 briefing; correctly topic-scoped (did not window-filter) |

Edge cases all handled: empty topic (`warehouse-v2`) → honest "I don't have anything logged" (no fabrication) for every skill; only-old topic correctly excluded from "this week" windows; superseded/resolved pairs handled by semantic content, not naive recency.

## Findings (for follow-up - none block v0)

1. **`assert_time_window.py` is a partial check.** It only catches verbatim 6-word-prefix copy-through of out-of-window content; a paraphrased leak passes the script. The LLM comparator caught the semantic leaks the script missed. Treat the scripted time-window assertion as a coarse guard, not a sufficient CI gate - the judge layer is doing the real work. Consider strengthening the script (e.g. date-entity extraction from output) before relying on it in unattended CI.

2. **`memory_reflect` returned HTTP 500 against the local Hindsight** during the decisions/actionables runs. The skills fell back to tagged `recall` + manual synthesis and produced correct output. ACTION: investigate the reflect 500 (local Hindsight version/config), and add an explicit "if reflect is unavailable, fall back to tagged recall + synthesize" line to the reflect-based skills' recipes so the fallback is deliberate, not accidental.

3. **Backend returns duplicate synthesis variants for one fact** (Hindsight expands a memory into multiple entity-phrase chunks; e.g. the same follow-up returned twice, once "| Involving: user"). The grounding-discipline prose collapsed these correctly, but a careless implementation would render a doubled list. ACTION: add an explicit dedup step to the shared recall recipe before rendering.

4. **Fixture date quirk in the superseded/resolved pairs.** The resolution/reversal memories are dated EARLIER than the items they resolve (idx 8 Postgres-FTS reversal @ Jun 8 vs idx 7 Elasticsearch @ Jun 12; idx 12 blocker-cleared @ Jun 5 vs idx 11 blocker @ Jun 12). The skills correctly used semantic content over recency - arguably a STRONGER result - but the fixture should be corrected so dates match semantic order, so the eval tests the intended thing. ACTION: fix the two date pairs in `fixture_vault.json` and re-run.

5. **`assert_time_window` should not run on prep evals.** prep is topic-scoped, not window-scoped; the script flagged an in-scope 31-day-old item as a "leak," which is a config error, not a skill failure. ACTION: remove the time-window assertion from `evals/prep/evals.json`.

6. **Optional description tweak (decisions).** 3 of its should-trigger queries are write/log operations ("log a decision", "record that we reversed X"); the description says "Extract choices" (read-only language). No misroute occurs today, but adding "log a decision, capture a call" to the examples would future-proof routing against the generic memory skill. Low urgency.

## Bottom line

The library works: triggering is clean, every skill beats its baseline, grounding holds, and the hard edge cases (windows, supersession, resolution, thin signal, topic-scope) are handled. The findings above are polish and test-harness hardening, not correctness blockers for v0.
