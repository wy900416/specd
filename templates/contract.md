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
domain: ""
level: "{{level}}"
type: "{{type}}"
path: "{{contract_path}}"
created: {{date}}
updated: {{date}}
tags: []
links: []
---

# {{title}}

> Draft. The schema file is the source of truth for wire format; this spec carries
> intent, compatibility policy, and the contract's social obligations.

## Type and location

- type: `{{type}}` (openapi / asyncapi / schema / proto / graphql / grpc / other)
- path: `{{contract_path}}` (relative to this file)

## Purpose

Which service exposes this contract, and which services consume it?

## Operations or messages

| Name | Kind | Caller | Notes |
|---|---|---|---|
| <operationId or event name> | request/response or event | <service> | <idempotency, pagination> |

## Compatibility policy

- Backward compatible changes: <what is allowed>
- Breaking changes: <major bump, deprecation window, migration guide>
- Unknown fields: <ignore / reject>

## Errors

| Condition | Status / error code | Retry? | Caller action |
|---|---|---|---|
| <condition> | <code> | yes/no | <action> |

## Requirements

### REQ-CON-001: <testable statement>

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
