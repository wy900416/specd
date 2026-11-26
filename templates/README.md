# Templates

The seed starts with **one kind**: `system`.

| Template | Use |
|---|---|
| `system.md` | The POC default. One per product; describes the boundary, actors, and requirements. |
| `spike.md` | Timeboxed demo log: hypothesis, demo contract, feedback, decision. |
| `plan.md` | Implementation plan from the architect: architecture, file map, tracks, test strategy. |
| `service.md` | Contract stage. A deployable unit that owns one domain and at least one contract. |
| `contract.md` | Contract stage. A wire interface plus its compatibility policy. |
| `flow.md` | Contract stage. Behaviour that crosses two or more services. |
| `domain.md` | Contract stage. A bounded context. |
| `standard.md` | A cross-cutting rule. `pinned: true` only when every matching context must receive it. |
| `nfr.md` | A measurable constraint. |
| `adr.md` | A decision and its alternatives. |
| `change.md` | A contract-stage change proposal. |

`system.md` carries the v2 sections (`## Source`, `## Repo Profile`,
`## Assumptions`, `## Conflicts`, `## Validation`). The older templates are
contract-stage skeletons; when you use one, add those sections and set
`stage: contract` before promoting it.

See `SPEC.md` for the required sections and `docs/contract-mode.md` for the
promotion path.
