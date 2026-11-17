# Agents

These are **role briefs**, not presets. They are plain Markdown so they work with
any agent runner: Claude Code, Cursor, Codex, DSH, a custom loop, or a human
reading them.

## Available

| Brief | Use it for | Reads |
|---|---|---|
| `architecture.md` | boundary review, contract impact, cross-service consistency | `SPEC.md`, `checklists/context.md`, `checklists/review.md` |
| `spec-writer.md` | conversational spec generation, drafting, proposals | `SPEC.md`, `checklists/validate.md`, `templates/` |

## Run one

Use the brief as the agent's system prompt or as the first message:

```text
Read agents/architecture.md and follow it. Task: review the proposed change to
orders-api. The current spec is specs/contract/orders-api.md.
```

Or, in a chat, point the agent at the brief and the matching skill:

```text
Read AGENTS.md. Load .agents/skills/spec-interview/SKILL.md and follow
agents/spec-writer.md. We need a spec for the refund flow.
```

The skills live in `.agents/skills/` as plain Markdown. DSH discovers them
automatically; other agents can read the same files, or copy the folders into
their own rules directory. No installation or runtime is required.

## Why not a preset?

A permanent preset is runner-specific configuration. These briefs are portable and
can be pasted into any agent. Promote one to a preset only when the role and tool
policy are stable.
