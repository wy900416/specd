---
id: "CHG-YYYYMMDD-001-<target>"
kind: change
title: "Change to <target>"
target: "<target-id>"
base_version: "<current-version>"
base_sha: "<target approved_sha>"
bump: patch
risk: low
compatibility: backward
# approved | deprecated (use deprecated for a retirement)
result_status: approved
status: proposed
author: "<agent or human>"
owner: "<owner>"
consumers: []
# Canonical approvals array. Each entry: role, name, date, scope.
approvals: []
proposal_sha: "<hash of the proposed body>"
released_as: ""
released_at: ""
released_by: ""
release_commit: ""
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

## Test Strategy

| REQ | Test file | Level | Owner |
|---|---|---|---|
| `REQ-...` | `tests/...` | unit / integration / black-box | implementer or verifier |

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

## Proposal validation

<!-- The spec-validator writes this block after applying
     mature/checklists/validate-proposal.md. Keep it outside the proposed-body markers.
     It records base_sha, proposal_sha, Result, and one row per section. -->

## Review

<!-- The spec-reviewer writes the review packet here, including the
     recommendation: ready to release / revise / reject. -->

## Notes

<!-- Anything the reviewer needs that is not in the target body. -->

<!-- BEGIN PROPOSED BODY -->
<Copy the full body of the target spec here, then edit it. Remove the validation
block: an approved baseline does not carry a current bootstrap validation. Release
applies only this section. Put front-matter overrides in `spec:` above; leave it
`{}` when only the body changes.>
<!-- END PROPOSED BODY -->

## Verification

<!-- Post-release evidence: regression, conformance, and consumer contract tests.
     This section is not applied by release. -->
