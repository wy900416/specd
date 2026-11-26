# Repository layout

The seed is plain Markdown. There is no build step in the specd flow; every
directory is something you read or edit, except `scripts/` which is an optional
self-check for maintainers.

```text
AGENTS.md                 cross-tool agent entry point
SPEC.md                   format and lifecycle, normative
.github/
  copilot-instructions.md always-on rules
  instructions/           path-scoped rules (specs/**)
  agents/                 specd orchestrator + role specialists
  prompts/                spike, new-spec, fill-gaps, validate-spec,
                          check-conflicts, plan-implementation, implement,
                          build-index, change, backfill
agents/                   role briefs (source of truth)
.agents/skills/           spec-draft, spec-gap-fill, spec-validate,
                          spec-context, spec-review, spike
checklists/               validate, validate-proposal, context, review, plan,
                          change, spike
templates/                system + plan + spike + change + graph + mature-stage kinds
docs/                     this manual
scripts/                  framework self-check (Node, no dependencies)
fixtures/                 framework conformance cases, not user specs
specs/                    empty; your specs land here
spikes/                   timeboxed spike logs
plans/                    implementation plans from the architect
examples/poc-url-shortener/ current POC example, outside validation
examples/legacy-v1/       frozen v1 reference graph
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
| `examples/poc-url-shortener/` | maintainers | Current POC example; never validated |
| `examples/legacy-v1/` | maintainers | Frozen v1 reference graph; not a template |
| `fixtures/` | maintainers | Conformance cases for the seed itself |
| `scripts/framework-check.mjs` | maintainers | Optional mechanical self-check; not part of the user flow |

## Adding specd to an existing repository

Copy `AGENTS.md`, `SPEC.md`, `.github/`, `agents/`, `.agents/skills/`,
`checklists/`, `templates/`, and `docs/` into your repository. Create `specs/`,
`plans/`, and `changes/archive/`.

**Merge, do not overwrite.** Keep your existing `README`, `AGENTS.md`,
`.github/copilot-instructions.md`, CI, and test config; add the specd sections to
them.

Do not copy `fixtures/` or `scripts/` unless you want the seed's own self-check;
they are for maintaining specd, not for the project's specs.

Then follow [`adoption.md`](adoption.md). Do not backfill the whole system; start
with the highest-churn or highest-blast-radius boundary.
