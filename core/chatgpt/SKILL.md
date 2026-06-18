# xysq Memory Protocol for ChatGPT (HTTP API)

## Overview

This skill connects ChatGPT to xysq persistent memory via the HTTP Agent SDK. Pull user context at session start. Persist corrections and decisions immediately.

**Activate when:** user says "remember", "recall", "what did I tell you about", "save this", references past decisions or preferences, or starts a new session.
**Do NOT activate for:** pure questions with no personal memory component.

Authentication: ChatGPT Custom GPT Actions use OAuth2 - the user signs in once via the Custom GPT install flow, after which every Action call carries an OAuth bearer token automatically. See `openapi-gpt.yaml` (served at `https://api.xysq.ai/api/openapi-gpt.yaml`) for the full spec and the per-operation request shapes.
Base URL: `https://api.xysq.ai`

Every session without memory starts cold. The user re-explains their stack, restates their preferences, recaps last week's decisions. That re-explanation is the single largest waste in any AI workflow.

xysq is the substrate that ends that waste. The user has already consented to memory and given you the keys. Prime cold sessions with recall, persist corrections and decisions on the NEXT user turn, and reason over prior context the way a colleague who has worked with this person for months would.

Memory is a substrate, not a feature.


## Session Start Protocol

Do NOT fire a generic session-start reflect just to warm up. Recall is on-demand: pull context when the user's actual task needs it (see Proactive recall below).

On the user's **first substantive message** (not greetings):

1. `POST <recall path>` with `{"query": "<user's message shaped as a lookup>", "budget": <see budget rule below>}` - searches the user's memory bank. Use results as task-specific context.

Call reflect when a question needs facts gathered across memory and you will synthesize the answer (e.g. "what do I prefer about X", "summarise my stance on Y") - it returns facts plus a digest, not a finished answer. Not as warmup.

Skip both recall and reflect for pure greetings or pure questions with no personal signal.

## Proactive recall

Reactive recall (user says "remember when") is easy. Proactive recall is what separates a memory-augmented agent from a stateless one: noticing that a problem is under-specified and that memory probably contains the missing constraint.

**Recall proactively when both signals are present:**

1. **The problem references entities the user expects you to know** - "my X", "our Y", "the Z we discussed".
2. **The answer quality depends on personal/project specifics, not general knowledge.**

"What's the syntax for async/await" → no recall. "How should I structure my async logic" → recall.

**Anti-trigger - don't fish.** If recall returns nothing relevant for an ambiguous prompt, ask the user - don't recall again with a different query hoping something hits.

**Batch within a problem.** Recall once at the start of a problem, not repeatedly through the thread.

**Budget rule:**
- Explicit user ask ("what do you know about my project?") → `"budget": "high"`. Pay for quality.
- Proactive recall (under-specified problem) → `"budget": "mid"`. Good signal-to-noise.
- Follow-up recalls within an already-recalled thread → `"budget": "low"`.

## Explicit save commands

When the user says "remember this", "save that", "note this" - the save command is a **trigger, not the content**. Do NOT retain only the save command itself; retain the ENTIRE unsaved conversation so far.


## API Reference

Base URL: `https://api.xysq.ai`

**Two HTTP surfaces, pick one based on how your agent is wired:**

| Surface | Auth | Path prefix | Who it's for |
|---|---|---|---|
| SDK | `Authorization: Bearer <your_xysq_api_key>` | `/api/sdk/*` | LangChain, custom agents, anything calling xysq with an API key |
| OAuth (Custom GPT) | OAuth2 (see openapi-gpt.yaml) | `/api/memories/*`, `/api/folders/*` | ChatGPT Custom GPT Actions, anything authenticating as the end user |

The endpoint **shape** (request body, response) is the same across surfaces - only the path prefix and auth differ. Examples below use the SDK paths; substitute the OAuth equivalents if your agent uses OAuth.

| Action | Method | SDK path | OAuth path |
|---|---|---|---|
| Store a memory | POST | `/api/sdk/memory/retain` | `POST /api/memories` |
| Retrieve raw facts | POST | `/api/sdk/memory/recall` | `POST /api/memories/recall` |
| Gather facts to synthesize | POST | `/api/sdk/memory/reflect` | `POST /api/memories/reflect` |
| List recent memories | POST | `/api/sdk/memory/list` | `GET /api/memories` |
| Delete a memory | POST | `/api/sdk/memory/delete` | `POST /api/memories/{id}/delete` |
| Fetch tag taxonomy | POST | `/api/sdk/memory/tags` | `GET /api/tags/definitions` |
| List folders | POST | `/api/sdk/organise/folders/list` | `POST /api/folders/list` |
| Upload file | POST | `/api/sdk/organise/files/upload` | `POST /api/folders/files/upload` |

