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

## Open Questions

- [ ] <question>
