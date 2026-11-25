---
mode: 'agent'
description: 'Generate specs/INDEX.md from the spec front-matter once the graph is large enough to need it.'
---

Generate `specs/INDEX.md` from the front-matter of `specs/**/*.md`.

Only do this when the trigger in `docs/index.md` is met: more than 20 specs, more
than 3 owners, a full read no longer fits the context budget, two missed
conflicts, or a CI step that needs an entry point. If the trigger is not met, say
so and stop.

Format:

```md
# Spec index

- generated_at: <ISO-8601>
- spec_count: <n>
- source: front-matter

| id | kind | stage | status | owner | summary | links |
|---|---|---|---|---|---|---|
```

Rules:

- Derive every row from the spec files. Do not invent.
- Include outgoing link targets, comma-separated.
- Sort by `kind`, then `id`.
- Never treat the index as the source of truth. If it disagrees with a spec, the
  spec wins.
- Do not edit any spec.
