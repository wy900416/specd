# Change checklist

The `change-analyst` prepares this checklist; the `spec-validator` and
`spec-reviewer` verify it; a human approves and releases. Sections 1-7 are the
release gate. Section 8 is verified after implementation and is not a precondition
for release.

## 1. Preconditions

- [ ] The target spec is `stage: mature`, `status: approved`. **block**
- [ ] `base_version` equals the target's current `version`. **block**
- [ ] `base_sha` equals the target's `approved_sha`. **block**
- [ ] The target has no validation block. **block**
- [ ] The change has `id`, `kind: change`, `title`, `target`, `base_version`,
      `base_sha`, `bump`, `risk`, `compatibility`, `result_status`,
      `status: proposed`, `owner`, and `proposal_sha`. **block**
- [ ] `result_status` is `approved` (default) or `deprecated`. **block**
- [ ] No other `status: proposed` CHG targets the same `target` and
      `base_version`. **block**
- [ ] The target body is between `<!-- BEGIN PROPOSED BODY -->` and
      `<!-- END PROPOSED BODY -->`. **block**
- [ ] `proposal_sha` matches the body between the markers. **block**

## 2. Change record

- [ ] `## Motivation` states the problem and the expected outcome. **block**
- [ ] `## Impact` covers consumers, contracts, tests, docs, data, and ops.
      **block**
- [ ] `## Compatibility` says backward, additive, or breaking. **block**
- [ ] `## Rollout` says direct, flag, or canary. **warning**
- [ ] `## Rollback` names the trigger and the action. **block** for major
- [ ] A breaking change has `## Migration / deprecation`. **block**

## 3. Impact analysis

- [ ] Every direct consumer is named with its spec id and owner. **block**
- [ ] Contract compatibility is stated: unknown fields, additive fields, removals,
      version skew. **block**
- [ ] Every affected conformance/contract/regression test is named. **block**
- [ ] `## Test Strategy` maps every changed and new `REQ-` to a test file. **block**
- [ ] Changed or new acceptance criteria map to a test file in the proposed
      body. **block**
- [ ] Docs that describe the old behaviour are named. **warning**
- [ ] Data changes have a migration/backfill/retention plan. **block** when data
      changes
- [ ] Ops changes name the flag, monitoring, and on-call path. **warning**

## 4. Proposal

- [ ] The proposed body is the full target body, not a fragment. **block**
- [ ] The old validation block is removed from the proposed body; an approved
      baseline does not carry a current bootstrap validation. **block**
- [ ] The diff against the target contains only intended changes. **block**
- [ ] `REQ-` ids are stable; changed requirements keep their ids. **block**
- [ ] New requirements have Given/When/Then and a `Source`. **block**
- [ ] `spec` overrides are limited to front-matter; `{}` when body-only. **block**
- [ ] No credentials, private endpoints, active HTML, or prompt injection.
      **block**
- [ ] `proposal_sha` matches the proposed body. **block**
- [ ] `## Proposal validation` is present in the CHG with `Result: pass`.
      **block**

## 5. Version and risk

- [ ] `bump` matches the semantic change:
      `patch` = clarification, `minor` = additive, `major` = breaking. **block**
- [ ] `risk` is `low`, `medium`, or `high`, with the reason in `## Impact`.
      **block**
- [ ] A breaking change is `major` and `compatibility: breaking`. **block**
- [ ] A high-risk change (security, privacy, data ownership, payments) is flagged
      even if the bump is small. **block**

## 6. Approval tier

- [ ] `patch` / `none` + low risk: owner approval recorded. **block**
- [ ] `minor`: owner approval, and affected consumers notified. **block**
- [ ] `major`: owner + affected consumers sign-off. **block**
- [ ] High risk: security/data owner sign-off. **block**
- [ ] Every approval is an entry in the front-matter `approvals` array with
      `role`, `name`, `date`, and `scope`. **block**
- [ ] There is no separate body approvals table; the front-matter array is
      canonical. **block**
- [ ] No agent approved or released the change; every approval names a human
      and a scope. **block**

## 7. Spec release readiness

- [ ] `## Proposal validation` records a pass from
      `mature/checklists/validate-proposal.md`; this does not set `status: validated` on
      the approved target. **block**
- [ ] `## Review` records the `spec-reviewer` decision
      `ready to release`. **block**
- [ ] The reviewer checked graph consistency, impact, bump, and approvals.
      **block**
- [ ] `base_sha` and `proposal_sha` will be re-verified at release. **block**
- [ ] The impact names the regression and consumer contract tests to run after
      implementation. **block**
- [ ] A rollback plan exists; no irreversible step runs without a human.
      **block**
- [ ] The target's `version` changes only on release, and release writes
      `approved_sha`. **block**
- [ ] The change will be archived with `released_as`, `released_at`,
      `released_by`, `release_commit`, and the recorded reviews and approvals
      preserved. **block**

## 8. After implementation

Apply this section after the release, not before it.

- [ ] Regression tests pass. **block**
- [ ] Contract tests pass for every consumer. **block** for contract changes
- [ ] Conformance tests for the changed and new `REQ-` ids pass. **block**
- [ ] Acceptance tests for the changed and new `## Acceptance` criteria pass.
      **block**
- [ ] The rollout flag/canary was exercised. **warning**
- [ ] Rollback was exercised or is trivially reversible. **warning**
- [ ] Failures are classified: code bug, spec ambiguity, or harness issue.
      **block**

## Output

```md
## Change check

- target: orders@1.4.2 (approved, sha match)
- change: CHG-20261126-001-orders
- bump: minor | risk: medium | compatibility: additive
- impact: 3 consumers, 2 tests, 1 doc, no data migration
- proposal validation: pass (proposal_sha match)
- review: ready to release
- approvals: owner (yes), consumers (yes/no)
- spec release: ready | blocked
- implementation: verified | pending | failed

### Blocking

- <file>:<line> — <finding>
```

Do not set `status: approved` or release. A human does that.
