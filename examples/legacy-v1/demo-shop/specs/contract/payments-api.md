---
id: payments-api
kind: contract
title: "Payments API"
summary: "HTTP contract exposed by the payments service for authorization."
version: 0.1.0
status: draft
owner: "payments-team"
domain: ""
level: "L2"
type: openapi
path: payments.openapi.yaml
created: 2026-11-17
updated: 2026-11-17
tags: [demo]
links:
  - rel: part-of
    target: payments
---

# Payments API

## Type and location

- type: `openapi`
- path: `payments.openapi.yaml`

## Purpose

`orders` asks `payments` to authorize a payment. The contract is internal to the
demo system and is not exposed to end clients.

## Operations or messages

| Name | Kind | Caller | Notes |
|---|---|---|---|
| `authorizePayment` | request/response | orders | returns `authorized`, `declined`, or `unknown` |

## Compatibility policy

- Backward compatible: adding result fields.
- Breaking: adding a new required result state without a migration plan.
- Breaking changes require a major bump and an update to the `orders` consumer.

## Errors

| Condition | Status / error code | Retry? | Caller action |
|---|---|---|---|
| provider timeout | 503 `unknown` | yes | reconcile later |
| declined | 200 `declined` | no | reject the order |

## Requirements

### REQ-PAPI-001: Authorization is idempotent per order

- **Priority:** must
- **Normative:** true
- **Given:** an authorization request for order `O`
- **When:** the caller retries the same request
- **Then:** the service returns the original authorization id and does not charge twice

## Open Questions

- [ ] Is `unknown` a terminal state for the order, or does it always reconcile?
