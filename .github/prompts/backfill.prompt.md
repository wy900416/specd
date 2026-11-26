---
mode: 'agent'
description: 'Backfill a draft baseline for one existing boundary: current behaviour, evidence, assumptions, validation.'
---

Backfill a baseline for this boundary:

${input:boundary}

Follow `agents/backfiller.md`, `docs/adoption.md`, and `checklists/validate.md`.

1. Confirm one boundary: a service, a contract, or a flow.
2. Read the code, contracts, tests, config, docs, and recent changes.
3. Write `specs/<kind>/<id>.md` describing **current behaviour**:
   - `stage: mature`, `status: draft`, `version: 0.1.0`;
   - `Source: repo:<path>:<line>` on every requirement;
   - gaps in `## Assumptions` with risk and revisit.
4. Run `/validate-spec`; fix mechanical findings.
5. Report the evidence, gaps, and the human approval needed for the `1.0.0`
   baseline.

Do not set `status: approved`, `approved_by`, or `approved_at`.
