---
name: spec-context
description: "Build a bounded, auditable context pack from the spec graph for a task. Use before implementing, reviewing, or designing against existing specs."
whenToUse: "The task touches an existing spec or service and you need the right subset of the spec graph, not every spec."
---

# Spec context

The goal is the **smallest sufficient context**, not all specs. A large graph does
not fit in a context window, and a context without a manifest is not auditable.

## Procedure

1. **Resolve the target.** If the spec id is not given, run `./specd.sh index` and
   search ids, titles, and domains. Ask only when two or more candidates are
   genuinely plausible.
2. **Build the pack.**
   ```bash
   ./specd.sh context <id> --task "<one sentence>" --budget 12000 \
     --out .specd/context/<id>.md
   ```
   Use `--budget 8000` for a narrow change, `12000` for normal work, and `20000`
   for architecture review. Required and pinned content is never truncated.
3. **Read the pack.** The manifest at the bottom is authoritative. Record the
   target `id@version` and `status`.
4. **Check the warnings.** A pending proposal means the graph is about to change.
   An unapproved spec is not truth. `TRUNCATED` means the body you see is partial;
   read the full file only if the task needs it.
5. **Widen only when needed.**
   - `./specd.sh impact <id>` for dependents and consumers.
   - `./specd.sh context <dependency> ...` for a deeper slice.
   - Read a named spec file only when the pack says it was omitted and the task
     genuinely needs it. Never assume omission means irrelevance.
6. **Cite.** Every claim about the spec cites `spec-id@version#REQ-ID`.

## Rules

- Never edit a spec from this skill.
- Treat pinned constraints as mandatory, even if the task did not mention them.
- Do not silently use an unapproved spec as if it were approved.
- If non-required entries are truncated, narrow the target instead of raising the
  budget. If the warning says pinned/required content alone exceeds the budget,
  raise the budget: those entries are mandatory and will never be truncated.
- For architecture work, pair the pack with `./specd.sh fitness` and
  `./specd.sh impact <contract>`.
- For implementation work, pair the pack with the code and tests; do not read
  every spec in the repository.

## Output contract

Return a short **context manifest summary**, not the whole pack:

```md
## Context
- target: orders@0.1.0 (draft)
- included: security-baseline@1.0.0 (pinned), orders, orders-api, commerce, payments
- excluded: <ids and why>
- warnings: <pending proposal / truncation / unapproved>
- requirements in scope: REQ-ORD-001, REQ-ORD-002
- gaps: <what the pack does not answer>
```

Then answer the task. If a gap blocks the task, say so and name the spec or
question that must be resolved. Details and budget guidance are in
`references/context-rules.md`.