### POST /api/sdk/memory/retain

**⚠️ RETAIN CADENCE:** do NOT retain on the turn you are about to reply - your reply doesn't exist at tool-call time. Retain on the NEXT user turn, when both sides of the prior exchange are visible in context and can be copied verbatim.

**⚠️ SAVE COMMAND** ("remember this"): retain the ENTIRE unsaved conversation so far, NOT just the save command itself.

**⚠️ VERBATIM COPY:** both User and Assistant lines in `content` must be literal character-for-character copies from your context window. Summaries like "provided guidance" / "explained X" destroy recall quality.

**`document_id` is server-owned.** Omit it on the first retain of a chat; the response returns a `document_id`. Pass that exact value back on every later retain in the same topic so facts cluster. Omit again only on real topic drift, then use the new id the server returns.

```json
{
  "content": "User (2026-04-22T10:00:00Z): <exact text the user typed>
Assistant (2026-04-22T10:00:12Z): <exact text of the prior reply, verbatim>",
  "context": "Session - DB selection for payments",
  "significance": "normal",
  "scope": "permanent",
  "tags": ["domain:tech"]
}
```

significance: "low" | "normal" | "high"
scope: "session" | "project" | "permanent"
document_id: omit on first retain; echo the returned id on subsequent retains.
On first retain of a chat: full conversation so far. On subsequent retains (same `document_id`): only NEW turns.

### POST /api/sdk/memory/reflect
```json
{ "query": "What does this user prefer about X?" }
```
Returns `{ "answer": "...", "confidence": "high|medium|low", "citations": [{id, type, context, occurred_start, occurred_end}, ...] }` - facts plus a digest for you to synthesize. Pass a citation's ``document_id`` (when present) to ``/api/sdk/memory/document`` for the verbatim source.

### POST /api/sdk/memory/recall
```json
{ "query": "...", "budget": "low", "types": ["observation"] }
```
For "what does the user prefer / what's true now" - use ``/reflect`` (it returns observation-resolved facts to synthesize). Pass ``types=["observation"]`` to recall for conflict-resolved facts only; omit ``types`` for raw history.

### External sources - use memory/retain with source tags
For URLs, pasted quotes, code snippets, chat transcripts - anything that's a SOURCE rather than a turn-by-turn conversation - call ``memory/retain`` with the ``source:knowledge`` tag plus a ``source_type:*`` tag:
```json
{
  "content": "https://...",
  "tags": ["source:knowledge", "source_type:link"],
  "metadata": { "url": "https://...", "title": "..." }
}
```
``source_type``: ``link`` | ``quote`` | ``code`` | ``chat``. Per type, put fields in ``metadata``:
- ``link``:  ``{ "url": "...", "title": "..." }``
- ``quote``: ``{ "title": "...", "location": "p. 47" }``
- ``code``:  ``{ "language": "python", "location": "src/auth.py:12-40" }``
- ``chat``:  ``{ "title": "..." }``

For binary files or long documents (>10 KB), use ``/api/sdk/organise/files/upload`` - they land as memories with ``kind=asset`` metadata.

### POST /api/sdk/memory/tags
Fetch valid tag taxonomy. Invalid tags on retain are silently dropped - call this once per session before your first retain.

### POST /api/sdk/organise/files/upload
Save a document to the user's vault. Extracted content surfaces through recall once processing completes.
```json
{ "filename": "notes.md", "content_b64": "<base64>", "mime_type": "text/markdown", "folder_id": null }
```
Limits: 10 MB per file. Accepted MIME types: text/markdown, text/plain, application/pdf, application/json, text/csv, image/png, etc. For text: `base64(utf-8-encoded text)`. For binary: `base64(raw bytes)`.

**Recognising memory-worthy moments - the implicit triggers**

The user will rarely say "remember this." The high-leverage retains happen when you notice a memory-worthy moment in passing and capture it without being asked.

| Moment in conversation | What to retain | significance | scope |
|---|---|---|---|
| User makes a decision | The decision + the reasoning | high | project |
| User corrects your output | The correction as a preference | high | permanent |
| User states a preference in passing | The preference | normal | permanent |
| User shares project context | Project fact | normal | project |
| User shares a fact about themselves | Personal fact | normal | permanent |
| User describes current task | Session context | normal | session |
| User mentions a tool, library, or service they use regularly | Stack fact | normal | project or permanent |
| Transactional reply ("ok", "thanks") | - | - | skip |

