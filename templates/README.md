# Templates

The seed starts with **one kind**: `system`. The core templates are here; the
mature-stage kinds and the change template are in [`../mature/templates/`](../mature/templates/).

## Core

| Template | Use |
|---|---|
| `system.md` | The bootstrap default. One per product; describes the boundary, actors, and requirements. Also the manual baseline template for a mature project. |
| `spike.md` | Timeboxed demo log: hypothesis, demo contract, feedback, decision. |
| `plan.md` | Implementation plan from the architect: architecture, file map, tracks, test strategy. |

## Mature only

Do not read these for a new POC. See [`../mature/README.md`](../mature/README.md).

| Template | Use |
|---|---|
| [`../mature/templates/service.md`](../mature/templates/service.md) | A deployable unit that owns one domain and at least one contract. |
| [`../mature/templates/contract.md`](../mature/templates/contract.md) | A wire interface plus its compatibility policy. |
| [`../mature/templates/flow.md`](../mature/templates/flow.md) | Behaviour that crosses two or more services. |
| [`../mature/templates/domain.md`](../mature/templates/domain.md) | A bounded context. |
| [`../mature/templates/standard.md`](../mature/templates/standard.md) | A cross-cutting rule. |
| [`../mature/templates/nfr.md`](../mature/templates/nfr.md) | A measurable constraint. |
| [`../mature/templates/adr.md`](../mature/templates/adr.md) | A decision and its alternatives. |
| [`../mature/templates/change.md`](../mature/templates/change.md) | A mature change: impact, test strategy, compatibility, rollout, rollback, proposal validation, review, and the proposed body. |
| [`../mature/templates/graph.md`](../mature/templates/graph.md) | A derived graph view; never the source of truth. |

Every spec template carries `## Source`, `## Repo Profile`, `## Context`,
`## Assumptions`, `## Agent Decisions`, `## Conflicts`, and the marker-delimited
`## Validation` block. Add `## Goals`, `## Non-goals`, and `## Actors` to a
`system` spec.

See `SPEC.md` for the required sections and `../mature/README.md` for the baseline
and promotion rules.
