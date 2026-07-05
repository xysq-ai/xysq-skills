---
name: auto-mem
description: "Turn on recall-before-asking for the rest of the session: at every point where the agent would stop to ask a decision or preference question, it first queries xysq memory for a prior answer. If a clear prior decision is found, it acts on it silently and notes the source. If memory is silent, it asks normally. Activate when the user says 'turn on auto-mem', 'recall before asking', 'use memory before asking me', 'stop re-asking me things', or similar. This is the forward-looking half of the memory loop; wrap-up is the backward-looking half that fills the vault auto-mem reads from."
---

# auto-mem

## When this fires

The user wants the agent to stop re-asking questions they have already answered
in a past session. Typical triggers: "turn on auto-mem", "use my memory before
asking", "recall before asking", "stop re-asking things I've decided", "use
xysq to answer your own questions first". Once active, this is a standing
session-wide instruction, not a one-shot lookup.

## Mission

auto-mem is the thing that ends "yes yes yes" fatigue. Every time you would
stop to ask the user a decision or preference question, you first check their
xysq vault for a prior answer. If memory has a clear answer, you act on it and
note the source in one line. If memory is silent, you ask normally.

This is the forward-looking half of the memory loop. wrap-up (the other half)
saves durable decisions at session end. auto-mem reads from that vault before
bothering the user again. Together they form a tightening loop: wrap-up
deposits, auto-mem spends, and corrections shrink the re-asking surface over
time.

## How to activate

When the user turns on auto-mem, confirm in a single line:

> "Recall-before-asking is on. I'll check your xysq memory for prior decisions
> before asking you preference or approval questions. If memory is clear, I'll
> act on it and tell you which memory I used. If memory is silent or ambiguous,
> I'll ask you like normal. I won't guess."

That is the whole activation step. No further setup needed.

## How recall-before-asking works (per decision point)

At every point where you would otherwise stop to ask a decision or preference
question, run a targeted `memory_recall` before surfacing the question.

**Shape the query precisely.** Ask about THIS specific choice, not a vague
topic. Examples:

- "what did the user decide about API route conventions, DELETE vs POST"
- "what is the user's preference for commit message style"
- "what did the user decide about error handling strategy"

Use `budget="low"` for clear preference lookups. Raise to `"mid"` only if the
first call returns empty on a topic you'd expect to be logged.

**Decision rule on the result:**

- Hit that clearly answers the choice: act on it. Tell the user in one short
  line what memory you used, so they can correct it if it's wrong. Example:
  "(from memory: you use POST .../delete, not DELETE routes)"
- No hit, or hits that are ambiguous or only loosely related: fall back to
  asking the user the normal question. Do NOT infer from loosely-related
  patterns. Absence of a memory hit means ask, not improvise.

**Scope.** Personal vault by default. Fan out to the team vault only when the
decision is clearly team-scoped (an architectural convention, a shared API
pattern, a team-level process call).

**Do not stack.** For a single decision point, run one recall call and act on
the result. Do not chain recall + reflect in sequence for the same question.

## Honesty rules

When acting from memory, always surface which memory answered the question, in
plain language: "(from memory: you decided X in [context])" or similar. The
user must be able to spot a stale or wrong memory and correct it on the spot.

When the user DOES correct a memory-driven default, that correction is itself
valuable. Point them at wrap-up (or retain it immediately if they ask): "want
me to save that correction to memory so it holds next session too?" Then do it.
This is how the loop tightens over time.

## What auto-mem does NOT do

Be honest about the boundary. auto-mem reduces the QUESTIONS you ask by
answering them from memory. It does not change the agent's permission posture,
does not auto-approve tool calls, does not bypass confirmation dialogs, and
does not flip any execution mode. If the user wants to change how many
approvals the agent requests for actions, that is a separate lever they control
in the agent's settings. auto-mem only handles the question layer, not the
action layer.

## Grounding discipline

Memory is a LOOKUP, not a license to improvise. If memory returns nothing clear
for a specific decision point, ask the user. If memory returns something that
only loosely rhymes with the choice at hand, ask the user. The fallback is
always "recall, else ask", never "recall, else guess".

## Output contract

On activation: one confirmation line (see above).

At each decision point where memory answered: one short inline note,
e.g. "(from memory: you use X)". Keep it in-line with whatever you are saying,
not a separate block. This keeps the working flow clean.

At each decision point where memory was silent: ask the question normally. No
special framing needed.

## Example

The agent is writing a new API route and is about to ask: "Should I use a
DELETE HTTP method or POST .../delete?"

With auto-mem on, it instead runs:

```
memory_recall(
  query="user decision on API route convention, DELETE vs POST .../delete",
  budget="low",
  types=["observation"]
)
```

The vault returns a prior decision: POST .../delete is the convention across
the project (logged in a wrap-up from two sessions ago). The agent acts on it:

> "Adding the delete route as POST .../delete. (from memory: you use POST
> .../delete, not DELETE routes, as your API convention)"

Later in the same session the agent hits a genuinely new choice: which of two
caching strategies to use for a new endpoint. Recall returns nothing relevant.
The agent asks normally:

> "For the new endpoint, do you want in-process LRU caching or Redis? I don't
> have a prior decision on this one."

The user answers. If they want that answer to hold next session, wrap-up will
capture it. Next session, auto-mem will read it back.

<!-- version: 2 -->
