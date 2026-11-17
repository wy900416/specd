---
id: orders-api
kind: contract
title: "Orders API"
summary: "HTTP contract exposed by the orders service for checkout clients."
version: 0.1.0
status: draft
owner: "orders-team"
domain: ""
level: "L2"
type: openapi
path: orders.openapi.yaml
created: 2026-11-17
updated: 2026-11-17
tags: [demo]
links:
  - rel: part-of
    target: orders
---

# Orders API

## Type and location

- type: `openapi`
- path: `orders.openapi.yaml`

## Purpose

The checkout client creates an order. The wire format is defined by the OpenAPI
document; this spec owns the intent and the compatibility policy.

## Operations or messages

| Name | Kind | Caller | Notes |
|---|---|---|---|
| `createOrder` | request/response | checkout client | idempotent on `Idempotency-Key` |

## Compatibility policy

- Backward compatible: adding optional fields, adding new endpoints.
- Breaking: removing fields, changing types, making optional fields required.
- Breaking changes require a major bump, a deprecation window, and a migration guide.

## Errors

| Condition | Status / error code | Retry? | Caller action |
|---|---|---|---|
| duplicate key | 200 with the original order | no | reuse the returned order id |
| payment declined | 402 `payment_declined` | no | show the reason, start a new checkout |
| payment unknown | 503 `payment_unknown` | yes | retry with the same key |

## Requirements

### REQ-OAPI-001: A duplicate create returns the original order

- **Priority:** must
- **Normative:** true
- **Given:** an order was created with key `K`
- **When:** the client posts the same key `K` again
- **Then:** the response is 200 and carries the original order id

## Open Questions

- [ ] Should the error envelope be shared with `payments-api`?
