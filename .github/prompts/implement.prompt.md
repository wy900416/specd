---
mode: 'agent'
description: 'Implement a validated spec from a ready plan: dispatch implementation and test tracks, then run the conformance gate.'
---

Implement this spec:

${input:spec}

Preconditions:

1. The target is `status: validated`, or `status: approved` with a released
   `CHG`.
2. For a new build or multi-track change, `plans/<spec-id>.md` exists with
   `status: ready` and a `spec_sha` matching the target's `validated_sha` or
   `approved_sha`. If not, run `/plan-implementation` first.
3. For a single-track mature change, the released `CHG` is the scope; a plan is
   optional.

Follow `agents/orchestrator.md` and `docs/fleet.md`.

1. Run the plan's setup track first, if it has one: dependencies, shared config,
   schema, test config.
2. Dispatch the implementation tracks and the verifier test tracks in parallel.
   Each track owns disjoint files and receives its track row, the file scope, and
   the context pack.
3. Verifier tracks receive the spec, its `## Acceptance`, and the `## Test
   Strategy` table as text, not the architecture notes, file map, or plan file.
4. After all write tracks finish, run the verification command.
5. Classify failures: code bug, spec ambiguity, harness issue. Route code bugs to
   the implementer; spec questions to the writer; harness issues to the plan.
6. Set the plan to `done` only when every in-scope `REQ-` and every acceptance
   criterion has a passing test. Report conformance and acceptance separately.
7. Report tracks, test results, and any spec gap.

Never run two agents that write the same file. Implementation and tests may be
written in parallel; they are executed after both land.
