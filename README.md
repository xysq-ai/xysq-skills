# xysq-skills

Single source of truth for all xysq skills delivered to AI agents.

## Layout

```
<skill-name>/<platform-key>/SKILL.md
```

The filename is always `SKILL.md`. The consumer (backend skill_sync) maps platform key to the correct file extension on the way out.

## Skills

### `core/`

The xysq memory skill - teaches an agent how to use the xysq MCP tools (retain, recall, reflect, delete, organise). Migrated from the backend's `skill/templates.py::get_baseline`. Available for all 9 platform keys.

### `recap/`, `decisions/`, `actionables/`, `blockers/`, `prep/`

Recall library skills for structured meeting and work summaries. Claude-code only in v0, structured to hold more platforms later.

## Platform keys

| Key | Platform |
|-----|----------|
| `claude-code` | Claude Code CLI |
| `claude-desktop` | Claude Desktop |
| `cursor` | Cursor IDE |
| `windsurf` | Windsurf IDE |
| `chatgpt` | ChatGPT (plugin/action) |
| `codex` | OpenAI Codex CLI |
| `gemini-cli` | Gemini CLI |
| `copilot-cli` | GitHub Copilot CLI |
| `generic` | Any other agent/platform |

## Shared assets

`_shared/` holds content snippets reused across skills (tool reference tables, common instructions, etc.).

`evals/` holds evaluation harnesses and test prompts for skill quality checks.

## Style rules

- No em dashes anywhere in skill content or docs - use hyphens, commas, or split sentences.
- Keep SKILL.md files self-contained: a consumer should be able to deliver the file as-is with no post-processing beyond extension mapping.
