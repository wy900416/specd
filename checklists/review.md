# Review checklist

> **Contract stage only.** In the POC stage the gate is
> [`spec-validate`](../.agents/skills/spec-validate/SKILL.md) and
> `checklists/validate.md`. Use this checklist when a spec is being promoted, a
> contract changes, or a proposal is about to be released.

Use this before approving a draft or releasing a proposal. Review the **graph**,
not just the file: a spec can be well written and still contradict a contract,
miss a pinned standard, or bump the wrong version.

## 1. Dimensions

| Dimension | Question | Blocking when |
|---|---|---|
| Intent | Is the problem, scope, and non-goal clear? | A reader cannot tell what decision the spec enables |
| Behaviour | Are the main path, failure path, and edge cases covered? | A normative requirement has no observable outcome |
| Contract | Are boundaries, errors, and compatibility stated? | A breaking change has no consumer impact or migration plan |
| Data | Is ownership and write authority explicit? | Two specs claim to own the same data |
| NFR | Are measurable constraints linked and testable? | A service has no applicable standard or NFR where one is required |
| Traceability | Does every requirement have a stable id and a verification path? | Requirements cannot be traced to a test, check, or review |
| Security | Are secrets, internal endpoints, and injection risks absent? | The security section of `checklists/validate.md` finds critical/high issues |
| Versioning | Does the bump match the semantic change? | A breaking change is labelled patch/minor |
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
- validation: <errors>, <warnings>
- blocking findings <n>
- non-blocking findings <n>
- impact: <direct consumers and affected versions>
- recommended bump: none | patch | minor | major
- agent decisions: <count, high-risk ones, accepted or overridden>
- open questions: <list>
- recommendation: approve | revise | reject

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
