# Mature lane

This pack is for an **approved baseline** (`stage: mature`, `status: approved`):
change requests, impact, proposal review, release, rollout, and backfill.

**Do not read it for a new POC build.** The core path is in
[`AGENTS.md`](../AGENTS.md); the mature lane is opt-in.

## Contents

| Path | Use |
|---|---|
| [`docs/change-mode.md`](docs/change-mode.md) | Evolution loop, impact, approval tiers, release, retirement, split |
| [`docs/adoption.md`](docs/adoption.md) | Backfill one boundary or write a manual baseline |
| [`checklists/change.md`](checklists/change.md) | The change release gate |
| [`checklists/validate-proposal.md`](checklists/validate-proposal.md) | Mechanical review of the effective spec |
| [`checklists/review.md`](checklists/review.md) | Graph, consumer, and version review |
| [`templates/change.md`](templates/change.md) | Change record and proposed body |
| [`templates/service.md`](templates/service.md), [`contract.md`](templates/contract.md), [`flow.md`](templates/flow.md), [`domain.md`](templates/domain.md), [`standard.md`](templates/standard.md), [`nfr.md`](templates/nfr.md), [`adr.md`](templates/adr.md) | Mature-stage kind templates |
| [`templates/graph.md`](templates/graph.md) | The derived graph view |

The mature role briefs are still in `agents/` (`change-analyst`, `backfiller`,
`spec-reviewer`), and their Copilot wrappers are in `.github/agents/`. They are
mature-only; the core path does not need them.

## Install nothing

The pack is files, not a runtime. Read only the files the task triggers. A POC
never needs this directory.
