# The specd manual

The [README](../README.md) has the pitch and the three lanes. This page is the full
index: pick a reading path, or jump to a document.

This is the manual's table of contents. It is not `specs/INDEX.md`, which is the
derived spec index and follows its own rule in [`index.md`](index.md).

## Terms

| Term | Meaning |
|---|---|
| `stage: poc` | The pre-baseline spec stage. Version stays `0.1.0`; the validator is the gate. |
| **spike** | An optional 90-minute demo lane. A spike is not a spec and its code is throwaway. |
| **bootstrap** | The lane that writes the first spec and the first implementation. |
| **evolution** | The lane for changing an approved (`stage: mature`) baseline. |
| **mature** | An approved baseline with consumers, a version, and tiered approvals. |

## Reading paths

| You want to... | Read |
|---|---|
| See the whole loop | [`workflow.md`](workflow.md) — one end-to-end diagram |
| See a demo today | [`spike.md`](spike.md) — one hypothesis, one fake path, 90 minutes |
| Start a new project | [`getting-started.md`](getting-started.md) → [`bootstrap-mode.md`](bootstrap-mode.md) → [`implementation.md`](implementation.md) |
| Change an approved baseline | [`../mature/README.md`](../mature/README.md) — the opt-in mature lane |
| Understand the reasoning | [`vibe-spec.md`](vibe-spec.md), [`poc-mode.md`](poc-mode.md), [`decisions.md`](decisions.md) |
| Run parallel agents safely | [`fleet.md`](fleet.md) — disjoint files, tests after writes |
| Fix a stuck flow | [`troubleshooting.md`](troubleshooting.md) |
| Look up a role or command | [`agents.md`](agents.md) |
| Know the required spec format | [`../SPEC.md`](../SPEC.md) — normative |

## Documents

### Start here

| Document | What it covers |
|---|---|
| [`workflow.md`](workflow.md) | The complete loop: spike, bootstrap, evolution, and human gates |
| [`getting-started.md`](getting-started.md) | Prerequisites, clone, open an agent, first spec, first build |
| [`repo-layout.md`](repo-layout.md) | The seed's directory tree, annotated |
| [`agents.md`](agents.md) | Copilot surfaces, file layout, which agent, slash commands, global skills |

### Core lanes

| Document | What it covers |
|---|---|
| [`spike.md`](spike.md) | 90-minute demo: hypothesis, demo contract, feedback, kill/iterate/graduate |
| [`bootstrap-mode.md`](bootstrap-mode.md) | The first spec: draft, infer, validate, what a spec looks like, changing a draft |

### Mature lane (opt-in)

| Document | What it covers |
|---|---|
| [`../mature/README.md`](../mature/README.md) | When and how to use the mature pack |
| [`../mature/docs/change-mode.md`](../mature/docs/change-mode.md) | Evolution: baseline, change request, impact, proposal, approval tiers, release, rollout |
| [`../mature/docs/adoption.md`](../mature/docs/adoption.md) | Backfilling a mature project, manual baseline, what to backfill first |

### Building

| Document | What it covers |
|---|---|
| [`implementation.md`](implementation.md) | Plan → fleet: the plan's contents, running tracks, reading the result, when not to fleet |
| [`fleet.md`](fleet.md) | Safe parallel work and prompt patterns for implementation and test generation |
| [`one-big-spec.md`](one-big-spec.md) | Why one system spec is the POC default, and when to split |

### Model and policy

| Document | What it covers |
|---|---|
| [`vibe-spec.md`](vibe-spec.md) | Why describe-infer-validate replaces the interview |
| [`poc-mode.md`](poc-mode.md) | The inference ladder, assumptions, agent decisions, high-risk fences |
| [`index.md`](index.md) | When `specs/INDEX.md` earns its keep, and what it contains |
| [`decisions.md`](decisions.md) | Why each default exists, and what it costs |

### Reference

| Document | What it covers |
|---|---|
| [`troubleshooting.md`](troubleshooting.md) | Symptom → fix for the common stalls |
| [`../SPEC.md`](../SPEC.md) | Normative format and lifecycle |
| [`../AGENTS.md`](../AGENTS.md) | Agent entry point and hard rules |
| [`../checklists/validate.md`](../checklists/validate.md) | The bootstrap validation gate |
| [`../mature/checklists/validate-proposal.md`](../mature/checklists/validate-proposal.md) | The mature-change proposal gate |

## Keeping this useful

- Keep a document to one job. If it starts covering two, split it and add a row
  here.
- This page lists documents; it does not restate them. If you find yourself
  copying content here, link instead.
- When a document is added, renamed, or removed, update this page in the same
  change.
