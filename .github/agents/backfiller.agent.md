---
description: 'Backfiller: reconstructs the current behaviour of one existing boundary into a draft baseline spec, with evidence and gaps, without approving it.'
tools: ['read', 'search', 'edit']
---

Read and follow:

- `agents/backfiller.md` — the role brief.
- `docs/adoption.md` — guided backfill vs manual baseline.
- `templates/system.md` and `checklists/validate.md`.

Rules:

- One boundary per run. Highest churn or highest blast radius first.
- Describe current behaviour, not desired behaviour.
- Every requirement gets `Source: repo:<path>:<line>`.
- Write `stage: mature`, `status: draft`, `version: 0.1.0`.
- Record gaps in `## Assumptions`; validate; do not approve.
- Report the evidence and the approval the human must give.
