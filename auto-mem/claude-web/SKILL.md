---
name: auto-mem
description: "Activate once to turn on recall-before-asking for the rest of the session: at every point the agent would stop to ask a decision or preference question, it first queries xysq memory and acts on a clear prior answer silently. Fire when the user says /auto-mem, 'recall before asking', 'use my past decisions', 'stop re-asking me things', or 'check memory before you ask'. Distinct from wrap-up (which saves the session) and decisions (which lists past calls): auto-mem is forward-looking recall wired into the question loop, not a lookup or a save."
---

# auto-mem

## When this fires
The user runs `/auto-mem`, or says something like "use my past decisions", "stop
re-asking me things I've already answered", "check memory before asking me", or
"recall before asking". This is a session-mode toggle, not a one-time lookup.
It activates for the rest of the current conversation. Do not fire unprompted.

## Mission
Stop the "yes yes yes, approve every step" fatigue. The agent normally halts at
every decision point and asks the user. auto-mem inserts a memory check first:
if xysq already has a clear answer, act on it quietly and keep moving. If memory
is silent, ask like normal. Never guess. Never extrapolate from loosely-related
patterns and call it a preference.

This is the forward-looking half of the memory loop. wrap-up is the
backward-looking half: it compresses a session and saves the durable decisions.
auto-mem drinks from what wrap-up (and any other retain) has already put there.
The two together are a tightening loop: you save preferences once, you never get
asked the same question twice.

## On activation: confirm in one line
When the user fires `/auto-mem`, reply with exactly one short confirmation. Tell
them:
- recall-before-asking is now on for this session
- what it will do (acts silently on clear memory hits, notes the source)
- what it won't do (does not flip permission posture; does not auto-approve tool
  calls; does not guess when memory is silent)

Example confirmation:

> "Recall-before-asking is on. I'll check your xysq memory before stopping to
> ask decisions or preferences. If I find a clear past answer, I'll act on it
> and note it. If memory is silent, I'll ask you normally. This does not change
> approval or permission settings."

## How to recall at each decision point

The mode is sticky. From the moment `/auto-mem` activates until the conversation
ends, apply this at every point you would otherwise pause to ask the user a
decision or preference question:

1. **Shape a targeted query.** Don't run a broad recall. Ask for THIS specific
   choice: "what did the user decide about <the exact choice>". Include intent-
   shaped keywords: "decided, prefer, convention, rule, always, never". Pass
   `budget="low"` for common preference lookups (fast, cheap); escalate to
   `budget="mid"` only if the low hit is thin and the decision is consequential.

2. **Apply the decision rule:**
   - **Clear hit:** the memory directly and unambiguously answers the choice.
     Act on it. Tell the user in one short line what you found and from where.
     Format: "(from memory: you decided X)" or "(from memory: your standing
     preference is X)".
   - **Ambiguous or low-signal hit:** the memory is loosely related but doesn't
     clearly resolve this specific choice. Fall back to asking the user. Do not
     stretch a vague hit into a confident answer.
   - **No hit:** fall back to asking the user. Absence of a memory hit means
     ask, not improvise.

3. **Scope:** personal vault by default. Fan out to a team vault only when the
   decision is clearly team-scoped (a shared API convention, a team-agreed rule).
   Don't fan out speculatively.

4. **One tool call per question.** Do not stack `memory_recall` + `memory_reflect`
   for the same question. Pick recall. Reflect is for synthesis over many facts;
   this is a targeted lookup.

## Honesty: surface which memory, accept corrections

When acting from memory, always tell the user which decision you found (a brief
paraphrase, not a full dump). This gives them the chance to override it. If they
correct you ("no, I changed that, use Y instead"), treat the correction as a new
preference. Point them at wrap-up or memory_retain to persist the correction so
the loop tightens: the wrong answer won't come back next session.

## What auto-mem does NOT do

Be crisp about the boundary:

- It does not flip Claude.ai's permission posture or auto-approve any action the
  user would otherwise review. Permission settings are a separate lever you
  control.
- It reduces the number of QUESTIONS by answering them from memory. It does not
  reduce the number of tool calls or file writes you review.
- It does not retain new memories itself. For that, use wrap-up at the end of the
  session, or ask the agent to retain a specific fact via memory_retain.

## Grounding discipline

Act on memory only when the hit clearly resolves the choice in front of you.
"Loosely consistent with" is not good enough. Prefer asking the user over acting
on a weak signal. A wrong answer from memory is more damaging than a repeated
question, because it silently encodes a mistake.

## Example

User runs `/auto-mem`. Agent confirms recall-before-asking is on.

Later, the agent is about to add a new API endpoint and needs to decide the HTTP
verb for a delete operation. Instead of asking, it runs:

```
memory_recall(
  query="what did user decide about HTTP verb for delete routes, API convention",
  budget="low",
  types=["observation"]   // a standing convention: return the resolved current fact
)
```

Hit: a session summary from wrap-up that says "user prefers POST .../delete over
DELETE routes (API convention)."

Agent acts and notes it:

> "(from memory: you use POST .../delete, not DELETE routes) Adding the endpoint
> as POST /entries/delete."

Later, the agent hits a genuinely new choice: whether to paginate a list endpoint
by cursor or offset. No memory hit. It asks the user normally:

> "Should I paginate this with a cursor or an offset? I don't have a past
> preference logged for this."

User answers. Agent acts. If the user then says "wrap up", wrap-up will save that
preference so auto-mem can recall it next time.

<!-- version: 2 -->
