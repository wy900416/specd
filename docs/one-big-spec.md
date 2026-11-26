# One big spec first, split later

> In the POC stage, a split is a normal edit: move the requirements, keep the ids,
> and re-validate. The proposal and version steps described below apply at
> mature stage.

This framework can represent a graph of small, service-level specs. It does **not**
require you to start there. For a POC, the better default is often one coarse spec
for the whole product.

## The claim

Start with **one big spec** when the product boundary is still a hypothesis and the
goal is to learn from users. Split it only when a boundary proves stable.

A big spec is not a 500-page document. It is one spec with clear sections, stable
requirement ids, and a short list of open questions. It is written so it *can* be
split, not so that it never will be.

## Why one big spec for a POC

1. **Boundaries are hypotheses.** At the start, you do not know where the seams
   are. Splitting now freezes a guess into a contract.
2. **One context, one review, one owner.** A single file fits in one agent context
   and one review pass. Ten small specs create ten places to be inconsistent.
3. **Splitting has coordination cost.** Every new spec needs links, ownership,
   versioning, and a consumer. That cost buys nothing until two teams or two
   deployables actually need it.
4. **Premature splits create a distributed monolith.** You get the cost of
   services (contracts, version skew, cross-service flows) without the benefit
   (independent ownership).
5. **User feedback is about the product, not the architecture.** The first round of
   feedback usually changes the flow, not the service boundary. A big spec is
   cheaper to change.
6. **You can still be precise.** Stable `REQ-` ids, Given/When/Then, and explicit
   non-goals work just as well in one file. Precision comes from the requirements,
   not from the file count.

## What "big" means

- One `system` spec that states the problem, the actors, the main flow, the
  non-goals, and the requirements.
- Optionally one `service` spec if there is a single deployable unit. A modular
  monolith is a valid POC shape. If you add one, it still needs the service edges:
  one domain, one contract, and its constraints. If those do not exist yet, keep
  the POC in the system spec.
- Sections with clear names (`## Order flow`, `## Payments`, `## Admin`) so a
  future split has natural cut lines.
- Stable requirement ids from day one. When you split, the ids move with the
  requirements; references do not break.
- A `## Agent Decisions` section if the POC uses agent defaults (see
  [`poc-mode.md`](poc-mode.md)).

## When to split

Split when at least one of these is true:

| Trigger | Why it is a real seam |
|---|---|
| Two teams need to change it independently | Ownership is the strongest boundary |
| It deploys independently | A deploy boundary is a contract boundary |
| An external consumer uses a contract | The contract now has a social obligation |
| A section changes at a different cadence | Release cadence is a boundary |
| The spec no longer fits a context or a review | The document has become unreadable |
| A boundary has survived two changes | It is evidence, not a guess |

Do **not** split because:

- the architecture diagram has boxes;
- the code has packages;
- "microservices" is the target;
- one file feels large.

## How to split without losing history

1. Pick a section with a stable boundary and an owner.
2. Create the new spec (`domain`, `service`, `contract`, or `flow`).
3. Move the requirements into it. **Keep the same `REQ-` ids.**
4. Add the links: `part-of`, `implements`, `exposes`, `depends-on`,
   `constrained-by`.
5. Leave a pointer in the big spec, or mark the moved section with
   `superseded-by` if the whole spec is replaced.
6. Version both specs. The big spec changes because its content moved; the new spec
   starts at `0.1.0`.
7. Update `GRAPH.md` and any `id@version#REQ` references.

A split is a change proposal, not a rewrite. Review it like any other change.

## How this fits the framework

The graph is the **end state**, not the starting requirement. The framework gives
you the vocabulary (`system`, `domain`, `service`, `contract`, `flow`, `standard`)
and the rules for when you do split. It does not force you to use all of them on day
one.

The sequence is:

```text
one system spec
  -> system + one service
  -> system + services + contracts
  -> add flows when behaviour crosses services
  -> split further only on evidence
```

## Anti-patterns

- **Split by layer**: `controller`, `service`, `repository` specs. Layers are not
  ownership boundaries.
- **Split by file**: one spec per source file. The graph becomes a mirror of the
  code, not a model of the product.
- **Split by endpoint**: one contract spec per endpoint. Contracts are interfaces,
  not routes.
- **Split before the first user**: you are encoding guesses as contracts.
- **Keep the big spec forever**: the opposite failure. If a boundary is stable and
  owned, split it; a big spec that no longer fits a context is a bottleneck.
