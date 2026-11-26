---
mode: 'agent'
description: 'Run a 90-minute spike: one hypothesis, one demo path, fake data, then feedback and a kill/iterate/graduate decision.'
---

Run a spike for:

${input:description}

Follow `agents/spike.md`, `docs/spike.md`, `templates/spike.md`, and
`checklists/spike.md`.

1. Write the hypothesis and the signal in one sentence.
2. Write the five-line demo contract in `spikes/<id>.md` on the main branch, so
   the log survives the code.
3. Create a `spike/<id>` branch for the code.
4. Build one vertical slice with fake auth/data/payments and the simplest stack
   that runs. One agent. No polish.
5. Smoke test the one path.
6. At the timebox (90 minutes by default), stop and demo what exists.
7. Ask the three feedback questions and record the answers.
8. Decide: kill, iterate once, or graduate to the spec lane.

Do not write a full spec, run the validator, run the architect, or start a fleet.
