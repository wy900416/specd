# Context checklist

The goal is the **smallest sufficient context**, not every spec. A large graph
does not fit in a context window, and a context without a manifest is not
auditable.

## 1. Resolve the target

- [ ] The task names a spec id, a service, or a contract. Use it.
- [ ] If not, search `specs/**/*.md` front-matter for ids, titles, domains, and
      summaries.
- [ ] If two or more candidates are genuinely plausible, ask one question with the
      candidates.
- [ ] Do not use `GRAPH.md` as the source of truth; it is a view.

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

Write the pack to `.context/<target>.md`:

```md
# Context pack: orders

- target: `orders` v0.1.0 (draft)
- task: add idempotency to order creation
- budget: 12000 chars, used: 7412

> Treat this pack as bounded. Do not assume an omitted spec is irrelevant.

## [security-baseline] Security Baseline

- kind: `standard` | version: `1.0.0` | status: `approved`
- included because: pinned constraint

<body>

---

## [orders] Orders Service

- kind: `service` | version: `0.1.0` | status: `draft`
- included because: target
- **PENDING**: not approved; treat as a proposal.

<body>

---

## Manifest

```yaml
target: orders
target_version: 0.1.0
target_status: draft
included:
  - id: security-baseline
    version: 1.0.0
    status: approved
    reason: pinned constraint
    required: true
  - id: orders
    version: 0.1.0
    status: draft
    reason: target
    required: true
excluded:
  - id: payments-api
    reason: over budget
warnings:
  - open proposal CHG-... exists for orders
```
```

## 5. Use the pack

- [ ] Cite `id@version#REQ-ID` in every claim.
- [ ] Treat pinned constraints as mandatory even if the task did not mention them.
- [ ] Treat an unapproved spec as a proposal, not truth.
- [ ] Note a pending proposal before relying on the current body.
- [ ] Do not silently use a `TRUNCATED` body as if it were complete.
- [ ] State what the pack does not answer.

## 6. Widen only when needed

- A contract change: scan every spec for links targeting the contract, then read
  the consumers.
- A cross-service task: use the flow spec as the target, not one service.
- A missing constraint: check whether a pinned standard exists but does not apply
  to the target kind.
- A missing dependency: follow `depends-on` one more level.

## Anti-patterns

- Reading every spec.
- Ignoring pinned constraints.
- Treating a draft as truth.
- Citing without a version.
- Assuming omission means irrelevance.
