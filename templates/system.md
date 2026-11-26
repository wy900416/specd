---
id: {{id}}
kind: system
title: "{{title}}"
summary: "{{summary}}"
version: 0.1.0
status: draft
stage: poc
owner: "{{owner}}"
domain: ""
level: L1
created: {{date}}
updated: {{date}}
tags: [poc]
decision_mode: agent-assisted
source: chat
validated_by: ""
validated_at: ""
validated_sha: ""
approved_by: ""
approved_at: ""
approved_sha: ""
conflicts_with: []
links: []
---

# {{title}}

> Draft hypothesis. The writer fills what the user said; the gap-filler fills the
> rest; only the validator sets `validated`. Version stays `0.1.0` in the POC
> stage. Keep `REQ-SYS-001` as this spec's prefix and keep ids stable.

## Source

> <the user's description, verbatim, with a date>

## Repo Profile

| Area | Finding | Evidence |
|---|---|---|
| Language | | `repo:<path>:<line>` |
| Framework | | `repo:<path>:<line>` |
| Tests | | `repo:<path>:<line>` |
| Conventions | | `repo:<path>:<line>` |
| Global skills | | `global-skill:<name>` or "not accessible" |

## Context

What problem does this system solve, for whom, and why now? State the boundary:
what is inside and what is explicitly outside.

## Goals

- <measurable outcome>

## Non-goals

- <what this system deliberately does not do>

## Actors

- <actor>: <what they need>

## Requirements

### REQ-SYS-001: <testable statement>

- **Priority:** must
- **Normative:** true
- **Source:** user
- **Given:** <precondition>
- **When:** <action>
- **Then:** <observable outcome>

## Assumptions

<!-- The gap-filler fills this. A product guess needs a basis, a risk, and a revisit trigger.
     High-risk POC facts: Confirmed: agent (POC), Revisit: before production.
     A fact the user reserved: Confirmed: needs-human. -->

| # | Assumption | Basis | Risk | Confirmed | Revisit |
|---|---|---|---|---|---|
| | | | | | |

## Agent Decisions

<!-- The gap-filler fills this. One implementation choice per row. -->

| # | Question | Chosen | Why | Alternatives | Reversible | Revisit after |
|---|---|---|---|---|---|---|
| | | | | | | |

## Open Questions

- [ ] <question that blocks validation, with an owner>

## Conflicts

<!-- Conflicts with existing specs go here. The user resolves them. -->

| # | Other spec | Conflict | Options | Resolution |
|---|---|---|---|---|
| | | | | |

<!-- BEGIN VALIDATION -->
## Validation

<!-- The validator replaces this block. Keep END as the last line of the file.
     The canonical hash excludes everything between the two markers. -->
- Not run yet. The validator writes this section.
<!-- END VALIDATION -->
