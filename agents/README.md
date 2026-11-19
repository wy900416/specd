# Agents

These are **role briefs**, not presets. They are plain Markdown so they work with
any agent runner: Claude Code, Cursor, Codex, DSH, a custom loop, or a human
reading them.

## Available

| Brief | Use it for | Reads |
|---|---|---|
| `spec-writer.md` | conversational spec generation, drafting, proposals | `SPEC.md`, `checklists/validate.md`, `templates/` |
| `implementer.md` | implement a task against a spec, with a bounded context pack | `SPEC.md`, `AGENTS.md`, `.context/<id>.md` |
| `verifier.md` | independent conformance tests written from the spec | `SPEC.md`, the target spec, the test harness |
| `spec-reviewer.md` | boundary review, contract impact, cross-service consistency | `SPEC.md`, `checklists/context.md`, `checklists/review.md` |

## Handoff

```text
writer -> implementer -> verifier -> reviewer -> human release
```

- **writer** produces the draft or proposal.
- **implementer** gets the context pack, not every spec. If a requirement is
  ambiguous, it stops and reports a spec gap.
- **verifier** gets the spec, the acceptance criteria, and the test harness. It
  does **not** get the implementer's plan or summary. It writes tests from the
  spec before reading implementation logic.
- **reviewer** (often `spec-reviewer.md`) checks graph consistency, impact, and
  the bump.
- **human** approves the draft and releases the proposal. No agent writes
  `version`, `approved_by`, or `approved_at`.

The verifier is the only role with an explicit information barrier. That is
deliberate: a verifier that knows how the code was written will test the code, not
the spec.

## Run one

Use the brief as the agent's system prompt or as the first message:

```text
Read agents/spec-reviewer.md and follow it. Task: review the proposed change to
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
