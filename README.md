# Spec-driven workspace

A small, runnable spec graph with conversational agents on top. The engine is
`specd` (Python, in `specd/`); the operating layer is three DSH skills and two
agent briefs.

## Quick start

```bash
./specd.sh validate        # schema, links, requirements
./specd.sh fitness         # architecture rules
./specd.sh scan --strict   # injection / secrets / internal endpoints
./specd.sh index           # build index.json
./specd.sh build           # static viewer at dist/index.html
./specd.sh context orders --task "add idempotency" --budget 8000
```

`./specd.sh` is a wrapper around `python3 -m specd`; it sets the workspace as the
project root, so it works from any directory.

## Layout

```
specs/                     published and draft specs
  system/                  L0 system intent
  domain/                  L1 bounded contexts
  service/                 L2 services
  contract/                L2 API / event contracts
  flow/                    cross-service flows
  nfr/                     non-functional requirements
  standard/                cross-cutting standards (pinnable)
templates/                 skeletons used by `specd new`
changes/                   change proposals (agent-writable)
changes/archive/           released proposals
agents/                    role briefs (architecture, spec-writer)
.agents/skills/            DSH-discovered skills
  spec-interview/          conversational drafting
  spec-context/            bounded context packing
  spec-review/             review and impact
specd/                     the engine (CLI + library)
dist/                      generated static viewer
index.json                 generated index
```

## The loop

```
draft ──edit──▶ review ──human approve──▶ published (approved)
                                           │
                              agent proposes a change
                                           ▼
                                    changes/CHG-...md
                                           │
                              human reviews diff + releases
                                           ▼
                                  published, version bumped
```

- A **draft** is editable by anyone.
- A **published** spec is read-only for agents. Changes go through
  `./specd.sh propose`, which copies the body into `changes/`.
- `./specd.sh release` applies a proposal, bumps the version, archives the
  proposal, and records the approval. Only a human runs it.
- `version` is a release decision, never an edit side effect. `validate` warns
  when an approved body changes without a release (`W051`) or the version moves
  outside `release` (`W052`).

## Skills

| Skill | What it does |
|---|---|
| `spec-interview` | one-question-at-a-time interview -> draft or proposal -> review packet |
| `spec-context` | bounded, prioritized context pack with a manifest |
| `spec-review` | lint + fitness + impact + version hygiene -> review packet |

They are discovered from `.agents/skills/` by DSH and appear in the session skill
catalog. In a chat, ask the agent to load one, or invoke it by name. They can also
be used outside DSH: the `SKILL.md` files are ordinary instructions.

## Agents

| Brief | Role |
|---|---|
| `agents/spec-writer.md` | interviewer / writer; loads `spec-interview` |
| `agents/architecture.md` | boundary reviewer; loads `spec-context` + `spec-review` |

These are role briefs, not DSH presets. Use one as a subagent prompt:

```text
Read agents/architecture.md and follow it.
Task: review the proposed change to orders-api.
```

See `agents/README.md` for details.

## Demo graph

The fixture is a tiny checkout system:

- `demo-shop` (system) -> `commerce` (domain)
- `orders` and `payments` (services)
- `orders-api` and `payments-api` (contracts)
- `place-order` (flow)
- `security-baseline` (pinned standard) and `latency-budget` (NFR)

It passes `validate`, `fitness`, and `scan`. Replace it with the real system.

## Spec format

A spec is Markdown with YAML front-matter. Requirements use stable ids:

```md
### REQ-ORD-001: Create an order idempotently

- **Priority:** must
- **Normative:** true
- **Given:** a client submits the same `Idempotency-Key` twice
- **When:** both requests reach the service
- **Then:** exactly one order is created and both responses carry the same order id
```

Key fields: `id`, `kind`, `title`, `version`, `status`, `owner`, `links`
(typed edges), and for contracts `type` + `path`. See `templates/` for each kind.

## What is intentionally missing

This is the smallest runnable loop, not the full platform. Still absent:

- CI wiring and CODEOWNERS;
- code/trace reconciliation (`specd` has `trace`, but no runtime import);
- multi-service change sets and consumer sign-off;
- a web editor (the viewer is read-only);
- a `specd approve` command for new drafts (a human edits the front-matter today).

Those are the next layers, in that order.
