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
applies_to: []
created: {{date}}
updated: {{date}}
tags: []
links: []
---

# {{title}}

> Draft. An NFR is a constraint, not a feature. State who it applies to, how it is
> measured, and what happens when the budget is exhausted.

## Applies to

- kinds: `service`, `contract`
- tags: <optional>

## Requirement

### REQ-NFR-001: <measurable statement>

- **Priority:** must
- **Normative:** true
- **Given:** <load / condition>
- **When:** <period or operation>
- **Then:** <threshold and measurement window>

## Measurement

- signal: <metric / log / trace / audit>
- query: <how to compute it>
- window: <e.g. 30 days>
- threshold: <e.g. p95 < 300 ms>

## Budget and response

What happens when the budget is exhausted? Who is notified? What is degraded first?

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
