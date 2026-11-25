# Contract mode

Contract mode is the optional second half of specd. A POC spec is a hypothesis; a
contract spec is something other people depend on. The switch is deliberate and
should be rare.

## When to promote

Promote a spec to `stage: contract` when any of these is true:

- another team depends on it;
- it deploys independently;
- an external consumer uses its contract;
- it handles real money, PII, or regulated data;
- a reversal would be expensive;
- the interface has survived two changes.

Do not promote because the POC "feels done". Promote because a dependency exists.

## What changes

| POC stage | Contract stage |
|---|---|
| `stage: poc` | `stage: contract` |
| `version: 0.1.0`, no bumps | semver; only a release changes it |
| `status: draft / validated` | `status: approved / deprecated` |
| Agent validation | Human approval + agent validation |
| Edit the draft, re-validate | Propose a change in `changes/`, human releases |
| `id#REQ-ID` | `id@version#REQ-ID` |

## Promotion

1. Keep the same `id` and `REQ-` ids.
2. Confirm every high-risk assumption and every agent decision with the user.
3. Set `stage: contract`, `status: approved`, `approved_by`, `approved_at`, and
   `version: 1.0.0`.
4. Add the links the kind requires (a service needs a domain and a contract, for
   example).
5. Archive the POC discussion in the spec's change log, not in a new spec.

## Changes

An approved contract spec is read-only for agents. A change is a full copy in
`changes/`:

```yaml
---
id: CHG-20261125-001-orders
kind: change
title: "Add idempotent order creation"
target: orders
base_version: 1.0.0
bump: minor
status: proposed
author: "agent"
created: 2026-11-25
summary: "Make order creation idempotent."
spec: {}
---
<the proposed body of the target>
```

`spec` holds front-matter overrides; leave it `{}` when only the body changes.

## Release

A human releases a proposal:

1. Verify `base_version` equals the target's current `version`.
2. Apply the body and the `spec` overrides.
3. Set `version` according to `bump`.
4. Set `status: approved`, `approved_by`, `approved_at`, `updated`.
5. Move the proposal to `changes/archive/` with `status: released` and
   `released_as: <version>`.

An agent may prepare steps 1-3 and present the diff. It must not execute steps 4-5.

## Validation and review

- `checklists/validate.md` still applies, plus the contract-specific kind rules.
- `checklists/review.md` adds cross-service consistency and the bump guide.
- `spec-reviewer` is the contract-stage reviewer; `spec-validator` remains the
  mechanical gate.

## Anti-patterns

- Promoting a spec with unresolved high-risk assumptions.
- Bumping `version` on every edit instead of on release.
- Editing an approved spec directly.
- Starting contract mode before an external dependency exists.
