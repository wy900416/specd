---
id: "CHG-YYYYMMDD-001-<target>"
kind: change
title: "Change to <target>"
target: "<target-id>"
base_version: "<current-version>"
bump: patch
risk: low
compatibility: backward
status: proposed
author: "<agent or human>"
owner: "<owner>"
consumers: []
approvals: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
summary: "<one line>"
spec: {}
---

# CHG-YYYYMMDD-001-<target>: <title>

## Motivation

What problem does this change solve, and what outcome proves it worked?

## Impact

### Consumers

- `<spec-id>` — <team, what it uses, what breaks>

### Contracts

- Compatibility: backward / additive / breaking
- Unknown fields:
- Version skew:
- Deprecation window:

### Tests

- Existing: <suite/path>
- New/changed `REQ-` coverage: <path>

### Docs

- <runbook, API doc, example>

### Data

- Migration/backfill:
- Retention:

### Ops

- Rollout:
- Monitoring:
- On-call:

## Compatibility

What changes for a consumer, and what does not? For a breaking change, name the
migration path.

## Rollout

Direct / feature flag / canary. Who enables it, and what is the first check?

## Rollback

Trigger:
Action:
Owner:

## Migration / deprecation

For breaking changes only: consumer migration steps and the deprecation window.

## Approvals

| Role | By | At | Scope |
|---|---|---|---|
| owner | | | |
| consumer | | | |
| security/data | | | |

## Notes

<!-- Anything the reviewer needs that is not in the target body. -->

<!-- BEGIN PROPOSED BODY -->
<Copy the full body of the target spec here, then edit it. Remove or mark stale
the old `## Validation` section: an approved baseline does not carry a current
bootstrap validation. Release applies only this section. Put front-matter
overrides in `spec:` above; leave it `{}` when only the body changes.>
<!-- END PROPOSED BODY -->
