---
name: spec-context
description: "Build a bounded, auditable context pack from the spec graph for a task. Use before implementing, reviewing, or designing against existing specs."
whenToUse: "The task touches an existing spec or service and you need the right subset of the spec graph, not every spec."
---

# Spec context

The goal is the **smallest sufficient context**, not all specs. There is no
runtime: read the files, apply the traversal rules, and write a pack with a
manifest.

## Read first

- `SPEC.md` — the graph and link model.
- `checklists/context.md` — traversal order, budget, pack format, anti-patterns.

## Procedure

1. **Resolve the target.** If the spec id is given, use it. Otherwise search
   `specs/**/*.md` front-matter for ids, titles, domains, and summaries. Ask only
   when two or more candidates are genuinely plausible.
2. **Build the pack.** Follow `checklists/context.md` in order:
   pinned standards first, then the target, boundary contracts, constraints,
   structure, dependencies, decisions, related specs, and incoming references.
3. **Write it** to `.context/<target>.md` using the format in the checklist. Put
   the manifest at the bottom.
4. **Check the warnings.** A pending proposal means the graph is about to change.
   An unapproved spec is not truth. `TRUNCATED` means the body is partial.
5. **Widen only when needed.** Follow `depends-on` one more level, read a
   consumer, or read a named spec directly. Never assume omission means
   irrelevance.
6. **Cite.** Every claim about the spec cites `id@version#REQ-ID`.

## Rules

- Never edit a spec from this skill.
- Treat pinned constraints as mandatory even if the task did not mention them.
- Do not silently use an unapproved spec as if it were approved.
- If non-required entries are truncated, narrow the target. If pinned/required
  content alone exceeds the budget, raise the budget: it is never truncated.
- For cross-service review, pair the pack with `checklists/review.md` and a
  reverse link scan for impact.
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
question that must be resolved.
