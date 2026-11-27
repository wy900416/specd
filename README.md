# specd

**Spec-driven development for new and mature projects.** Start with a spike when
you need feedback; bootstrap a spec when you know what to build; evolve an approved
baseline when the project is mature. No interview, no ceremony, no runtime.

Specs are plain Markdown. There is no runtime, build step, or parser. The seed
works with GitHub Copilot out of the box, and with any agent that reads
[`AGENTS.md`](AGENTS.md).

New here? Jump to the [quick start](#quick-start) or the
[manual index](docs/README.md).

## Three lanes

| Lane | Question | Flow | When |
|---|---|---|---|
| **Spike** | Would this be useful? | hypothesis -> demo -> feedback -> decide | 90 minutes, before a baseline |
| **Bootstrap** | What exactly to build? | describe -> draft -> validate -> plan -> fleet | new product or pre-baseline spec |
| **Evolution** | How do we change this safely? | change -> impact -> proposal -> tiered approval -> release -> verify | an approved baseline exists |

Start with a spike when you are unsure. Bootstrap creates the first baseline.
Evolution changes an approved baseline; it is opt-in under `mature/` and is the
default once the project is mature.

The end-to-end loop, including gates and artifacts: [`docs/workflow.md`](docs/workflow.md).

## How it works

- **Describe, don't interview.** One paragraph in, one draft spec out. The first
  useful answers come from a running product, not a questionnaire.
- **Infer, but label.** The agent chooses the stack, structure, and defaults, and
  records each guess with a basis, a risk, and a revisit trigger.
- **Fence the risky facts.** Security, privacy, data ownership/PII, authentication,
  retention, pricing, legal, compliance, breaking contracts, and irreversible
  migrations are inferred for the POC only with fake data, marked `Risk: high`,
  and confirmed before promotion. The full list is in SPEC §7.
- **Validate, don't approve.** A separate `spec-validator` applies the checklist
  and binds the result to the file hash. Humans approve only when the project is
  mature.
- **Record every gate.** Validation lives in a marker-delimited block; a mature
  change records `## Proposal validation` and `## Review`, and release binds the
  new baseline with `approved_sha`.
- **Plan before parallel code.** The architect writes `plans/<id>.md`; then
  implementers and the verifier write disjoint files.

## Where the human guard is

Most of the flow is agent-run. A human is in the loop at exactly these points:

| Point | What the human does | Why here |
|---|---|---|
| POC spec | Nothing. `spec-validator` plus the content hash is the gate. | The draft is a cheap hypothesis; speed beats approval. |
| POC exceptions | Resolves an open conflict, answers a `Confirmed: needs-human` fact, or confirms a high-risk fence before promotion. | The agent cannot make a value or fact decision for the user. |
| First baseline | Approves a promotion or a backfill as the `1.0.0` baseline. | This is where a hypothesis becomes a contract. |
| Mature change | Releases after tiered approval: owner for patch/minor, consumers for major, security/data for high risk. | Consumers, contracts, data, and irreversible operations are now involved. |
| Implementation | The verifier is the gate. A human steps in only for an ambiguous requirement or an irreversible rollout. | Tests decide conformance; approval is not a substitute for them. |

The point is not "no humans". It is that the human is asked for the things an
agent cannot decide, and only when the cost of being wrong is real.

## Quick start

`/spike`, `/new-spec`, `/plan-implementation`, `/implement`, and `/change` below
are prompt files for VS Code, Visual Studio, and JetBrains. In Copilot CLI/app
or another agent, describe the same step and name the agent.

### 0. Want a demo first?

```text
/spike Build a URL shortener for a small internal team. Links expire after 30 days.
```

The agent writes `spikes/<id>.md`, builds one fake path on a `spike/<id>` branch,
and demos at the timebox. Then decide: kill, iterate, or graduate to the bootstrap
lane below.

### 1. Get the seed

```bash
git clone https://github.com/wy900416/specd.git my-poc
cd my-poc
```

Or click **Use this template** on GitHub and clone your copy.

### 2. Open it with an agent

| Surface | What to do |
|---|---|
| VS Code + Copilot | Open the folder, open Copilot Chat, select the `specd` agent, and paste the description. If the picker does not show it, reload the window or run `/new-spec`. |
| Copilot CLI/app | Start in the folder and describe the product. `/fleet` is available for implementation. |
| Any other agent | Say: "Read `AGENTS.md` and follow `agents/orchestrator.md`." |

### 3. Describe the product

> Build a URL shortener for a small internal team. Links expire after 30 days, and
> I want a simple web page plus an API.

The agent writes `specs/system/url-shortener.md`, validates it, and reports the
requirements, the assumptions, any fenced high-risk fact, and the validation
result. There is no approval step. If validation blocks, read `## Validation`; the
blocking list names the exact fix.

### 4. Implement

Say **implement**. The architect writes `plans/url-shortener.md` first, then the
fleet implements the code and writes the conformance tests in parallel.

```text
/plan-implementation specs/system/url-shortener.md
/implement specs/system/url-shortener.md
```

### 5. If the project is mature

Do not edit an approved spec. Run:

```text
/change specs/service/orders.md "Add idempotent order creation"
```

Review the impact, compatibility, rollout, rollback, and the approvals needed. A
human releases; a small change goes straight to the implementer, a multi-track
change uses the architect plan and fleet.

Full walkthrough: [`docs/getting-started.md`](docs/getting-started.md).

## What is in the seed

```text
AGENTS.md                 cross-tool agent entry point
SPEC.md                   format and lifecycle, normative
.github/                  Copilot instructions, agents, prompts
agents/                   role briefs (source of truth)
.agents/skills/           spec-draft, spec-gap-fill, spec-validate,
                          spec-context, spec-review, spike
checklists/               validate, context, plan, spike (core)
templates/                system, plan, spike (core)
docs/                     the manual
mature/                   opt-in: change, review, adoption, kind templates
specs/                    your specs land here
spikes/                   timeboxed demo logs
plans/                    implementation plans from the architect
changes/                  mature-stage proposals only
```

The `mature/` pack is opt-in; a new build never needs it.

Annotated layout, including what to copy into an existing repo:
[`docs/repo-layout.md`](docs/repo-layout.md).

## The manual

The full index is [`docs/README.md`](docs/README.md). It has reading paths for a
demo, a new project, a mature change, an adoption, and reference work.

## Normative references

- [`SPEC.md`](SPEC.md) — the format and lifecycle.
- [`AGENTS.md`](AGENTS.md) — the agent entry point and hard rules.
- [`checklists/validate.md`](checklists/validate.md) — the bootstrap validation
  gate.
- [`mature/README.md`](mature/README.md) — the opt-in mature lane.

## What this is not

- Not a formal language. Prose is allowed; structure exists to expose gaps.
- Not a build system. There is no parser, generator, or CI requirement.
- Not a guarantee. Validation catches what the checklist can name, not whether the
  product is worth building.
- Not an interview. The user describes once; the agent infers until a
  user-reserved fact or a conflict forces a question.
- Not POC-only. The evolution lane is the long-term mode: approved baselines,
  changes, impact, release, rollout.
- Not a delivery pipeline for a POC. Use the spike lane to learn; use bootstrap to
  establish the baseline; use evolution to change it.
