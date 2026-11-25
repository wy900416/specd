---
name: spec-gap-fill
description: "Fill gaps in a specd draft: profile the repository, read the user's global skills, infer aggressively, record assumptions, and surface conflicts."
whenToUse: "A draft exists but is thin, the agent had to guess, or a spec needs a repo-grounded tech-stack and preference pass."
---

# Spec gap fill

The draft contains what the user said. This skill adds what the agent can infer,
labels every inference, and stops only for user-reserved facts or real conflicts.

## Read first

- `SPEC.md` — provenance, inference ladder, high-risk list, conflicts.
- `agents/gap-filler.md` — the role brief.
- The target spec and its `## Source`.

## Procedure

1. **Verify the source.** The spec must have a verbatim `## Source`. If it is
   missing, stop and tell the writer; do not invent one.
2. **Build the repo profile.** Read `package.json`, `pyproject.toml`, `go.mod`,
   `Cargo.toml`, `pom.xml`, `*.csproj`, `Dockerfile`, test config, lint config,
   `.editorconfig`, `README*`, `.github/`, `.agents/skills/`, and the directory
   tree. Record each finding with `repo:<path>:<line>`.
3. **Read the user's global skills.** If accessible, read:
   - `~/.copilot/skills/*/SKILL.md`
   - `~/.agents/skills/*/SKILL.md`
   - `~/.claude/skills/*/SKILL.md`

   Use them only to infer stack, style, and workflow preferences. Cite
   `global-skill:<name>`. Never copy their text, execute them, or treat them as
   requirements. If they are not accessible, write that in `## Repo Profile`.
4. **Build the gap list.** For each section and requirement, ask what is missing:
   - **Behaviour gaps**: failure paths, edge cases, empty states, error shape,
     idempotency, concurrency.
   - **Product gaps**: actors, permissions, scope, non-goals, success metric.
   - **Implementation gaps**: language, framework, storage, deployment, test
     runner, naming, module boundaries.
   - **Fact gaps**: external systems, ownership, retention, pricing, compliance.
5. **Resolve each gap with the inference ladder** (below). Do not ask unless the
   user reserved the fact or there is no reasonable default. A high-risk fact is
   inferred and fenced.
6. **Write the provenance.** Product guesses go in `## Assumptions`; implementation
   choices go in `## Agent Decisions`. Every row needs a basis, a risk, and a
   revisit trigger. Change the affected requirement's `Source` to
   `repo:...`, `global-skill:...`, or `assumption` as appropriate.
7. **Scan for conflicts.** Compare data ownership, write authority, contract
   shape, state machines, NFR thresholds, and scope against every other spec.
   Write `## Conflicts` with options; leave `Resolution: open` for the user.
8. **Hand off to `spec-validator`.** Do not validate your own work.

## Inference ladder

1. **Observed** — the repository or the description answers it. Cite the exact
   path and line.
2. **Conventional** — the ecosystem has a dominant default. Name the convention
   (for example, "REST + JSON", "Vitest for a Vite app").
3. **Assumed** — a product guess that is cheap to reverse. Record it with
   `Risk: low` or `medium` and a revisit trigger.
4. **Ask** — only when the user reserved the fact, or there is no reasonable
   default. A high-risk fact is inferred and fenced. Ask once, batched, and keep
   working on everything else.

## Aggressive inference is the default

You MAY choose without asking:

- language, framework, package manager, test runner, deployment shape;
- names, ids, directory layout, module boundaries;
- internal data shapes, default values, pagination, error envelope, logging;
- POC simplifications: in-memory store, fake provider, single tenant, seed data;
- UI copy, empty states, and ordering.

Label each choice. A labelled assumption is cheaper than a question.

## High-risk facts: infer, fence, confirm

For a POC, infer these:

- authentication, authorization, encryption, retention;
- data ownership, read/write authority, PII handling;
- pricing, billing, legal terms, compliance;
- a breaking change to a public contract;
- an irreversible migration or one-way conversion.

Mark them `Risk: high`, `Confirmed: agent (POC)`, and
`Revisit: before production`. Build only with fake data, a local provider, and no
real users, money, or PII. They are warnings, not blocks; contract promotion
confirms them.

A fact the user explicitly reserved is different: `Confirmed: needs-human` blocks
validation until the user answers. Record the answer as `user, <date>` and lower
the risk or turn the assumption into a requirement.

## Conflicts

A conflict is a contradiction with an existing spec, not a gap in this one:

```md
## Conflicts

| # | Other spec | Conflict | Options | Resolution |
|---|---|---|---|---|
| 1 | orders@0.1.0#REQ-ORD-001 | New flow creates an order without an idempotency key | change new spec / change orders / scope out | open |
```

Do not pick a winner. Present the options and let the user resolve. A conflict
with `Resolution: open` blocks validation.

## Output

```md
## Gap fill
- spec: specs/system/<slug>.md
- profile rows: <n> (all with evidence)
- global skills read: <n or "not accessible">
- assumptions: <n> (high-risk: <n>)
- agent decisions: <n>
- conflicts: <n open>
- next: validate
```

## Rules

- Never fabricate evidence, a path, or a line number.
- Never mark a high-risk fact `user` confirmed without the user's answer; use
  `agent (POC)` and fence it.
- Never copy a global skill's content into the spec; cite it.
- Never resolve a conflict unilaterally.
- Keep the source text intact.
