---
id: {{id}}
kind: {{kind}}
title: "{{title}}"
summary: "{{summary}}"
version: {{version}}
status: draft
owner: "{{owner}}"
domain: "{{domain}}"
level: "{{level}}"
created: {{date}}
updated: {{date}}
tags: []
decision_mode: human
links: []
---

# {{title}}

> Draft. A service owns one domain and exposes at least one contract.
> Link it with `implements`, `exposes`, `depends-on`, and `constrained-by`.

## Responsibility

What does this service own? What data is it the source of truth for?
What does it explicitly not own?

## Data ownership

- <entity>: <who may write it, who may read it>

## Interfaces

List the contracts this service exposes or consumes. Contracts are separate specs;
do not duplicate their schemas here.

## Dependencies

- `payments` — <why, and what happens when it is unavailable>

## Behaviour and failure modes

Describe the main path and the failure path: timeouts, retries, idempotency,
compensation, and what the caller observes.

## Requirements

### REQ-SVC-001: <testable statement>

- **Priority:** must
- **Normative:** true
- **Given:** <precondition>
- **When:** <action>
- **Then:** <observable outcome>

## Constraints

Link standards and NFRs with `constrained-by`.

## Open Questions

- [ ] <question>

## Agent Decisions

<!-- Optional. Remove this section if every decision is human. One row per decision. -->
| # | Question | Chosen | Why | Alternatives | Reversible | Revisit after |
|---|---|---|---|---|---|---|
| | | | | | | |
