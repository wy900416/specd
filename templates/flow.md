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

## Open Questions

- [ ] <question>
