# POC mode: infer, label, escalate

A POC stalls when every unknown becomes a question. The alternative is not silent
invention: it is **aggressive, labelled inference**. The agent chooses a default,
writes down why, and moves on. The user reacts to the product instead of
pre-answering it.

## The rule

The agent MAY infer when:

1. the repository, the description, or a user-installed global skill answers it;
2. the choice follows a convention;
3. the choice is cheap to reverse;
4. the choice is recorded in `## Assumptions` or `## Agent Decisions`;
5. the affected requirement's `Source` names the basis.

The agent MUST ask only when the user reserved the fact, a conflict exists, or
there is no reasonable default. A high-risk fact is inferred, fenced, and
confirmed before production.

## What the agent may decide

- language, framework, package manager, test runner, deployment shape;
- naming, ids, directory structure, module boundaries;
- internal data shapes, default values, pagination, error envelope, logging;
- POC simplifications: in-memory store, fake provider, single tenant, seed data;
- UI copy, empty states, and ordering.

## What the agent may infer but must fence

- authentication, authorization, encryption, or data retention;
- who owns a piece of data, who may read or write it, or PII handling;
- pricing, billing, or legal terms;
- compliance obligations;
- a breaking change to a public contract;
- an irreversible migration or a one-way data conversion.

For a POC, mark these `Risk: high`, `Confirmed: agent (POC)`, and
`Revisit: before production`. Build against them only with fake data, a local
provider, and no real users, money, or PII. The validator records them as warnings;
they do not block validation, and contract promotion confirms them.

A fact the user explicitly reserved is different: `Confirmed: needs-human` blocks
validation until the user answers. This is a factual question, not an approval of
the spec.

## Record format

`decision_mode: agent-assisted` is set when either table has a row.

Product or external guesses:

```md
## Assumptions

| # | Assumption | Basis | Risk | Confirmed | Revisit |
|---|---|---|---|---|---|
| 1 | Links are internal-only | no public sharing in the description | medium | no | first user feedback |
| 2 | Users sign in with the company SSO | company convention | high | agent (POC) | before production |
```

Implementation choices:

```md
## Agent Decisions

| # | Question | Chosen | Why | Alternatives | Reversible | Revisit after |
|---|---|---|---|---|---|---|
| 1 | Code generation | random base62 | simple; enough collision space | hash of URL | yes | 10k links |
| 2 | Payment provider | fake provider behind an adapter | POC does not need a real charge | real provider | yes | before any real charge |
```

One row per fact. A row without a revisit trigger is a hidden requirement.

Mark the affected requirement:

```md
### REQ-SYS-001: Shorten a valid URL

- **Priority:** must
- **Normative:** true
- **Source:** assumption
- **Given:** ...
```

## Inference ladder

1. **Observed** — the repository or the description answers it. Cite the evidence.
2. **Conventional** — the ecosystem has a dominant default. Name it.
3. **Assumed** — a reversible product guess. Record basis, risk, revisit.
4. **Ask** — only when the user reserved the fact, or there is no reasonable
   default. A high-risk fact is inferred and fenced. Ask once, batched.

## No approval

There is no human approval step in the POC stage. The `spec-validator` agent sets
`status: validated` when the checklist passes. The user can still change anything
by saying so; the spec returns to `draft` and is re-validated.

## Leaving POC mode

When the spec is promoted to mature stage:

1. Ask the user to confirm every high-risk assumption and every agent decision
   that survived.
2. Turn accepted assumptions into requirements; keep the provenance.
3. Move the rest to `## Open Questions` with an owner.
4. Set `stage: mature`, start semver, and use the proposal flow in
   [`change-mode.md`](change-mode.md).
