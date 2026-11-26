# Change proposals

> **Mature stage only.** A bootstrap spec (`stage: poc`) is a draft: edit it
> directly and re-validate. A proposal is for an `approved` baseline.

A mature change is a **change record plus a proposed target body**, stored in
`changes/`. The record explains why, who is affected, and how it rolls out; the
proposed body is the full replacement for the target.

## Create one

Use `/change` or the `change-analyst` agent. It:

1. reads the approved target and its consumers;
2. writes the impact, compatibility, rollout, and rollback sections;
3. copies the target body between the markers;
4. proposes `bump`, `risk`, and `compatibility`;
5. records the approvals needed.

## Format

`changes/CHG-<YYYYMMDD>-<nnn>-<target>.md`:

```yaml
---
id: CHG-20261126-001-orders
kind: change
title: "Add idempotent order creation"
target: orders
base_version: 1.4.2
bump: minor
risk: medium
compatibility: additive
status: proposed
author: "agent"
owner: "orders-team"
consumers: [checkout, admin]
approvals: []
created: 2026-11-26
updated: 2026-11-26
summary: "Make order creation idempotent."
spec: {}
---
```

The body has the change record, then:

```md
<!-- BEGIN PROPOSED BODY -->
<the full proposed body of the target spec>
<!-- END PROPOSED BODY -->
```

Release applies only the section between the markers.

## Review

- Apply [`checklists/change.md`](checklists/change.md).
- Compare the target and the proposed body side by side; the diff is derived.
- Confirm `base_version` equals the target's current `version`.
- Confirm `bump`, `risk`, and `compatibility` agree.
- Confirm the approval tier: owner, consumers for major, security/data for high
  risk.
- Confirm regression and contract tests are identified.

## Release

A human releases:

1. Verify `base_version`.
2. Apply the proposed body and the `spec` overrides.
3. Set the new `version` according to `bump`.
4. Set `status: approved`, `approved_by`, `approved_at`, `updated`; clear
   `validated_by`, `validated_at`, and `validated_sha`.
5. Move the change to `changes/archive/` with `status: released`,
   `released_as`, `released_at`.
6. Update the index and any graph view.

An agent may prepare 1-3 and present the diff. It must not execute 4-6.

## Naming

`CHG-<YYYYMMDD>-<nnn>-<target>.md`. The number is sequential within the day. Keep
the file name even after archiving; the id is the stable reference.
