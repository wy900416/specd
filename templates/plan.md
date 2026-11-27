---
plan: "plan-{{spec_id}}"
spec: "{{spec_id}}"
spec_sha: "{{spec_sha}}"
change: ""
status: draft
created: {{date}}
updated: {{date}}
owner: "agent:architect"
---

# Implementation plan: {{title}}

> A plan is not a spec. It coordinates implementation and test generation. It is
> bound to the spec's canonical hash: if the spec changes, this plan is `stale`.

## Scope

- Spec: `{{spec_id}}` (validated)
- In scope: `REQ-...`
- Out of scope: <explicit non-goals for this implementation>

## Decision

- Recommendation: build | build a slice | wait
- Smallest slice that answers the product question: <one paragraph>
- Why now: <the evidence or user signal>
- What would change the decision: <trigger>

## Architecture

- Shape: <single module / modular monolith / services>
- Components: <name -> responsibility>
- Data flow: <request/event -> module -> store -> response>
- Storage: <what is stored, where, and what is faked for the POC>
- Interfaces: <HTTP, CLI, events, function boundaries>
- Rejected alternatives: <choice -> why not>

## File Map

| Path | Action | Track | Depends on |
|---|---|---|---|
| `<path>` | create / modify | T1 | |

## Work Tracks

Tracks must own disjoint file sets. Implementation and test tracks may run in
parallel; execution happens after both land.

| Track | Agent | Files | Depends on | Done when |
|---|---|---|---|---|
| T1 | implementer | `<paths>` | | tests for REQ-... pass |
| V1 | verifier | `tests/...` | | every in-scope REQ has a test |

## Test Strategy

Conformance:

| REQ | Test file | Level | Owner |
|---|---|---|---|
| `REQ-...` | `tests/...` | unit / integration / black-box | implementer or verifier |

Acceptance:

| GOAL / criterion | Test file | Level | Owner |
|---|---|---|---|
| `GOAL-...` / <criterion> | `tests/...` | black-box | verifier |

- Conformance gate: the verifier owns the black-box tests written from the spec.
- Acceptance gate: the verifier owns the tests for `## Acceptance`; the user accepts.
- Developer tests: the implementer owns unit/integration tests.
- The verifier receives this table, not the architecture notes.

## Risks and Fences

- From the spec: <high-risk assumption>, stays fake: <data/provider/auth>.
- Implementation risk: <risk -> mitigation>.
- Irreversible step: <none, or what needs a human before running>.

## Open Questions

- [ ] <question> — owner: <team> — blocks: ready

## Verification

- Command: `<test command>`
- Expected: every in-scope REQ has a passing test; failures classified as code
  bug, spec ambiguity, or harness issue.

## Change log

- {{date}}: created.
