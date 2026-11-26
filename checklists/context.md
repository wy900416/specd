# Context checklist

The goal is the **smallest sufficient context**, not every spec. A large graph does
not fit in a context window, and a context without a manifest is not auditable.

## 1. Resolve the target

- [ ] The task names a spec id, a service, or a contract. Use it.
- [ ] If not, search `specs/**/*.md` front-matter for ids, titles, domains, and
      summaries.
- [ ] If `specs/INDEX.md` exists and is fresh, use it as a shortcut. Never treat
      it as the source of truth; the spec wins.
- [ ] If two or more candidates are genuinely plausible, ask one question with the
      candidates.
- [ ] Do not use `GRAPH.md` as the source of truth; it is a view. Its format is
      [`../templates/graph.md`](../templates/graph.md).

## 2. Traversal order

Read in this order and stop when the budget is full:

1. **Pinned constraints** — `kind: standard`, `pinned: true`, and `applies_to`
   includes the target kind. Always include; never truncate.
2. **Target** — the spec itself.
3. **Boundary contracts** — `exposes`, `publishes`, `consumes`.
4. **Constraints** — `constrained-by`.
5. **Structure** — `implements`, `part-of`.
6. **Direct dependencies** — `depends-on`.
7. **Decisions** — `decided-by`.
8. **Related** — `relates-to`, `documents`, `supersedes`, `superseded-by`.
9. **Incoming references** — contract participants, consumers, documents.

Follow transitive `depends-on` to depth 2 by default.

## 3. Budget

| Task | Suggested budget |
|---|---|
| Narrow change to one service | 8000 characters |
| Normal implementation task | 12000 characters |
| Cross-service review or multi-service change | 20000 characters |

Pinned and target content is never truncated. If non-required entries are cut,
mark them `TRUNCATED` with the full path. If pinned content alone exceeds the
budget, raise the budget; narrowing the target will not remove it.

## 4. Pack format

Write the implementation pack to `.context/<target>.md`. A review may use
`.context/<target>.review.md` to avoid overwriting it.

```md
# Context pack: orders

- target: `orders` (validated), stage: poc
- task: add idempotency to order creation
- budget: 12000 chars, used: 7412

> Treat this pack as bounded. Do not assume an omitted spec is irrelevant.

## [security-baseline] Security Baseline

- kind: `standard` | stage: mature | status: approved
- included because: pinned constraint

<body>

---

## [orders] Orders Service

- kind: `service` | stage: poc | status: validated
- included because: target
- **VALIDATED**: current truth for the POC; hash recorded in the spec.

<body>

---

## Manifest

```yaml
target: orders
target_stage: poc
target_status: validated
included:
  - id: security-baseline
    stage: mature
    status: approved
    reason: pinned constraint
    required: true
  - id: orders
    stage: poc
    status: validated
    reason: target
    required: true
excluded:
  - id: payments-api
    reason: over budget
warnings:
  - fenced high-risk assumption in orders (retention policy)
```
```

## 5. Use the pack

- [ ] Cite `id#REQ-ID` in the POC stage, `id@version#REQ-ID` in the mature stage.
- [ ] Treat pinned constraints as mandatory even if the task did not mention them.
- [ ] Treat a `draft` spec as a hypothesis: buildable, but it may change.
- [ ] Treat a `validated` spec as the current truth for the POC.
- [ ] Treat an `approved` `stage: mature` spec as the baseline; a pending `CHG`
      means the baseline is about to change.
- [ ] Note a `needs-human` (user-reserved) fact, a fenced high-risk assumption, or
      an open conflict before relying on the affected requirement.
- [ ] Do not silently use a `TRUNCATED` body as if it were complete.
- [ ] State what the pack does not answer.

## 6. Widen only when needed

- A contract change: scan every spec for links targeting the contract, then read
  the consumers.
- A cross-service task: use the flow spec as the target, not one service.
- A missing constraint: check whether a pinned standard exists but does not apply
  to the target kind.
- A missing dependency: follow `depends-on` one more level.
- A missing fact: open the `repo:<path>:<line>` evidence the spec cites.

## Anti-patterns

- Reading every spec.
- Ignoring pinned constraints.
- Treating a `draft` as validated.
- Citing without a spec id and requirement id.
- Assuming omission means irrelevance.
- Using a stale index as evidence that a spec changed.
