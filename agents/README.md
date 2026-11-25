# Agents

These are **role briefs**, not presets. They are plain Markdown so they work with
any agent runner: Copilot, Claude Code, Cursor, DSH, a custom loop, or a human
reading them.

## Available

| Brief | Use it for | Reads |
|---|---|---|
| `orchestrator.md` | entry point; delegates and parallelizes | `AGENTS.md`, `docs/fleet.md` |
| `spec-writer.md` | description -> draft | `SPEC.md`, `templates/system.md`, `docs/vibe-spec.md` |
| `gap-filler.md` | infer, assume, escalate, conflict scan | `SPEC.md`, `.agents/skills/spec-gap-fill/` |
| `spec-validator.md` | independent gate; sets `status: validated` | `SPEC.md`, `checklists/validate.md` |
| `architect.md` | validated spec -> fleet-ready plan | `SPEC.md`, `templates/plan.md`, `checklists/plan.md` |
| `implementer.md` | implement a planned track | `SPEC.md`, `plans/<id>.md`, `.context/<id>.md` |
| `verifier.md` | conformance tests written from the spec | `SPEC.md`, the target spec, the test strategy |
| `spec-reviewer.md` | contract-stage consistency and impact | `SPEC.md`, `checklists/review.md` |

## Handoff

```text
orchestrator -> writer -> gap-filler -> validator -> architect
                                                        |
                                                        v
                                      implementer + verifier (fleet)
                                                        |
                                     contract stage -> spec-reviewer
```

- **orchestrator** is the default entry: it delegates one spec sequentially, then
  plans before implementing.
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
- **spec-reviewer** is contract-stage only: cross-service consistency, impact, and
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
