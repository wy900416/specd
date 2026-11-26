---
name: spec-context
description: "Build a bounded, auditable context pack from the spec graph for a task. Use before implementing, reviewing, or designing against existing specs."
whenToUse: "The task touches an existing spec and you need the right subset of the graph, not every spec."
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
   `specs/**/*.md` front-matter for ids, titles, domains, and summaries. If
   `specs/INDEX.md` exists and is fresh, use it as a shortcut; never treat it as
   the source of truth. Ask only when two or more candidates are genuinely
   plausible.
2. **Build the pack.** Follow `checklists/context.md` in order: pinned standards
   first, then the target, boundary contracts, constraints, structure,
   dependencies, decisions, related specs, and incoming references.
3. **Write it** to `.context/<target>.md` using the format in the checklist. Put
   the manifest at the bottom.
4. **Check the warnings.** A `draft` spec is a hypothesis: buildable, but it may
   change. A `validated` spec is the current truth for the POC. An `approved`
   `stage: mature` spec is the baseline; a pending `CHG` means it is about to
   change. A fenced high-risk assumption is a warning; an unresolved conflict or a
   user-reserved (`needs-human`) fact means the spec is not ready to rely on.
   `TRUNCATED` means the body is partial.
5. **Widen only when needed.** Follow `depends-on` one more level, read a
   consumer, or read a named spec directly. Never assume omission means
   irrelevance.
6. **Cite.** Every claim cites `id@version#REQ-ID` in the mature stage, or
   `id#REQ-ID` in the POC stage.

## Rules

- Never edit a spec from this skill.
- Treat pinned constraints as mandatory even if the task did not mention them.
- Do not silently use a `draft` spec as if it were validated.
- If non-required entries are truncated, narrow the target. If pinned/required
  content alone exceeds the budget, raise the budget: it is never truncated.
- For a mature-stage review, pair the pack with `checklists/review.md` and a
  reverse link scan for impact.
- For implementation work, pair the pack with the code and tests; do not read
  every spec in the repository.

## Output contract

Return a short **context manifest summary**, not the whole pack:

```md
## Context
- target: orders@0.1.0 (validated), stage: poc
- included: security-baseline (pinned), orders, orders-api, commerce
- excluded: <ids and why>
- warnings: <draft / open conflict / high-risk / truncation>
- requirements in scope: REQ-ORD-001, REQ-ORD-002
- gaps: <what the pack does not answer>
```

Then answer the task. If a gap blocks the task, say so and name the spec or
question that must be resolved.
