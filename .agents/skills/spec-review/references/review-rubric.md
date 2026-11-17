# Review rubric

Companion to `spec-review/SKILL.md`. Use it to make findings specific and to
separate blocking problems from style.

## Dimensions

| Dimension | Question | Blocking when |
|---|---|---|
| Intent | Is the problem, scope, and non-goal clear? | A reader cannot tell what decision the spec enables |
| Behaviour | Are the main path, failure path, and edge cases covered? | A normative requirement has no observable outcome |
| Contract | Are boundaries, errors, and compatibility stated? | A breaking change has no consumer impact or migration plan |
| Data | Is ownership and the write authority explicit? | Two specs claim to own the same data |
| NFR | Are measurable constraints linked and testable? | A service has no applicable standard or NFR where one is required |
| Traceability | Does every requirement have a stable id and a verification path? | Requirements cannot be traced to a test, check, or review |
| Security | Are secrets, internal endpoints, and injection risks absent? | `specd scan --strict` reports critical/high |
| Versioning | Does the bump match the semantic change? | A breaking change is labelled patch/minor |
| Consistency | Do linked specs agree? | Two specs contradict each other, or a consumer is missing |

## Severity

- **Blocking** — cannot approve or release: contradiction, missing contract
  consumer, wrong bump for a breaking change, security finding, invented fact.
- **Non-blocking** — should fix before approval but does not change meaning:
  ambiguity, missing failure mode, unexplained warning, orphan spec.
- **Nit** — wording, formatting, ordering. Do not lead with nits.

## Bump guide

| Change | Bump | Example |
|---|---|---|
| Typo, formatting, clarification that does not change behaviour | `none` or `patch` | Rewording a sentence |
| New optional field, new endpoint, additive behaviour | `minor` | Adding `metadata` to a response |
| Removing a field, changing a type, new required field, changed state machine | `major` | Renaming `order_id` to `id` |
| New spec, first release | `0.1.0` draft, then `1.0.0` on approval | A new service spec |

If the diff and the suggested bump disagree, report both and ask the human to
choose. Do not silently "fix" the bump.

## Consistency checks that lint cannot do

- Two services claim ownership of the same entity.
- A flow references a service that does not expose the contract it calls.
- A standard applies to a service that does not link it.
- A contract's compatibility policy contradicts its consumer's expectations.
- An NFR has no measurement, or a measurement with no owner.
- A requirement is duplicated in two specs under different ids.

## Review packet example

```md
## Review
- target: orders@0.1.0 (draft)
- gates: validate=pass, fitness=pass, scan=pass
- blocking findings 1
- non-blocking findings 2
- impact: orders-api consumers — none outside orders
- recommended bump: minor
- open questions: order id ownership
- recommendation: revise

### Blocking
- `flows/place-order.md`: payment timeout leaves the order `pending` but no
  reconciliation owner is named. Add an owner or a terminal state.

### Non-blocking
- `services/orders.md#REQ-ORD-001`: "exactly one order" is testable, but the
  idempotency key lifetime is unspecified.
- `contracts/orders-api.md`: error envelope is not shared with `payments-api`.
```
