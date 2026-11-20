# POC mode: agent decisions

A POC often stalls on questions the user has not decided yet. Waiting for every
answer is slower than building a default and letting the user react to it.

POC mode lets an agent choose a default. It does **not** let the agent invent
silently. Every agent decision is recorded, marked, and reversible.

## The rule

An agent may decide when all of these hold:

1. the user said "I don't know", "you decide", or "not sure";
2. the decision is reversible, or cheap to reverse;
3. it does not change security, privacy, compliance, data ownership, pricing,
   legal terms, or the breaking behaviour of a public contract;
4. the decision is recorded in `## Agent Decisions`;
5. the affected requirement is marked `**Decided by:** agent (POC)`.

If any condition fails, the question stays in `## Open Questions`.

## Why

- **Speed.** A POC needs a decision to test the product; a blank question block
  does not produce feedback.
- **Feedback beats speculation.** The user often cannot answer abstractly but can
  react to a working default.
- **Reversibility.** A recorded, low-cost default is cheaper to change than a
  delayed POC.
- **Provenance.** The next reader must know which decisions were human and which
  were agent defaults. Silent invention destroys trust in the spec.

## What the agent may decide

- naming, ids, and internal structure that do not leak into a public contract;
- a conventional default where alternatives are close (UUID vs sequential id,
  cursor vs offset pagination);
- a POC-only simplification that is easy to replace (in-memory store, fake
  provider, single-tenant);
- the order of steps in a flow when the user has no preference.

## What the agent must not decide

- authentication, authorization, encryption, or data retention;
- who owns a piece of data, or who may write it;
- pricing, billing, or legal terms;
- a breaking change to a public contract;
- an irreversible migration or a one-way data conversion;
- anything the user explicitly said they want to decide.

When in doubt, ask once. If the user still has no answer and the decision is
high-risk, record it as an open question, not an agent decision.

## Record format

Set the front-matter flag:

```yaml
decision_mode: agent-assisted
```

Add this section to the spec:

```md
## Agent Decisions

| # | Question | Chosen | Why | Alternatives | Reversible | Revisit after |
|---|---|---|---|---|---|---|
| 1 | Order id source | service-generated UUID | conventional; avoids client collisions | client-supplied id | yes | first user feedback |
| 2 | Payment provider | fake provider behind an adapter | POC does not need a real charge | real provider | yes | before any real charge |
```

Mark the affected requirement:

```md
### REQ-ORD-001: Create an order idempotently

- **Priority:** must
- **Normative:** true
- **Decided by:** agent (POC) — revisit after first user feedback
- **Given:** ...
```

One decision per row. Do not bundle three choices into one rationale. A decision
without a revisit trigger is a hidden requirement.

## Lifecycle

```text
user: "I don't know"
  -> agent picks a reversible default
  -> records it in ## Agent Decisions
  -> marks the requirement
  -> user tries the POC
  -> user reacts: accept / override / change the product
  -> revise the spec (proposal if approved)
```

The agent decision is expected to change. That is the point. It is a **default**,
not a commitment.

## Review

The spec reviewer checks:

- every agent decision is marked inline and listed in `## Agent Decisions`;
- each is reversible, or the cost of reversal is stated;
- none touches the high-risk list;
- each has a revisit trigger;
- the human accepting the draft explicitly accepts or overrides the decisions.

Human approval accepts the draft. It does not turn an agent decision into a human
decision; the provenance stays. If the user later decides, change the spec through
a proposal and keep the history.

## Leaving POC mode

When the product has real users and the decisions start to matter:

1. Ask the user to accept, override, or defer each `## Agent Decisions` row.
2. Move accepted rows to the body as normal requirements; keep the provenance in
   the review history.
3. Move deferred rows to `## Open Questions`.
4. Remove the `**Decided by:** agent (POC)` marker only when a human has explicitly
   decided that requirement. Set `decision_mode: human` when no agent decisions
   remain.
5. Version the spec as a release.
