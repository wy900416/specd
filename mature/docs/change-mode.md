# Evolution mode: changing a mature project

POC is the **bootstrap** phase. The long-term mode is **evolution**: a project has
an approved baseline, other people depend on it, and every change is a proposal
with impact, compatibility, and a release.

This is the default when the project is mature. It is not an optional appendix to
the POC flow. Full end-to-end diagram: [`../../docs/workflow.md`](../../docs/workflow.md).

## When a project is mature

- Its specs are `stage: mature`, `status: approved`, and versioned.
- Consumers depend on its contracts, services, or flows.
- The code and tests exist; the question is how to change them safely.
- A wrong change has a cost beyond the POC.

## Bootstrap vs evolution

| | Bootstrap | Evolution |
|---|---|---|
| Stage | `stage: poc` | `stage: mature` |
| Status | `draft`, `validated` | `approved`, `deprecated` |
| Version | `0.1.0`, no bumps | semver; only a release changes it |
| Gate | agent validation | agent validation + tiered human approval |
| Edit | edit the draft, re-validate | change request + proposal + release |
| Reference | `id#REQ-ID` | `id@version#REQ-ID` |
| Code | build from the validated spec | change from the approved baseline |

## The evolution loop

```text
CHG-...          change request: target, base_version, bump, risk, motivation
  → impact       consumers, contracts, tests, docs, data, ops
  → proposal     full target body + spec overrides, between markers
  → review       agent validation + spec-reviewer + tiered human approvals
  → release      apply, bump version, approve, archive
  → implement    small change direct; large change plan + fleet
  → verify       regression + conformance + contract compatibility
  → rollout      flag / canary / migration / deprecation / rollback
```

## Baseline

An approved spec is a **baseline**. A change target must be approved; if it is
`draft` or `validated`, it is still bootstrap and is edited directly.

Promotion from bootstrap:

1. Confirm every high-risk assumption and every agent decision with the user.
2. Resolve conflicts and open questions.
3. Set `stage: mature`, `status: approved`, `approved_by`, `approved_at`,
   `version: 1.0.0`; clear `validated_by`, `validated_at`, and `validated_sha`,
   and remove the validation block.
4. Add the links the kind requires.
5. Compute `approved_sha` from the resulting file and write it.
6. Record the promotion in the change log. From now on, use this mode.

## Change request

A change request is `changes/CHG-<YYYYMMDD>-<nnn>-<target>.md`. Allocate the
next `nnn` by scanning `changes/`, and keep one active proposed CHG per `target`
and `base_version`. Its front-matter:

```yaml
---
id: CHG-20261126-001-orders
kind: change
title: "Add idempotent order creation"
target: orders
base_version: 1.4.2
base_sha: "<target approved_sha>"
bump: minor
risk: medium
compatibility: additive
result_status: approved
status: proposed
author: "agent"
owner: "orders-team"
consumers: [checkout, admin]
# Canonical approvals array. Each entry: role, name, date, scope.
approvals: []
proposal_sha: "<hash of the proposed body>"
released_as: ""
released_at: ""
released_by: ""
release_commit: ""
created: 2026-11-26
updated: 2026-11-26
summary: "Make order creation idempotent."
spec: {}
---
```

The body is a **change record** followed by the proposed target body:

```md
## Motivation
## Impact
### Consumers
### Contracts
### Tests
### Docs
### Data
### Ops
## Test Strategy
## Compatibility
## Rollout
## Rollback
## Migration / deprecation
## Proposal validation
## Review
## Notes

<!-- BEGIN PROPOSED BODY -->
<the full proposed body of the target spec>
<!-- END PROPOSED BODY -->

## Verification
```

Release applies only the content between the markers. Impact, rollout, and the
recorded reviews stay in the record and are archived with it.

## Impact analysis

The `change-analyst` answers, with evidence:

- **Consumers:** which specs link to the target (`consumes`, `depends-on`,
  `exposes`, `relates-to`); which teams own them.
- **Contracts:** additive or breaking; unknown-field policy; version skew;
  deprecation window.
- **Tests:** conformance tests, contract tests, regression suite; which `REQ-` ids
  need new coverage.
- **Docs:** API docs, runbooks, onboarding, examples that name the old behaviour.
- **Data:** schema changes, migrations, backfill, retention.
- **Ops:** rollout mechanism, feature flag, monitoring, rollback, on-call.

An impact section without file paths or spec ids is a guess, not an analysis.

## Proposal

