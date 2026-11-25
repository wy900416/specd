---
mode: 'agent'
description: 'Implement a validated spec from a ready plan: dispatch implementation and test tracks, then run the conformance gate.'
---

Implement this spec:

${input:spec}

Preconditions:

1. The spec is `status: validated`.
2. `plans/<spec-id>.md` exists with `status: ready` and a matching `spec_sha`.
   If not, run `/plan-implementation` first.

Follow `agents/orchestrator.md` and `docs/fleet.md`.

1. Run the plan's setup track first, if it has one: dependencies, shared config,
   schema, test config.
2. Dispatch the implementation tracks and the verifier test tracks in parallel.
   Each track owns disjoint files and receives its track row, the file scope, and
   the context pack.
2. Verifier tracks receive the spec and `## Test Strategy`, not the architecture
   notes or the implementation plan.
3. After all write tracks finish, run the verification command.
4. Classify failures: code bug, spec ambiguity, harness issue. Route code bugs to
   the implementer; spec questions to the writer; harness issues to the plan.
5. Set the plan to `done` only when every in-scope `REQ-` has a passing test.
6. Report tracks, test results, and any spec gap.

Never run two agents that write the same file. Implementation and tests may be
written in parallel; they are executed after both land.
