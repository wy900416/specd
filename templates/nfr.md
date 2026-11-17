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

## Open Questions

- [ ] <question>