The proposal is a **full replacement body** of the target, not a diff. The diff is
derived by reading the target and the proposal side by side. `spec` holds
front-matter overrides (title, summary, owner, links, `applies_to`, `pinned`);
leave it `{}` when only the body changes.

The proposed body drops the validation block: an approved baseline does not carry
a current bootstrap validation.

`base_sha` is the target's `approved_sha` at proposal time; `proposal_sha` binds
the proposed body. The target's `## Acceptance` travels in the proposed body; the
change's `## Test Strategy` maps changed criteria to tests. The validator applies
[`checklists/validate-proposal.md`](../checklists/validate-proposal.md) to the
effective spec and writes `## Proposal validation` into the CHG. The
`spec-reviewer` writes `## Review`. Neither flips the approved target to
`status: validated`; release readiness is the change checklist plus the recorded
review.

## Tiered approval

The gate is [`checklists/change.md`](../checklists/change.md). Agent validation is
always required. Human approval depends on the change:

| Bump | Risk | Human approval | Extra |
|---|---|---|---|
| `patch` / `none` | low | owner | consumer notice optional |
| `minor` | low / medium | owner | affected consumers notified |
| `major` | any | owner + affected consumers | migration and rollback required |
| any | high (security, privacy, data ownership, payments) | owner + security/data owner | human always; no agent release |

Rules:

- The agent prepares the request, impact, proposal, and checklist. It never
  approves or releases.
- Approvals are recorded only in the front-matter `approvals` array; each entry
  has `role`, `name`, `date`, and `scope`. There is no separate body table.
- A `major` change without consumer sign-off is not ready to release.
- A high-risk change without the security/data owner is not ready to release.
- If the change is small and single-track, skip the architect plan and fleet; run
  the implementer and regression tests directly.

## Release

A human releases only after `## Proposal validation` records `Result: pass` and
`## Review` recommends `ready to release`.

A human releases:

1. Verify `base_version` equals the target's current `version`, and `base_sha`
   equals the target's `approved_sha`.
2. Verify `proposal_sha` matches the proposed body, then apply the body and the
   `spec` overrides.
3. Set the new `version` according to `bump`.
4. Set `status: result_status` (default `approved`), `approved_by`,
   `approved_at`, `updated`; clear `validated_by`, `validated_at`, and
   `validated_sha`, and remove the validation block.
5. Compute `approved_sha` and write it into the target.
6. Move the change to `changes/archive/` with `status: released`,
   `released_as`, `released_at`, `released_by`, and `release_commit`; preserve the
   reviews and approvals.
7. Update the index and any graph view.

An agent may prepare steps 1-2 and present the diff. It must not execute the
approval, `approved_sha`, archive, or index steps.

The release commit or PR is the external evidence that a human approved. The
Markdown record cannot prove identity; it records the human and the commit.

## Implementation

| Change size | Path |
|---|---|
| One file / one track | implementer + regression tests |
| Several disjoint tracks | architect plan + fleet + conformance tests |
| Data or contract migration | migration plan + rollout + rollback |

The plan is optional for small changes. Do not add a fleet to a one-file fix.

## Verification

- **Regression:** the existing suite still passes.
- **Conformance:** the changed and new `REQ-` ids have tests from the spec.
- **Acceptance:** the changed and new `## Acceptance` criteria have user-facing
  tests; the human accepts the outcome at rollout.
- **Contract compatibility:** consumers still pass their contract tests.
- **Rollout:** the flag/canary path is exercised; the rollback is tested.

## Retirement and split

- **Deprecate:** a `CHG` with `result_status: deprecated`, a proposed body that sets
  `status: deprecated`, `superseded-by` where a replacement exists, and the normal
  approvals. The release keeps the spec readable and updates incoming links.
- **Split:** create and approve the new spec(s) through the manual-baseline path,
  then a `CHG` on the old target with `result_status: deprecated` and the outgoing
  links. A split is a sequence of changes, not one multi-target record.

## Rollout and deprecation

- Roll out behind a flag or canary when the change is user-visible or stateful.
- State the rollback trigger and who can pull it.
- For a breaking contract, state the deprecation window and the consumer
  migration path.
- Archive the change with the released version; keep the record.

## Adoption

A mature project usually starts without specs. Backfill a baseline from the
existing code, contracts, and tests; then every change uses this mode. See
[`adoption.md`](adoption.md).

## Anti-patterns

- Editing an approved spec directly.
- A `major` bump with no consumer sign-off or migration.
- Bumping `version` on every edit instead of on release.
- An impact section that lists only the target file.
- A proposal that includes unrelated edits.
- An agent approving or releasing its own change.
- Running a fleet on a one-file change.
