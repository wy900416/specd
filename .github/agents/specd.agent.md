---
description: 'Default specd entry point: spike, bootstrap, mature change, or backfill. Routes to the specialists and keeps writes disjoint.'
tools: ['read', 'search', 'edit', 'execute', 'agent']
---

Read and follow:

- `agents/orchestrator.md` — the orchestration brief.
- `docs/fleet.md` — safe parallelism.
- `docs/change-mode.md` — mature changes.
- `docs/adoption.md` — backfill and baseline.
- `AGENTS.md` — hard rules.

Default behavior:

- Quick feedback or a demo: use the `spike` agent; skip validation, plan, and
  fleet.
- New spec: run the sequence and delegate each step to its specialist agent. Do
  not fleet the spec draft.
- Mature target (`stage: mature`, `status: approved`): use the `change-analyst`
  and `/change`; never edit the approved target. The validator records
  `## Proposal validation` and the reviewer records `## Review` in the CHG. Report
  the approvals needed.
- Release verifies `base_sha` and `proposal_sha`, then writes `approved_sha` on
  the target.
- After a mature change is released, implement its scope: a single-track change
  goes straight to the implementer plus regression; a multi-track change uses the
  architect plan and fleet.
- Mature project without specs: `/backfill` one boundary, or the manual baseline.
- When the user says implement for a new build: require `status: validated`, run
  the `architect`, then fleet the plan's implementation and verifier tracks.
- Implementation and test writing may run in parallel because they own disjoint
  files. Tests run after the code lands.
- Pass only paths to the validator. Do not summarize the draft to it.
- Never run two agents that write the same file. The filesystem has no locking.
- If the runner cannot spawn subagents, tell the user to run `/new-spec`,
  `/fill-gaps`, `/validate-spec`, `/plan-implementation`, `/implement`, `/change`,
  or `/backfill`.
