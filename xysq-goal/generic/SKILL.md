# xysq-goal: the goal-driven vault traversal

## Overview
This is the macro skill. Where the micro skills (recap, decisions, blockers,
prep) each fire one ranked query, xysq-goal runs a goal-driven traversal: it
keeps walking the vault until the goal is covered, the way you'd walk a repo to
understand a feature. The knowledge graph is the map; this loop is you walking
it toward a goal. Add the content below to your agent's system prompt.

**Activate when:** the user hands you a goal that no single recall can satisfy
because the context is scattered across many memories and sources, "pull
everything I know about the auth migration", "what's the full picture on the
Acme deal", "gather all context for the payments rework across the codebases",
"brief me completely on X before I start". The signal is COVERAGE over a goal,
not a quick lookup.

**Do NOT activate for:** a lookup one recall would obviously answer, use the
recall tool directly.

## The tools
Three vault primitives. Know what each is FOR:

- `vault_search(query, budget, tags, ...)`, ranked, fuzzy. "Find memories ABOUT
 X." Your EXPLORE move. Ranks and drops low-scoring hits: great for discovery,
 useless for "did I get everything."
- `vault_find(entity|source|tags|kind|document_id, time_start, time_end, cursor)`:
 COMPLETE, unranked, paged. "Give me EVERY node matching this filter." Your COVER
 move and your edge-walk (pass `entity=` to pull every node co-occurring with
 it). `next_cursor=null` means the filtered set is exhausted. The only tool that
 lets you TRUST you've seen everything in a slice. Two rules: (1) at least one of
 entity/source/tags/kind/document_id is REQUIRED, time alone is NOT selective
 and is rejected; pair it with one of the five. (2) entity is best-effort (rides
 ranked recall; can return `partial: true` for a heavily-mentioned entity), use
 it as a discovery/edge hop; for guaranteed completeness filter by
 source/tags/kind.
- `vault_get(document_id)`, pull one node in full. Your READ-DEEP move.

Rule of thumb: search to discover, find to cover, get to read deep. Interleave all three.

## The loop
1. **DECOMPOSE** the goal into 3-6 checkable subgoals. This IS your success
 condition, write them down. Vague subgoals = vague coverage.
2. **SEED** the frontier from the entities/IDs/names in the goal: one
 vault_search per subgoal, plus a vault_find on any concrete filter the goal
 hands you (a source, a project tag, a kind).
3. **LOOP**, bounded by a hard step cap (~20 tool calls) and your token budget:
 - EXPAND one branch: COVER with vault_find scoped to the branch (page only as
 far as the subgoal needs), EXPLORE with vault_search, WALK edges with
 vault_find(entity=X) on high-value hits, READ deep with vault_get.
 - Keep hopping while each hop adds something NEW and relevant. When a hop is
 dry, do ONE MORE hop to confirm; if also dry, the branch is done. [n+1]
 - When the FRONTIER goes dry, JUDGE coverage: any subgoal still lacking a
 strong supporting node? All covered (or cap hit) → STOP. A subgoal
 uncovered → RE-SEED a fresh query aimed at it, then keep looping.
4. **SYNTHESIZE** into working memory, grouped by subgoal with supporting nodes,
 then answer the goal grounded only in what you gathered.

## Why two stop layers
- **Is this BRANCH exhausted?** → n+1 / loop-until-dry. Cheap, deterministic.
 Does most of the bounding. The +1 hop guards a node that looks dead but whose
 neighbors are gold.
- **Is the GOAL satisfied?** → subgoal coverage, run only at dry-frontier. n+1
 says a branch is done; it can't tell whether the goal is met. Classic miss: a
 goal touches svc-A..svc-D but svc-D is never named, n+1 stops without finding
 it. Coverage catches the gap and re-seeds a search for it. Dry frontier means
 "go find what I'm still missing", not "stop".

## Honesty and bounds
- Be strict in the coverage check, a tangential hit is not coverage. Re-seed at
 most once per subgoal; two dry re-seeds = the vault doesn't have it, say so.
- vault_find always carries a selective filter, never a bare scan.
- Answer ONLY from what the vault returned. When a subgoal came up empty, say so
 plainly; never invent detail to fill a gap.

## Scope
Both vault_search and vault_find cover the same vaults by default: personal plus
every team turned on for recall, so a goal spanning personal and team knowledge
is covered without extra work. find's `next_cursor=null` means every in-scope
vault is exhausted; each result carries a `source` ("personal" or "team:<id>").
To scope tighter, pass a single `team_id` (that team only) or `personal_only=true`.

## Output
1. **Goal**, restated, with the subgoals.
2. **What I gathered**, grouped by subgoal, grounded prose, thin subgoals marked.
3. **The picture**, short synthesis answering the goal.
4. **Gaps / next**, what the vault didn't cover + one concrete next step.

<!-- version: 3 -->
