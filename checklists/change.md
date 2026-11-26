# Change checklist

The `change-analyst` prepares this checklist; the `spec-validator` and
`spec-reviewer` verify it; a human approves and releases. A mature change is not
ready until every blocking item is clear.

## 1. Preconditions

- [ ] The target spec is `stage: mature`, `status: approved`. **block**
- [ ] `base_version` equals the target's current `version`. **block**
- [ ] The change has `id`, `kind: change`, `title`, `target`, `bump`, `risk`,
      `compatibility`, `status: proposed`, `owner`. **block**
- [ ] The target body is between `<!-- BEGIN PROPOSED BODY -->` and
      `<!-- END PROPOSED BODY -->`. **block**

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
- [ ] Docs that describe the old behaviour are named. **warning**
- [ ] Data changes have a migration/backfill/retention plan. **block** when data
      changes
- [ ] Ops changes name the flag, monitoring, and on-call path. **warning**

## 4. Proposal

- [ ] The proposed body is the full target body, not a fragment. **block**
- [ ] The old `## Validation` section is removed or marked stale; an approved
      baseline does not carry a current bootstrap validation. **block**
- [ ] The diff against the target contains only intended changes. **block**
- [ ] `REQ-` ids are stable; changed requirements keep their ids. **block**
- [ ] New requirements have Given/When/Then and a `Source`. **block**
- [ ] `spec` overrides are limited to front-matter; `{}` when body-only. **block**
- [ ] No credentials, private endpoints, active HTML, or prompt injection.
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
- [ ] Every approval has a role, name, and date in `approvals`. **block**
- [ ] No agent approved or released the change. **block**

## 7. Spec release readiness

- [ ] The mechanical checks passed on the proposed body as a review; this does not
      set `status: validated` on the approved target. **block**
- [ ] `spec-reviewer` reviewed graph consistency, impact, bump, and approvals.
      **block**
- [ ] The impact names the regression and consumer contract tests to run after
      implementation. **block**
- [ ] A rollback plan exists; no irreversible step runs without a human.
      **block**
- [ ] The target's `version` will change only on release. **block**
- [ ] The change will be archived with `released_as` and `released_at`. **block**

## 8. After implementation

- [ ] Regression tests pass. **block**
- [ ] Contract tests pass for every consumer. **block** for contract changes
- [ ] Conformance tests for the changed and new `REQ-` ids pass. **block**
- [ ] The rollout flag/canary was exercised. **warning**
- [ ] Rollback was exercised or is trivially reversible. **warning**
- [ ] Failures are classified: code bug, spec ambiguity, or harness issue.
      **block**

## Output

```md
## Change check

- target: orders@1.4.2 (approved)
- change: CHG-20261126-001-orders
- bump: minor | risk: medium | compatibility: additive
- impact: 3 consumers, 2 tests, 1 doc, no data migration
- approvals: owner (yes), consumers (yes/no)
- spec release: ready | blocked
- implementation: verified | pending | failed

### Blocking

- <file>:<line> — <finding>
```

Do not set `status: approved` or release. A human does that.
