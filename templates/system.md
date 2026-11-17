---
id: {{id}}
kind: {{kind}}
title: "{{title}}"
summary: "{{summary}}"
version: {{version}}
status: draft
owner: "{{owner}}"
domain: ""
level: "{{level}}"
created: {{date}}
updated: {{date}}
tags: []
links: []
---

# {{title}}

> Draft. An agent may fill this file; only a human sets `status: approved`, and
> only a human release step changes `version`. Replace `REQ-SYS-001` with this
> spec's own prefix and keep ids stable.

## Context

What problem does this system solve, for whom, and why now? State the boundary:
what is inside this system and what is explicitly outside it.

## Goals

- <measurable outcome>

## Non-goals

- <what this system deliberately does not do>

## Actors

- <actor>: <what they need>

## Domains

List the bounded contexts. Create or link one `domain` spec per context.

- `commerce` — <one-line responsibility>

## System requirements

### REQ-SYS-001: <testable statement>

- **Priority:** must
- **Normative:** true
- **Given:** <precondition>
- **When:** <action>
- **Then:** <observable outcome>

## Constraints

Link system-level NFRs and standards with `constrained-by`.

## Decisions

Link ADRs with `decided-by`.

## Open Questions

- [ ] <question that must be answered before approval>
