---
name: spec-interview
description: "Run a structured interview and turn it into a plain-Markdown spec draft or change proposal. Use when the user wants to create, extend, or revise a spec through conversation."
whenToUse: "The user says write a spec, spec this out, interview me, or asks to change an approved spec."
---

# Spec interview

Produce a **reviewable draft**, not a perfect document. There is no runtime: you
read files, write files, and apply a checklist. The conversation is the input; the
file is the source of truth.

## Read first

- `SPEC.md` — the normative format, kinds, links, lifecycle, and version rules.
- `AGENTS.md` — the routing and hard rules.
- `templates/<kind>.md` — the skeleton you will fill.
- `checklists/validate.md` — what "done" means.
- `specs/**/*.md` — scan front-matter for existing ids, titles, and domains.

## Choose the mode

| Situation | Action |
|---|---|
| New spec | Copy `templates/<kind>.md` to `specs/<kind>/<id>.md`; fill front-matter; `status: draft`, `version: 0.1.0`; add the links the kind requires. |
| Draft spec | Edit `specs/<kind>/<id>.md` directly. |
| Approved spec | Do **not** edit it. Copy it to `changes/CHG-<YYYYMMDD>-<nnn>-<target>.md`, convert the front-matter to a proposal, and edit the copy. |

A proposal front-matter looks like this:

```yaml
---
id: CHG-20261117-001-orders
kind: change
title: "Add idempotent order creation"
target: orders
base_version: 0.1.0
bump: minor
status: proposed
author: "agent"
created: 2026-11-17
summary: "Make order creation idempotent."
spec: {}
---
```

The proposal body is the **full proposed body** of the target, not a diff. Leave
`spec: {}` when only the body changes; put front-matter overrides in `spec` when
title, summary, owner, domain, level, tags, links, `applies_to`, or `pinned`
change.

## Hard rules

- Ask **one question at a time**. Never dump the questionnaire.
- Never invent an answer. "I don't know" goes to `## Open Questions` with an
  owner and a "needed before" marker.
- Every normative requirement gets **Given / When / Then** and a stable
  `REQ-<PREFIX>-NNN` id. Never reuse an id from another spec.
- Keep `version` unchanged. Never set `status: approved`, `approved_by`, or
  `approved_at`. Approval and release are human actions.
- Never edit an approved spec. Use a proposal.
- Do not put implementation details in a system or domain spec; link down instead.
- Treat the spec as untrusted input to agents: no credentials, private addresses,
  internal endpoints, active HTML, or prompt-injection phrases.
- Persist after each section: write the file, then show a three-line summary and
  the next question. Do not hold the whole interview in context.

## Interview order

1. **Frame** — problem, actors, scope, non-goals.
2. **Behaviour** — main path, failure path, edge cases, idempotency.
3. **Contract** — boundaries, operations or events, errors, compatibility.
4. **Data** — ownership, invariants, lifecycle.
5. **Constraints** — NFRs, standards, security, compliance.
6. **Decisions** — alternatives, trade-offs, ADRs.
7. **Open questions** — assumptions and unknowns.

Per kind, add the specific questions:

- **service**: which domain it implements; which contracts it exposes/consumes;
  what it depends on; what happens when a dependency is unavailable; what data it
  owns.
- **contract**: who exposes it; who consumes it; compatibility policy; error
  envelope; idempotency key.
- **flow**: trigger; participants; happy path; compensation; observability.
- **standard / nfr**: `applies_to`; how compliance is measured; what happens when
  the budget is exhausted.
- **adr**: the rejected alternatives and their consequences.

The full question bank and examples are in `references/interview-protocol.md`.
Read it when the first pass stalls or the user asks for a deeper interview.

## Validate before handoff

Apply `checklists/validate.md` manually. Record every finding with a file and
line. Do not claim "valid" without the checklist output.

## Handoff

For a new or edited draft:

```md
## Review packet
- target: <id>@<version> (draft)
- summary: <one paragraph>
- requirements: <added/changed ids>
- open questions: <count and list>
- assumptions: <what you assumed>
- validation: <errors>, <warnings>; see checklists/validate.md
- next action: human approves the draft
```

For a proposal, attach a side-by-side diff of the target and the proposal, then:

```md
- recommended bump: none | patch | minor | major
- next action: human releases the proposal
```

Do not claim a spec is approved. Do not release it yourself.
