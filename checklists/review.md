# Review checklist

> **Mature stage only.** In the bootstrap stage the gate is
> [`spec-validate`](../.agents/skills/spec-validate/SKILL.md) and
> `checklists/validate.md`. Use this checklist when a baseline is being promoted,
> a mature change is being reviewed, or a proposal is about to be released.

Use this before releasing a change. Review the **graph and the consumers**, not
just the file: a spec can be well written and still break a consumer, miss a
pinned standard, or bump the wrong version.

## 1. Dimensions

| Dimension | Question | Blocking when |
|---|---|---|
| Intent | Is the problem, scope, and non-goal clear? | A reader cannot tell what decision the spec enables |
| Impact | Are all consumers, tests, docs, data, and ops named? | A consumer or migration is missing |
| Compatibility | Is the change backward, additive, or breaking? | A breaking change has no consumer impact or migration plan |
| Behaviour | Are the main path, failure path, and edge cases covered? | A normative requirement has no observable outcome |
| Contract | Are boundaries, errors, and compatibility stated? | A breaking change has no consumer impact or migration plan |
| Data | Is ownership and write authority explicit? | Two specs claim to own the same data |
| NFR | Are measurable constraints linked and testable? | A service has no applicable standard or NFR where one is required |
| Traceability | Does every requirement have a stable id and a verification path? | Requirements cannot be traced to a test, check, or review |
| Security | Are secrets, internal endpoints, and injection risks absent? | The security section of `checklists/validate.md` finds critical/high issues |
| Versioning | Does the bump match the semantic change? | A breaking change is labelled patch/minor |
| Approval | Does the tier match the bump and risk? | A major/high-risk change lacks the required sign-off |
| Rollout | Is there a flag/canary, rollback, and owner? | A stateful or user-visible change has no rollback |
| Consistency | Do linked specs agree? | Two specs contradict each other, or a consumer is missing |

## 2. Severity

- **Blocking** — cannot approve or release: contradiction, missing contract
  consumer, wrong bump for a breaking change, security finding, invented fact.
- **Non-blocking** — should fix before approval but does not change meaning:
  ambiguity, missing failure mode, unexplained warning, orphan spec.
- **Nit** — wording, formatting, ordering. Do not lead with nits.

## 3. Bump guide

| Change | Bump | Example |
|---|---|---|
| Typo, formatting, clarification that does not change behaviour | `none` or `patch` | Rewording a sentence |
| New optional field, new endpoint, additive behaviour | `minor` | Adding `metadata` to a response |
| Removing a field, changing a type, new required field, changed state machine | `major` | Renaming `order_id` to `id` |
| New spec, first release | `0.1.0` draft, then `1.0.0` on approval | A new service spec |

If the diff and the suggested bump disagree, report both and ask the human to
choose. Do not silently change the bump.

## 4. Consistency checks that lint cannot do

- [ ] Every direct consumer of the target is named with its owner.
- [ ] Contract tests exist or are updated for every consumer.
- [ ] The data migration is reversible, or the rollback is a restore.
- [ ] The rollout flag/canary has an owner and a first check.
- [ ] Two services do not claim ownership of the same entity.
- [ ] A flow references a service that actually exposes the contract it calls.
- [ ] A standard applies to a service that links it with `constrained-by`.
- [ ] A contract's compatibility policy matches its consumers' expectations.
- [ ] An NFR has a measurement, an owner, and a degradation response.
- [ ] A requirement is not duplicated in two specs under different ids.
- [ ] An approved spec has no open questions.
- [ ] A deprecated spec has a `superseded-by` target, and incoming links are
      updated.

## 5. Decision provenance

- [ ] Every agent decision is marked inline and listed in `## Agent Decisions`.
- [ ] Each is reversible, or the cost of reversal is stated.
- [ ] None covers security, privacy, compliance, data ownership, pricing, legal,
      or a breaking public contract without human sign-off.
- [ ] Each has a revisit trigger; a POC decision without one is a hidden
      requirement.
- [ ] The human accepting the draft explicitly accepts or overrides the agent
      decisions.

## 6. Review packet

```md
## Review
- target: <id>@<version> (<status>)
- change: <CHG id or "promotion">
- validation: <errors>, <warnings>
- blocking findings <n>
- non-blocking findings <n>
- impact: <direct consumers and affected versions>
- compatibility: backward | additive | breaking
- risk: low | medium | high
- approvals: owner / consumers / security-data
- rollout: direct | flag | canary; rollback: <yes/no>
- recommended bump: none | patch | minor | major
- agent decisions: <count, high-risk ones, accepted or overridden>
- open questions: <list>
- recommendation: ready to release | revise | reject

### Blocking
- <file>:<line> — <finding>

### Non-blocking
- <file>:<line> — <finding>
```

Every finding cites a file and line or `id@version#REQ-ID`. Do not restate the
whole spec.

## 7. What a passing checklist does not prove

- That the requirement is the right requirement.
- That the behaviour is testable in the real system.
- That the contract is implementable with the current stack.
- That the owner has capacity to maintain it.

Say these out loud in the review packet instead of implying the checklist is
approval.
