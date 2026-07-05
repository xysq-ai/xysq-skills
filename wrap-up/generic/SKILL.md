# wrap-up: summarize a session into durable memory, losslessly

## Overview
Add the content below to your agent's system prompt. wrap-up is the loop's
persistence step: when a working session ends, it extracts the durable knowledge
into one compact, recallable memory so the next session (yours or a teammate's)
starts informed instead of blank.

**Activate when** the user says "wrap up", "summarize this session and save it",
"save what we did", "checkpoint this", "store this session", or signals the
session is ending and wants it persisted. Fire only on an explicit request,
never unprompted.

## Mission
Compress the session for STORAGE, not for reading aloud. The contract is exact:
**lose no knowledge, just tokens.** A vague prose summary ("discussed auth, made
some decisions") is a FAILURE, it stores nothing recallable. You are extracting
the durable atoms a future session would need, and dropping only true filler.

Think of this as the INVERSE of a context-compaction summary. Compaction
summarizes for the model's working memory, so it keeps the conversation's shape
and accepts losing precision (exact numbers, code snippets, variable names,
carefully worded constraints are its first casualties). wrap-up wants the
opposite trade: you may drop the shape (the back-and-forth, resolved dead-ends,
chatter), but you must KEEP exactly that precision, because it is what a future
recall actually needs.

Filler you may drop: greetings, acknowledgements, thinking-out-loud that led
nowhere, dead-ends resolved later, chatter that names no fact, decision, person,
file, or method. NEVER drop: any decision, fact, blocker, task, correction,
preference, or concrete detail (names, numbers, file paths, commands, errors).

## How to summarize (structured extraction + a condensation catch-all)
Walk the whole session and pull the knowledge into buckets. Each item is one
tight line, dense but complete (keep the WHY, the WHO, the exact value):

1. **Decisions** - every choice made, with rationale. Tag `memory_kind:decision`.
2. **Facts** - durable facts about the project, code, people, systems.
3. **Blockers** - what's stuck and what/who it waits on. `memory_kind:blocker`.
4. **Open tasks** - what's still to do, with deadlines. `memory_kind:action`.
5. **Corrections & preferences** - anything the user corrected you on or stated
   as a preference. Keep close to verbatim, highest-value lowest-token memories.
   This includes operating/autonomy preferences (e.g. "stop asking me to approve
   every step, act on my past decisions"), not just output corrections. Capture
   these verbatim; they're what a future session needs most.
6. **Condensation catch-all** - anything important that doesn't fit a bucket,
   condensed to the fewest words that keep every concrete claim. The safety net.

Assemble ONE compact document from these buckets (sections in order; omit empty
ones). Before saving, scan once more: "any decision, fact, blocker, task,
correction, or concrete detail I left out?" If yes, add it. Compression that
drops knowledge is the one thing this skill must never do.

## How to save it (one document per session, re-run updates it)
Mint ONE `document_id` for the session on the first wrap-up and REUSE it every
later wrap-up in the same session, with `update_mode="replace"`, so the session
is one living document that stays current, never a stack of duplicates.

First wrap-up of the session:
```
memory_retain(
  content=<the assembled compact summary>,
  context="<client> session summary: <one-line topic>",
  tags=["memory_kind:decision", ...other memory_kind tags you used...],
  significance="high",
  scope="project",
  document_id=<omit on the very first call>,
)
```
The server returns a `document_id`. Remember it for this session.

Every later wrap-up in the SAME session:
```
memory_retain(
  content=<the freshly re-assembled summary over the WHOLE session so far>,
  context="<client> session summary: <one-line topic>",
  tags=[...],
  significance="high",
  scope="project",
  document_id=<the SAME id the first wrap-up returned>,
  update_mode="replace",
)
```
Re-assemble over the whole session each time, then `replace`: one document that
always reflects the latest state, no duplicates. If `update_mode` is not
available in your client, reuse the same `document_id` anyway so re-runs cluster
into one document instead of scattering. If you cannot recover the earlier id
(context was lost), recall this session's summary first rather than minting a new
one; only mint fresh as a last resort, and say so.

## Scope: personal by default, team on request
- Default: personal vault (omit team_id).
- "Save this to the team" / "save to <team name>": call list_teams for the id,
  then pass `team_id=<that id>` so the summary lands in the shared team vault.
  This turns your session into the team's starting context. A team save still
  mirrors to your personal vault (tagged with the team).

## Grounding discipline
Summarize ONLY what actually happened. Do not infer or embellish. If the session
was thin, say so and save a short honest summary rather than padding it.

## After saving, confirm briefly
Tell the user in one or two lines what you saved (the buckets captured, personal
or team) and that re-running updates this same memory. Don't dump the full
summary back unless asked.

<!-- version: 2 -->
