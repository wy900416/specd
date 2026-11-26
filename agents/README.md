# Agents

These are **role briefs**, not presets. They are plain Markdown so they work with
any agent runner: Copilot, Claude Code, Cursor, DSH, a custom loop, or a human
reading them.

## Available

| Brief | Use it for | Reads |
|---|---|---|
| `spike.md` | quick feedback: one demo path, 90 minutes | `docs/spike.md`, `templates/spike.md` |
| `orchestrator.md` | entry point; delegates and parallelizes | `AGENTS.md`, `docs/fleet.md` |
| `spec-writer.md` | description -> draft | `SPEC.md`, `templates/system.md`, `docs/vibe-spec.md` |
| `gap-filler.md` | infer, assume, escalate, conflict scan | `SPEC.md`, `.agents/skills/spec-gap-fill/` |
| `spec-validator.md` | independent gate; sets `status: validated` | `SPEC.md`, `checklists/validate.md` |
| `change-analyst.md` | mature change -> impact + proposal | `SPEC.md`, `docs/change-mode.md`, `checklists/change.md` |
| `backfiller.md` | existing boundary -> draft baseline | `SPEC.md`, `docs/adoption.md` |
| `architect.md` | validated spec -> fleet-ready plan | `SPEC.md`, `templates/plan.md`, `checklists/plan.md` |
| `implementer.md` | implement a planned track | `SPEC.md`, `plans/<id>.md`, `.context/<id>.md` |
| `verifier.md` | conformance tests written from the spec | `SPEC.md`, the target spec, the test strategy |
| `spec-reviewer.md` | mature-stage consistency and impact | `SPEC.md`, `checklists/review.md` |

## Handoff

```text
quick feedback:  spike -> demo -> feedback -> kill | iterate | graduate
bootstrap:       orchestrator -> writer -> gap-filler -> validator
                                                          |
                                                          v
                                        architect -> implementer + verifier (fleet)
evolution:       change-analyst -> validator + spec-reviewer -> human release
                                                          |
                                                          v
                                        implementer / architect+fleet -> verifier
```

- **spike** is the fast lane: one hypothesis, one demo path, fake boundaries, no
  validator/architect/fleet. It ends with a decision.
- **orchestrator** is the bootstrap entry: it delegates one spec sequentially, then
  plans before implementing.
- **change-analyst** prepares a mature change: impact, compatibility, rollout,
  rollback, approvals, proposed body.
- **backfiller** reconstructs one existing boundary into a draft baseline; a human
  approves it.
- **writer** captures the description and writes the traceable draft.
- **gap-filler** reads the repo and the user's global skills, infers, labels, and
  surfaces conflicts.
- **validator** applies the checklist and sets `validated` only on a clean pass.
  It does not read the writer's rationale.
- **architect** turns the validated spec into `plans/<id>.md`: architecture, file
  map, work tracks, and test strategy. It writes no code.
- **implementer** gets the spec, its ready plan track, and a context pack. If a
  requirement is ambiguous, it stops and reports a spec gap.
- **verifier** gets the spec, the `## Test Strategy`, and the test harness. It
  does **not** get the architecture notes, file map, or the implementer's summary.
- **spec-reviewer** is mature-stage only: cross-service consistency, impact, and
  version hygiene.

The validator and the verifier are separate roles with explicit information
barriers. A gate that reads the author's reasoning stops being a gate.

## Run one

Use the brief as the agent's system prompt or as the first message:

```text
Read AGENTS.md. Follow agents/gap-filler.md and
.agents/skills/spec-gap-fill/SKILL.md. Fill gaps in specs/system/url-shortener.md.
```

Copilot entry points live in `.github/agents/`. Each is a thin wrapper that points
at one of these briefs, so there is one source of truth.

## Why not a preset?

A permanent preset is runner-specific configuration. These briefs are portable and
can be pasted into any agent. Promote one to a preset only when the role and tool
policy are stable.
