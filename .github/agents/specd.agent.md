---
description: 'Default specd entry point. Turns a description into a validated spec, then plans before implementation. Uses fleet for implementation and test generation when the plan has disjoint tracks.'
tools: ['read', 'search', 'edit', 'agent']
---

Read and follow:

- `agents/orchestrator.md` — the orchestration brief.
- `docs/fleet.md` — safe parallelism.
- `AGENTS.md` — hard rules.

Default behavior:

- For one spec, run the sequence and delegate each step to its specialist agent.
  Do not fleet the spec draft.
- When the user says implement: require `status: validated`, run the `architect`
  to produce `plans/<spec-id>.md` with `status: ready`, then fleet the plan's
  implementation tracks and verifier test tracks.
- Implementation and test writing may run in parallel because they own disjoint
  files. Tests run after the code lands.
- Pass only paths to the validator. Do not summarize the draft to it.
- Never run two agents that write the same file. The filesystem has no locking.
- If the runner cannot spawn subagents, tell the user to run `/new-spec`,
  `/fill-gaps`, `/validate-spec`, `/plan-implementation`, and `/implement` in
  order.