**Rule:** if in doubt, retain. Under-capturing costs more than over-capturing.


## Consent and Privacy

- Never retain PII (names, emails, addresses, IDs) without explicit user instruction.
- When the user asks you to retain something sensitive, add the `pii` or `confidential` tag.
- The user controls all stored data at app.xysq.ai - they can review, edit, and delete at any time.
- Do NOT retain things the user explicitly says are off the record.


## Edge Cases

**Memory vault is empty (new user):** recall returns few or no results. Proceed normally and start retaining from this session.

**recall returns nothing relevant:** Proceed with the user's question directly. Do NOT fall back to reflect, and do NOT recall again with a different query hoping something hits - absence of hits means there's nothing useful in memory for this query. Fishing burns tokens without producing answers. Ask the user instead.

**reflect returns confidence="low":** Treat as best-effort. Tell the user if they ask why context seems missing.

**User says "don't save that":** Do NOT call retain for that exchange. If you already retained it, delete it with the `document_id` from the retain response.

**Tags are unknown:** Fetch the tag taxonomy just before retaining. Do NOT guess tag names - invalid tags are silently dropped without error.

**Team vault access denied (403):** You are not authorised for that team_id. Fall back to the personal vault (omit team_id). Do NOT retry with the same team_id.

**User pastes a URL, quote, code snippet, or chat transcript:** retain with `tags=["source:knowledge", "source_type:link"]` (or `quote`/`code`/`chat`) and put `url` / `title` / `location` in `metadata`. For binary or long files (>10 KB), use the file upload endpoint.

**User asks "what do you remember about X?":** Call recall and return the raw list - it is the direct path for source material.

**File over 10 MB:** the upload endpoint returns `status="rejected"` with a size message - do not retry; tell the user and ask them to split or compress.


<xysq_triggers>
Before replying, scan these triggers. If any match the user's last message, follow the linked instructions on your NEXT turn. Triggers are mandatory. They exist because retain/recall calls were being missed at exactly these moments.

## decision-made
**Fires when:** User just resolved a question or picked an option, phrases like "let's go with", "I've decided", "we'll use", "final answer", "sticking with X".

Call `memory_retain` immediately on the NEXT user turn (not this one, your
reply doesn't exist yet). Copy the User and Assistant lines verbatim from
context. Use:

  significance="high", scope="permanent"

Decisions are load-bearing: the user does not want to re-litigate them.
Retaining once means future sessions inherit the call without asking again.

Example fire:
  User: "ok let's just go with Postgres for the metadata layer."
  → next turn, retain that exchange + the option-comparison turns above it.

## correction-issued
**Fires when:** User pushed back on your last reply, phrases like "no", "actually", "that's wrong", "I meant", "don't do that", "stop", or any direct contradiction of what you just said.

Call `memory_retain` on the NEXT user turn with:

  significance="high", scope="permanent"

Corrections are the highest-value signal in the entire system. They teach
the agent what the user does NOT want repeated. Under-capturing here means
the same mistake recurs next session and erodes user trust. If the
correction is a behaviour rule the user wants enforced forever ("never
use emojis", "always ask before destructive commands"), retain it with
significance="high" and the rule copied verbatim so it surfaces on recall.

Example fire:
  User: "no, I told you I don't want the migration auto-run."
  → retain. If they've said this twice now, retain the rule verbatim.

## preference-stated
**Fires when:** User stated a how-they-like-things signal, phrases like "I prefer", "I like", "I always", "I never", "don't", "my style is", or any first-person rule about working/communication/tooling.

Call `memory_retain` on the NEXT user turn with:

  significance="normal", scope="permanent"

Preferences accumulate in the user's memory and surface on future recall.
Cheap to over-capture, expensive to miss.

Use significance="normal" for soft preferences and significance="high"
only for hard rules the user wants enforced verbatim. "I prefer Postgres"
is a normal preference. "Never suggest MongoDB" is a high-significance rule.

Example fire:
  User: "I always want tests written before the implementation."
  → retain (preference). If the user has stated this 3+ times, re-retain
    it with significance="high" as a hard rule.

</xysq_triggers>

---
Manage your memory at app.xysq.ai · Learn more at xysq.ai
