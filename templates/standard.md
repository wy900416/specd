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
pinned: false
applies_to: []
created: {{date}}
updated: {{date}}
tags: []
links: []
---

# {{title}}

> Draft. A standard is a cross-cutting rule. Set `pinned: true` only when every
> matching agent context must receive it; pinned standards are injected first and
> are never truncated by the context budget.

## Scope

- applies to: `service`, `contract`
- tags: <optional>

## Rules

### REQ-STD-001: <rule that can be checked>

- **Priority:** must
- **Normative:** true
- **Given:** <context>
- **When:** <situation>
- **Then:** <required behaviour>

## Verification

How is compliance checked? Test, static analysis, policy engine, review checklist,
or runtime monitor. Name the check, not just the intention.

## Exceptions

Who can grant an exception, for how long, and where is it recorded?

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
