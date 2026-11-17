# Agents

These are **role briefs**, not DSH presets. They are plain Markdown so they work
with any agent runner, including DSH subagents.

## Available

| Brief | Use it for | Skills it loads |
|---|---|---|
| `architecture.md` | boundary review, contract impact, cross-service consistency | `spec-context`, `spec-review` |
| `spec-writer.md` | conversational spec generation, drafting, proposals | `spec-interview` |

## Run one in DSH

Use the brief as the subagent's prompt, then give it the concrete task:

```text
Read agents/architecture.md and follow it. Task: review the proposed change to
orders-api. The current spec is specs/contract/orders-api.md.
```

Or, in a normal chat, ask the current agent to load the matching skill and follow
the brief:

```text
Load spec-interview and follow agents/spec-writer.md.
We need a spec for the refund flow.
```

The three skills are auto-discovered by DSH from `.agents/skills/` and appear in
the session skill catalog. A brief alone does not grant tools; the agent still
uses the normal read/write/bash tools, and the brief's boundaries are enforced by
the skill rules and by you.

## Why not a DSH preset?

A permanent agent preset is a Cordis composition change in the DSH profile, not a
workspace file. It affects every session in the profile and needs an explicit
installation step. Start with these briefs; promote one to a preset only when the
role and tool policy are stable.
