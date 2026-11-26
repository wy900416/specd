# Adopting a mature project

A mature project usually has code, contracts, tests, and docs — but no spec
baseline. Bootstrap a baseline first, then every change goes through
[`change-mode.md`](change-mode.md).

There are two paths. They can be combined.

## Path A: guided backfill (`/backfill`)

Use it when the behaviour is discoverable from the repository.

1. Pick **one boundary**: a service, a contract, or a flow with a high change
   frequency or a high blast radius. Do not start with the whole system.
2. Run `/backfill <boundary>`. The `backfiller` agent reads the code, contracts,
   tests, and docs, and writes a draft spec describing **current behaviour**, not
   desired behaviour. `## Source` records your backfill request; every requirement
   cites repository evidence.
3. It marks every inferred requirement with evidence (`repo:<path>:<line>`) and
   every uncertainty in `## Assumptions`.
4. Run `/validate-spec`. Fix mechanical findings.
5. A human reviews and approves the baseline: `stage: mature`, `status: approved`,
   `version: 1.0.0`; clear the `validated_*` fields.
6. Repeat for the next boundary, highest churn first.

The backfiller never approves. A backfilled spec is a hypothesis about the
current system; a human makes it the baseline.

## Path B: manual baseline

Use it when the boundary is new, poorly instrumented, or the code is not the best
source of truth.

1. Write the spec with the `spec-writer` agent, using the normal template.
2. Set `stage: mature`, `status: draft`, `version: 0.1.0`.
3. Fill `## Source`, `## Repo Profile`, requirements, assumptions, and decisions.
4. Validate it.
5. A human approves: `status: approved`, `approved_by`, `approved_at`,
   `version: 1.0.0`; clear the `validated_*` fields.
6. Treat it as the baseline; changes go through `changes/`.

Manual is slower but better when the team knows the intended behaviour and the
code is not a reliable description of it.

## What to backfill first

| Priority | Why |
|---|---|
| High change frequency | The spec pays for itself immediately |
| High blast radius | Impact analysis matters most |
| External contract | Consumers need a stable reference |
| Shared data ownership | Ambiguity is expensive |
| Recently broken area | The spec can capture the postmortem |

Do not backfill everything. A baseline that is never read is documentation, not a
spec.

## After the baseline

1. Every change is a `CHG` with impact, compatibility, and approvals.
2. The spec graph grows as boundaries become real.
3. Add an index when the graph crosses the trigger in [`index.md`](index.md).
4. Keep `examples/` separate from `specs/`.

## Anti-patterns

- Backfilling a whole system before any change.
- Marking a backfilled spec `approved` without a human review.
- Describing the desired system instead of the current one.
- Backfilling without evidence; every requirement needs a source.
- Skipping the baseline and calling direct edits "changes".
