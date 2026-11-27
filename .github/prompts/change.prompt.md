---
mode: 'agent'
description: 'Prepare a mature change: impact, compatibility, rollout, rollback, approvals, and a proposed target body.'
---

Prepare a mature change.

Target spec:

${input:target}

Requested change:

${input:change}

Follow `agents/change-analyst.md`, `mature/docs/change-mode.md`,
`mature/checklists/change.md`, and `mature/templates/change.md`.

1. Confirm the target is `stage: mature`, `status: approved`. Record its `version`
   as `base_version` and its `approved_sha` as `base_sha`. Refuse if another
   proposed CHG targets the same target and base version.
2. Search the graph for consumers and read contracts, tests, docs, data, and ops.
3. Propose `bump`, `risk`, and `compatibility` with evidence.
4. Write `changes/CHG-<YYYYMMDD>-<nnn>-<target>.md`:
   - motivation, impact, compatibility, rollout, rollback, migration;
   - the full proposed target body between the markers;
   - `proposal_sha` computed from that body;
   - `result_status: approved` (or `deprecated` for a retirement);
   - `status: proposed`, never approved.
5. List the approvals needed by tier: owner, consumers, security/data. Approvals
   live only in the front-matter `approvals` array.
6. Run sections 1-6 of `mature/checklists/change.md`; leave `## Proposal validation` and
   `## Review` for the validator and reviewer, and report blocking findings.

Do not approve, release, edit the target, or bump the version.
