# Repository layout

The seed is plain Markdown. There is no build step; every directory is something
you read, edit, or delete.

```text
AGENTS.md                 cross-tool agent entry point
SPEC.md                   format and lifecycle, normative
.github/
  copilot-instructions.md always-on rules
  instructions/           path-scoped rules (specs/**)
  agents/                 core orchestrator + role specialists; mature wrappers
  prompts/                core: spike, new-spec, fill-gaps, validate-spec,
                          check-conflicts, plan-implementation, implement,
                          build-index; mature: change, backfill
agents/                   role briefs (source of truth)
.agents/skills/           spec-draft, spec-gap-fill, spec-validate,
                          spec-context, spec-review, spike
checklists/               validate, context, plan, spike (core)
templates/                system, plan, spike (core)
docs/                     this manual
mature/                   opt-in: docs, checklists, and kind/change templates
specs/                    empty; your specs land here
spikes/                   timeboxed spike logs
plans/                    implementation plans from the architect
changes/                  mature-stage proposals only
changes/archive/          released proposals
```

## What goes where

| Path | Written by | Notes |
|---|---|---|
| `specs/system/<id>.md` | `spec-writer`, `gap-filler` | The bootstrap default; one per product |
| `specs/<kind>/<id>.md` | mature-stage work | `service`, `contract`, `flow`, `domain`, `standard`, `nfr`, `adr` |
| `plans/<spec-id>.md` | `architect` | Code starts only when the plan is `ready` and `spec_sha` matches |
| `.context/<id>.md` | `architect` | Bounded implementation pack; `.context/<id>.review.md` for review. Gitignored. |
| `spikes/<id>.md` | `spike` | Log on main; code on `spike/<id>` |
| `changes/CHG-*.md` | `change-analyst` | Only for `stage: mature`, `status: approved` targets |
| `mature/docs/` | maintainers | Opt-in mature lane: change mode and adoption |
| `mature/checklists/` | maintainers | Opt-in mature gates: change, review, validate-proposal |
| `mature/templates/` | maintainers | Opt-in kind and change templates |

## Adding specd to an existing repository

Copy `AGENTS.md`, `SPEC.md`, `.github/`, `agents/`, `.agents/skills/`,
`checklists/`, `templates/`, and `docs/` into your repository. Create `specs/`,
`plans/`, and `changes/archive/`. Copy `mature/` only if you need the mature
lane, and point `AGENTS.md` at it.

**Merge, do not overwrite.** Keep your existing `README`, `AGENTS.md`,
`.github/copilot-instructions.md`, CI, and test config; add the specd sections to
them.

Then follow [`adoption.md`](../mature/docs/adoption.md). Do not backfill the whole system; start
with the highest-churn or highest-blast-radius boundary.
