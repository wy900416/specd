---
mode: 'agent'
description: 'Prepare a mature change: impact, compatibility, rollout, rollback, approvals, and a proposed target body.'
---

Prepare a mature change.

Target spec:

${input:target}

Requested change:

${input:change}

Follow `agents/change-analyst.md`, `docs/change-mode.md`,
`checklists/change.md`, and `templates/change.md`.

1. Confirm the target is `stage: mature`, `status: approved`, and record its
   `version` as `base_version`.
2. Search the graph for consumers and read contracts, tests, docs, data, and ops.
3. Propose `bump`, `risk`, and `compatibility` with evidence.
4. Write `changes/CHG-<YYYYMMDD>-<nnn>-<target>.md`:
   - motivation, impact, compatibility, rollout, rollback, migration;
   - the full proposed target body between the markers;
   - `status: proposed`, never approved.
5. List the approvals needed by tier: owner, consumers, security/data.
6. Run `checklists/change.md`; report blocking findings.

Do not approve, release, edit the target, or bump the version.
