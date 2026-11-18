# specd

Spec-driven development in **plain Markdown**. No runtime, no build step, no
parser, no Python. A spec is a file; the graph is a set of typed links; the agent
is whatever chat or coding agent you already use.

This repository is a small, runnable example of the format plus the instructions
that make it work: skills for interviewing, context packing, and review, and role
briefs for a spec writer and an architecture reviewer.

## Why no tooling

- **Portable.** Works with any agent, editor, or human. Nothing to install.
- **Inspectable.** Front-matter, headings, and links are the interface. No hidden
  index or generated state.
- **Reviewable.** The diff is the spec diff; the proposal is a file.
- **Honest.** Without a linter, validation is a checklist and a review. That is a
  real tradeoff: it relies on discipline and on agents following the checklist.

If you later want a linter or a viewer, it can be added *on top of* these files
without changing the format.

## Quick start

Open the repository in any agent and say:

```text
Read AGENTS.md and follow it.
Load .agents/skills/spec-interview/SKILL.md and follow agents/spec-writer.md.
We need a spec for the refund flow. Ask one question at a time.
```

Or, for a review:

```text
Read AGENTS.md, then agents/architecture.md.
Task: review the proposed change to orders-api.
```

DSH discovers the skills in `.agents/skills/` automatically. Claude Code, Cursor,
Codex, and others can read the same files; if your tool uses a different rules
directory, copy the folders there. The `AGENTS.md` file is the portable entry
point.

## Layout

```
SPEC.md                    the format and lifecycle, normative
AGENTS.md                  agent entry point and hard rules
GRAPH.md                   a view (Mermaid graph + table), not the source of truth
CHANGES.md                 how a proposal is created, reviewed, and released
checklists/
  validate.md              mechanical checks before approval
  context.md               bounded context packing
  review.md                judgement, severity, bump guide
templates/                 skeletons for each kind + a change proposal
specs/                     the graph; only specs live here
changes/                   open proposals; archive/ for released ones
.agents/skills/            plain-Markdown skills
agents/                    role briefs
```

## The loop

```
draft ──edit──▶ review ──human approves──▶ approved
                                            │
                               agent writes a proposal
                                            ▼
                                  changes/CHG-...md
                                            │
                               human reviews diff + releases
                                            ▼
                                  approved, version bumped
```

- A **draft** is editable by anyone.
- An **approved** spec is read-only for agents.
- A change is a **copy** of the target in `changes/`, with the full proposed body.
- A human approves a draft, and a human releases a proposal. Agents prepare; they
  do not approve or release.

## Skills

| Skill | What it does |
|---|---|
| [`spec-interview`](.agents/skills/spec-interview/SKILL.md) | one-question-at-a-time interview -> draft or proposal -> review packet |
| [`spec-context`](.agents/skills/spec-context/SKILL.md) | bounded, prioritized context pack with a manifest |
| [`spec-review`](.agents/skills/spec-review/SKILL.md) | checklists + impact + version hygiene -> review packet |

Each is a directory with a `SKILL.md` and, where useful, a `references/` folder.
The body is loaded on demand; the references hold the long question bank.

## Agents

| Brief | Role |
|---|---|
| [`agents/spec-writer.md`](agents/spec-writer.md) | interviewer / writer |
| [`agents/implementer.md`](agents/implementer.md) | implements a task from a context pack |
| [`agents/verifier.md`](agents/verifier.md) | writes conformance tests from the spec |
| [`agents/architecture.md`](agents/architecture.md) | boundary and contract reviewer |

The handoff is:

```text
writer -> implementer -> verifier -> reviewer -> human release
```

The verifier receives the spec and the test harness, **not** the implementer's
plan. It writes tests from the spec, so an implementation cannot define its own
acceptance. These are role briefs, not presets. Paste one into any agent as its
system prompt, or point the agent at the file. See
[`agents/README.md`](agents/README.md).

## Demo graph

A tiny checkout system, used as a fixture:

- `demo-shop` (system) -> `commerce` (domain)
- `orders` and `payments` (services)
- `orders-api` and `payments-api` (contracts)
- `place-order` (flow)
- `security-baseline` (pinned standard) and `latency-budget` (NFR)

See [`GRAPH.md`](GRAPH.md) for the graph view. Replace the demo with the real
system; keep the shape.

## Validation

There is no linter. Before approval, apply
[`checklists/validate.md`](checklists/validate.md); before release, apply
[`checklists/review.md`](checklists/review.md). Every finding cites a file and
line. A warning is allowed only with a one-line explanation.

The checks cover front-matter, unique ids, links, requirements, kind-specific
rules, graph hygiene, version hygiene, security, and view freshness. The security
checks matter because specs are inputs to agents: treat them as untrusted.

## Versioning

- `version` is semver and changes **only** on release.
- A new draft starts at `0.1.0`; a first approval is `1.0.0`.
- Bumps: `none` (editorial), `patch` (clarification), `minor` (additive),
  `major` (breaking).
- References use `id@version#REQ-ID`, for example `orders@0.1.0#REQ-ORD-001`.

## Adopt it in a real repository

1. Copy `SPEC.md`, `AGENTS.md`, `checklists/`, `templates/`, `.agents/skills/`,
   and `agents/` into your repository.
2. Delete the demo specs, or keep them as an example.
3. Write **one** system spec and **one** service spec by hand. Do not start with
   the whole microservice estate.
4. Give the service spec to an agent and watch where it has to guess. Those gaps
   are the next requirements.
5. Add a pinned standard and one contract. Then add a flow.
6. Only then scale to the rest.

The framework is deliberately small. The hard part is not the format; it is
keeping the graph consistent as the system changes.

## What this is not

- Not a formal language. Prose is allowed; structure exists to expose gaps.
- Not a build system. There is no parser, generator, or CI requirement.
- Not a replacement for tests or contract checks. A spec should lead to them, but
  this repository only defines the spec layer.
- Not a guarantee. A checklist can pass on a bad spec; the review has to say what
  the checklist cannot see.
