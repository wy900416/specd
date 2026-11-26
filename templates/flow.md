---
id: {{id}}
kind: {{kind}}
title: "{{title}}"
summary: "{{summary}}"
version: {{version}}
status: draft
stage: mature
decision_mode: agent-assisted
validated_by: ""
validated_at: ""
validated_sha: ""
owner: "{{owner}}"
domain: "{{domain}}"
level: "{{level}}"
created: {{date}}
updated: {{date}}
tags: []
links: []
---

# {{title}}

> Draft. A flow is the only spec that owns cross-service behaviour. Link it to at
> least two services with `part-of`; the services themselves do not own the flow.

## Trigger

What starts this flow? Synchronous request, event, schedule, or human action?

## Participants

- `orders` — <role>
- `payments` — <role>

## Happy path

1. <step, service, observable result>
2. <step>

## Failure and compensation

| Failure | Detection | Compensation | User-visible result |
|---|---|---|---|
| <failure> | <timeout / error / event> | <action> | <result> |

## Observability

- trace span: <name>
- key attributes: <order id, payment id>
- alert: <condition>

## Requirements

### REQ-FLOW-001: <testable end-to-end statement>

- **Priority:** must
- **Normative:** true
- **Given:** <precondition>
- **When:** <action>
- **Then:** <observable outcome>

## Source

> <the user's description or backfill request, verbatim, with a date>

## Repo Profile

| Area | Finding | Evidence |
|---|---|---|
| Language | | `repo:<path>:<line>` |
| Framework | | `repo:<path>:<line>` |
| Tests | | `repo:<path>:<line>` |
| Conventions | | `repo:<path>:<line>` |

## Context

What problem does this boundary solve, for whom, and why now? State the boundary.

## Assumptions

| # | Assumption | Basis | Risk | Confirmed | Revisit |
|---|---|---|---|---|---|
| | | | | | |

## Agent Decisions

| # | Question | Chosen | Why | Alternatives | Reversible | Revisit after |
|---|---|---|---|---|---|---|
| | | | | | | |

## Conflicts

| # | Other spec | Conflict | Options | Resolution |
|---|---|---|---|---|
| | | | | |


## Open Questions

- [ ] <question>

<!-- BEGIN VALIDATION -->
## Validation

<!-- The validator replaces this block. Keep END as the last line of the file.
     The canonical hash excludes everything between the two markers. -->
- Not run yet. The validator writes this section.
<!-- END VALIDATION -->
