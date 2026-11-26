# When to introduce an index

The spec graph ships without an index. `specs/**/*.md` is the source of truth, and
the front-matter `summary` is enough to scan a small graph.

An index is a **derived view**. It is useful when reading every spec has become
more expensive than maintaining a list. It is harmful when it becomes a second
source of truth that drifts from the files.

## Default: no index

At POC scale:

- there are one to ten specs;
- the whole graph fits in one context;
- conflict detection reads every spec, which is cheap and accurate;
- `summary`, `id`, and headings are enough to decide what to open.

Adding an index early adds a file to update and a second place to be wrong.

## Triggers

Create `specs/INDEX.md` when **any** one is true:

| Trigger | Threshold | Why |
|---|---|---|
| Scale | more than 20 specs | Full reads get expensive and noisy |
| Ownership | more than 3 owners | Readers need to find the owning spec fast |
| Context budget | a full read no longer fits (~100k tokens) | The agent cannot hold the graph |
| Missed conflicts | conflict detection missed a real conflict twice | The scan is no longer reliable |
| Deterministic tooling | CI or a search step needs one entry point | A generated list beats a bespoke script |

Do not introduce one because the repository "looks small without it".

## What it contains

`specs/INDEX.md` is a table derived from front-matter:

```md
# Spec index

- generated_at: 2026-11-25T09:00:00+08:00
- spec_count: 24
- source: front-matter

| id | kind | stage | status | owner | summary | links |
|---|---|---|---|---|---|---|
| orders | service | poc | validated | orders-team | Owns the order state machine | commerce, orders-api |
```

- One row per spec.
- Sort by `kind`, then `id`.
- `links` lists outgoing targets, comma-separated.
- No prose, no status narrative, no decisions.

## How it is generated

Use the `build-index` prompt, or generate it by hand from the same fields. The
generation is mechanical: `id`, `kind`, `stage`, `status`, `owner`, `summary`,
`links`.

A generated index is a cache. Deleting it must not lose information.

## Freshness

- `generated_at` and `spec_count` are mandatory.
- If the index exists, the validator warns when `spec_count` differs from the
  number of spec files.
- A stale index is a warning, not a block, unless a consumer relies on it.
- Never let a spec update depend on the index being current. The spec wins.

## Anti-patterns

- Hand-editing a row instead of the spec.
- Adding fields to the index that are not in the spec.
- Making the index required for validation.
- Generating it on every commit before there is a reader.
- Treating a stale index as evidence that the spec changed.
