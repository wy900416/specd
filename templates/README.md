# Templates

The seed starts with **one kind**: `system`.

| Template | Use |
|---|---|
| `system.md` | The bootstrap default. One per product; describes the boundary, actors, and requirements. Also the manual baseline template for a mature project. |
| `spike.md` | Timeboxed demo log: hypothesis, demo contract, feedback, decision. |
| `plan.md` | Implementation plan from the architect: architecture, file map, tracks, test strategy. |
| `service.md` | Mature stage. A deployable unit that owns one domain and at least one contract. |
| `contract.md` | Mature stage. A wire interface plus its compatibility policy. |
| `flow.md` | Mature stage. Behaviour that crosses two or more services. |
| `domain.md` | Mature stage. A bounded context. |
| `standard.md` | A cross-cutting rule. `pinned: true` only when every matching context must receive it. |
| `nfr.md` | A measurable constraint. |
| `adr.md` | A decision and its alternatives. |
| `change.md` | A mature change: impact, compatibility, rollout, rollback, approvals, and the proposed body. |

`system.md` carries the v2 sections (`## Source`, `## Repo Profile`,
`## Assumptions`, `## Conflicts`, `## Validation`). The older templates are
mature-stage skeletons; when you use one, add those sections and set
`stage: mature` before promoting it.

See `SPEC.md` for the required sections, `docs/adoption.md` for the baseline, and
`docs/change-mode.md` for promotion and release.
