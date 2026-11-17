# Context rules

Companion to `spec-context/SKILL.md`. These are the rules `specd context` already
implements, plus the judgement the tool cannot make.

## What the pack includes

In priority order:

1. **Pinned constraints** — standards with `pinned: true` that apply to the target
   kind. Always included, never truncated.
2. **Target** — the spec itself.
3. **Boundary contracts** — `exposes`, `publishes`, `consumes`.
4. **Constraints** — `constrained-by`.
5. **Structure** — `implements`, `part-of`.
6. **Direct dependencies** — `depends-on`.
7. **Decisions** — `decided-by`.
8. **Related** — `relates-to`, `documents`, `supersedes`, `superseded-by`.
9. **Incoming references** — contract participants, consumers, and documents.

Transitive `depends-on` is followed up to `--depth` (default 2).

## Budget

| Task | Suggested budget |
|---|---|
| Narrow change to one service | 8000 |
| Normal implementation task | 12000 |
| Architecture review or multi-service change | 20000 |

Required and pinned content is never truncated. If non-required entries are cut,
the tool marks them `TRUNCATED`: narrow the target or query a dependency
separately. If the warning says pinned/required content alone exceeds the budget,
raise the budget instead — those entries are mandatory and narrowing will not
remove them.

## Reading the manifest

The manifest at the bottom is authoritative. Check:

- `target_version` and `target_status` — cite the exact version.
- `included` — the reason each spec was included.
- `excluded` — what was deliberately left out, and why.
- `warnings` — pending proposals, budget overflow, missing content.
- `truncated` — the body you see is partial.

An unapproved entry is marked `PENDING`. Treat it as a proposal, not truth. A
pending change proposal means the graph is about to change; say so before relying
on the current version.

## When to widen

- The task changes a contract: run `specd impact <contract-id>` and read the
  consumer specs.
- The task spans services: use the flow spec as the target, not one service.
- The task touches a cross-cutting rule: read the standard directly.
- The task fails because a constraint is missing: check whether a pinned standard
  exists but does not apply to the target kind.

## Anti-patterns

- **Reading every spec.** It burns context and hides the relevant constraint.
- **Ignoring pinned constraints.** They are mandatory even when the task did not
  mention security or compliance.
- **Treating a draft as truth.** Cite the status.
- **Citing without a version.** `orders#REQ-ORD-001` is ambiguous after a release;
  use `orders@0.1.0#REQ-ORD-001`.
- **Assuming omission means irrelevance.** The pack is bounded by design; say what
  you did not read.
