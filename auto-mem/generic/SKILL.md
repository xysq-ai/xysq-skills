---
name: auto-mem
description: "Activate once to turn on recall-before-asking for the rest of the session: before stopping to ask the user a decision or preference question, the agent first queries xysq memory for a prior answer and acts on it silently if found. Distinct from wrap-up (which saves a session into memory) and from the recall skills (which surface memory on demand). Use when the user wants the agent to stop re-asking questions they have already answered."
---

# auto-mem

## When this fires
The user runs `/auto-mem` (or asks the agent to "stop re-asking things", "use my saved preferences", "recall before asking", or "remember what I decided"). This is a **session-mode toggle**, not a one-shot lookup. It activates a standing instruction that persists for the rest of the session.

## Mission
Stop the approval-fatigue loop. Every developer who has run an autonomous agent for more than twenty minutes knows the feeling: "should I use POST or DELETE?", "tabs or spaces?", "which branch?", one question after another for choices the user answered three sessions ago. auto-mem fixes that. At each point where the agent would stop to ask a decision or preference question, it first checks xysq memory for a prior answer. If the memory is clear, it acts and moves on. If memory is silent or ambiguous, it asks like normal. The user's past answers accumulate via wrap-up; auto-mem is what drinks from that store.

This is the forward half of the memory loop. wrap-up is the backward half (saves the session into memory). Together: wrap-up writes, auto-mem reads.

## On activation: what to say
Confirm in one sentence. Something like:

> Recall-before-asking is on for this session. Before each decision or preference question, I'll check your xysq memory first. If I find a clear prior answer I'll act on it and tell you where it came from. If memory is silent or ambiguous, I'll ask you normally. I won't guess.

That is all. No lists, no caveats beyond what's there. Then resume the task.

## How to recall (targeted, per decision point)

At each would-be question, run a targeted recall before asking. Shape it as a lookup for the specific choice at hand.

1. **Frame the query precisely.** Ask for this specific decision, not a broad topic. "What did I decide about HTTP route conventions for deletes?" is the right shape. "API conventions" is too wide.
2. **Use the recall tool** with a low-to-mid budget. A high-budget, expensive search is wrong here: you want a fast targeted lookup, not an exhaustive recall sweep. Low budget first; if it comes back empty, one mid-budget follow-up is fine.
3. **Apply the decision rule:**
   - **Clear hit** (the memory directly answers the choice): act on it. Tell the user in one short line what you did and where it came from: "(from memory: you use POST .../delete, not DELETE routes)". Include the document_id or context string so the user can correct it if it's stale.
   - **No hit or ambiguous hit** (memory is silent, or returns loosely related things that don't clearly answer the specific question): fall back to asking the user. Do not patch ambiguous hits together into a guess. Absence of a clear answer means ask, every time.
4. **Scope:** personal vault by default. Fan out to the team vault only when the decision is clearly about a team-level convention or shared preference, not a personal one.
5. **One tool, one question.** Do not chain recall and reflect for the same decision point. Pick recall; that's the right tool for a targeted decision lookup.

## Grounding discipline

Never guess. Loose analogies ("you used POST elsewhere so I'll assume...") are a failure mode. If memory doesn't clearly answer the question, the right move is to ask. The cost of a wrong assumption compounds across an autonomous run; the cost of one honest question is tiny. Treat ambiguity as absence.

When you act from memory, always surface which memory. The user may know it's stale. The one-liner "(from memory: ...)" is not optional courtesy; it is the mechanism that lets the user correct the loop.

When the user corrects a memory-driven default, that correction is itself a new decision. Point them to wrap-up (or the retain tool) to log it so the loop tightens for next session. The agent can offer to retain it inline: "Want me to save this correction so I don't make the same default next time?"

## What auto-mem does NOT do

Be honest about the boundary. auto-mem reduces the questions the agent asks by answering them from memory. It does not:

- Change permission mode or auto-approve tool calls. "Accept all edits" or "plan mode" are separate levers the user sets directly in their agent client.
- Run in the background unprompted. It is active only within the session it was invoked for.
- Guarantee it finds everything. Memory coverage depends on what was previously saved. A fresh vault means more questions, not guesses.

## Output contract

- On activation: one confirmation sentence (see above). Nothing more.
- At each memory hit: one short inline note "(from memory: <what you found, and its source>)". Then proceed with the action.
- At each miss: ask the question normally. No preamble about the failed recall; just ask.
- Keep the running commentary light. The point is to reduce interruptions, not replace them with narration.

## Example

User runs `/auto-mem`. Agent confirms recall-before-asking is on, then keeps working.

Later, the agent is about to write a new route and would normally stop to ask: "Should I use a DELETE HTTP method or POST .../delete for this endpoint?"

Instead, it first queries memory: "What did I decide about HTTP route conventions for delete operations?" The recall tool returns a prior decision: "No DELETE or PATCH HTTP routes anywhere in the codebase. Use POST .../delete and POST .../update instead."

The agent acts on it and notes in one line:

> (from memory: you use POST .../delete, not DELETE routes)

Then it writes the route and keeps going. No question asked.

Later, the agent hits a genuinely new choice: which of two third-party libraries to use for a new feature, with no prior decision in memory. The recall comes back empty. The agent stops and asks the user normally. One question, clearly necessary.

The user answers, picks library A, and mentions they'd always use it for this class of problem. The agent offers: "Want me to save that as a standing preference?" The user says yes; the agent retains it. Next session, auto-mem answers that question from memory without asking.

<!-- version: 1 -->
