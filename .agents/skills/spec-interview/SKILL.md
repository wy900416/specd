---
name: spec-interview
description: "Run a structured interview and turn it into a specd spec or change proposal. Use when the user wants to create, extend, or revise a spec through conversation."
whenToUse: "The user says write a spec, spec this out, interview me, or asks to change an approved spec."
---

# Spec interview

Produce a **reviewable draft**, not a perfect document. The conversation is the
input; the file is the source of truth. A good interview exposes gaps instead of
filling them with plausible prose.

## Before the first question

1. Read the `specs/` tree. If `index.json` is missing or stale, run `./specd.sh index`.
2. Decide the mode:
   - **new spec** -> `./specd.sh new <kind> <id> ...`, then edit `specs/<kind>/<id>.md`
   - **change to an approved spec** -> `./specd.sh propose <id> --bump <bump> --summary <text>`,
     then edit `changes/CHG-....md`
   - **draft spec** -> edit it directly
3. Decide the kind: `system`, `domain`, `service`, `contract`, `flow`, `nfr`, `adr`, `standard`.
4. If the target is ambiguous, ask one question with two or three concrete candidates.

`specd new` only fills the template. Immediately add the links the kind requires:
a service gets `implements` -> its domain, `exposes` -> its contract, and
`constrained-by` -> the standards/NFRs that apply. Run `./specd.sh validate` after
the first edit, not only at the end.

## Hard rules

- Ask **one question at a time**. Never dump the questionnaire.
- Never invent an answer. "I don't know" goes to `## Open Questions`.
- Every normative requirement gets **Given / When / Then** and a stable
  `REQ-<PREFIX>-NNN` id. Never reuse an id from another spec.
- Keep `version` unchanged. Never set `status: approved`, `approved_by`, or
  `approved_at`. Approval and release are human actions.
- Never edit a published (approved) spec. Use a change proposal.
- Do not put implementation details in a system or domain spec; link down instead.
- Run `./specd.sh scan --strict` before handoff. Never store credentials, private
  addresses, or internal endpoints in a spec.
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

## Commands

```bash
./specd.sh new service orders --title "Orders Service" --owner orders-team --domain commerce
./specd.sh propose orders --bump minor --summary "Add idempotent order creation"
./specd.sh validate
./specd.sh fitness
./specd.sh scan --strict
./specd.sh diff changes/CHG-....md
```

`propose` only works on an **approved** target. If the target is a draft, edit it
directly and ask a human to approve it when it is ready.

## Handoff

For a new draft, end with:

```md
## Review packet
- target: <id>@<version> (draft)
- summary: <one paragraph>
- requirements: <added/changed ids>
- open questions: <count and list>
- assumptions: <what you assumed>
- validation: `specd validate`, `specd fitness`, `specd scan`
- next action: human approves the draft
```

For a proposal, replace the last line with the `specd diff` output and:

```md
- recommended bump: none | patch | minor | major
- next action: human runs `specd release <proposal> --by <name>`
```

Do not claim a spec is approved. Do not run `release` yourself.
