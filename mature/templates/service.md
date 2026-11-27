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

## Conflicts

| # | Other spec | Conflict | Options | Resolution |
|---|---|---|---|---|
| | | | | |


## Agent Decisions

<!-- One row per decision. Leave the table empty if there are none. -->
| # | Question | Chosen | Why | Alternatives | Reversible | Revisit after |
|---|---|---|---|---|---|---|
| | | | | | | |

## Open Questions

- [ ] <question>

<!-- BEGIN VALIDATION -->
## Validation

<!-- The validator replaces this block. Keep END as the last line of the file.
     The canonical hash excludes everything between the two markers. -->
- Not run yet. The validator writes this section.
<!-- END VALIDATION -->
