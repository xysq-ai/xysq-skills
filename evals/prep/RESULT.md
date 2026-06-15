# prep skill eval results

now = 2026-06-15T12:00:00Z  
bank = fixture-eval-bank (76 memories after two loads; topic:sam loaded in second run)  
skill = /Users/Ximi-Hoque/Workspace/xysq/xysq-skills/prep/claude-code/SKILL.md

---

## Eval 1 - "prep me for my 1:1 with Sam"

### Scripted

| script | config | result |
|--------|--------|--------|
| assert_structure.py | skill=prep | PASS |
| assert_time_window.py | window_days=30 | FAIL (expected - see note) |

**Time window note:** idx 23 (Sam+Dana billing roadmap deferral, 2026-05-15, 31d old) appears in the with-skill output. This is intentional - prep is topic-scoped and the recipe explicitly says "do NOT restrict by time window." The assert_time_window script flags it as a leak but prep is not a window-scoped skill. This is a script-vs-recipe mismatch, not a skill failure.

### Grader

| dimension | result |
|-----------|--------|
| grounding | PASS |
| usefulness | PASS |

All claims traceable to Sam-topic memories. Correctly assembled: roles (Sam=EM, Dana=PL), Q3 roadmap alignment meeting, auth latency demo requirement, billing deferral to Q4, two concrete decision items. No hallucinations.

### Blind comparator

winner: **with-skill (A)**  
reason: With-skill stays focused on Sam-relevant context and closes with decision items. Baseline pads output with unrelated auth/eventstore progress (hotfix, token-refresh, load test) that has no bearing on the 1:1 with Sam.

---

## Eval 2 - "what do I need to know before my meeting with Dana"

### Scripted

| script | config | result |
|--------|--------|--------|
| assert_structure.py | skill=prep | PASS |

### Grader

| dimension | result |
|-----------|--------|
| grounding | PASS |
| usefulness | PASS |

Correctly identifies Dana as Product Lead, surfaces her agenda (milestone acceleration, stakeholder presentation on auth latency), and closes with two actionable items. All claims traceable to recalled Sam-topic memories.

### Blind comparator

winner: **with-skill (A)**  
reason: With-skill stays on Dana-relevant context. Baseline introduces a mild framing hallucination by attributing recent auth events (hotfix, token-refresh, load test) as "the milestones Dana mentioned wanting to push forward" - no memory makes that specific link.

---

## Eval 3 - "prep me for a meeting about warehouse-v2"

### Scripted

| script | config | result |
|--------|--------|--------|
| assert_thin_signal.py | - | PASS |

### Grader

| dimension | result |
|-----------|--------|
| grounding | PASS |
| usefulness | PASS |

Correctly identifies no warehouse-v2 content. Offers to search a related term per recipe. Notes what general warehouse context does exist without asserting it applies to warehouse-v2.

### Blind comparator

winner: **with-skill (A)**  
reason: With-skill leads with the thin-signal acknowledgment cleanly, then offers a next step. Baseline lists all warehouse pipeline details without clarity on whether they apply to warehouse-v2, making the thin-signal less clear.

---

## KEY CHECK: Sam meeting context assembly

**Did the with-skill output pull the Sam/Dana/Q3-roadmap context and frame it as prep?**  
YES. The output assembles all three Sam-topic memories (idx 21, 22, 23) into a briefing with Background / Recent activity / Open threads / Anything needing a decision. It names Sam's role, Dana's role, the Q3 roadmap alignment meeting, the auth latency demo requirement, and the billing deferral.

**Is it correctly topic-scoped (not window-filtered)?**  
YES. Idx 23 (31d old) was correctly included - the prep recipe says "Pull broadly - do NOT restrict by time window." The assert_time_window FAIL is a script limitation, not a skill error.

---

## OVERALL GATE

| eval | scripted | grounding | usefulness | comparator |
|------|----------|-----------|------------|------------|
| 1 | PARTIAL (assert_time_window FAIL is by-design for prep) | PASS | PASS | with-skill wins |
| 2 | PASS | PASS | PASS | with-skill wins |
| 3 | PASS | PASS | PASS | with-skill wins |

**prep: PASS**

The skill reliably assembles relevant context for a named meeting/person, formats it as an actionable briefing, handles thin-signal topics correctly, and consistently outperforms the naive baseline.

---

## Recipe weakness

One issue to watch: the recall engine returned many duplicate/paraphrased versions of the same underlying memory (e.g., 12 Sam-tagged results that are really 3 source facts expanded into multiple entities/phrases by Hindsight ingestion). The skill output correctly collapsed these into clean prose, but a naive skill could repeat the same fact multiple times. The grounding discipline ("natural summary, not a citation dump") is doing useful work here.

The assert_time_window script should not be run against prep outputs - prep is explicitly not window-filtered. Consider removing or marking it as N/A in evals.json, or replacing with a topic-coverage check.
