---
id: place-order
kind: flow
title: "Place Order"
summary: "End-to-end checkout across orders and payments."
version: 0.1.0
status: draft
owner: "platform"
domain: commerce
level: "L2"
created: 2026-11-17
updated: 2026-11-17
tags: [demo]
links:
  - rel: part-of
    target: orders
  - rel: part-of
    target: payments
---

# Place Order

## Trigger

A customer submits the cart to `POST /orders`.

## Participants

- `orders` — creates the order and owns its state.
- `payments` — authorizes the payment.

## Happy path

1. `orders` validates the cart and persists an order in `pending`.
2. `orders` calls `payments` with the order id and amount.
3. `payments` authorizes and returns `authorized`.
4. `orders` persists `confirmed` and returns the order id.

## Failure and compensation

| Failure | Detection | Compensation | User-visible result |
|---|---|---|---|
| payment declined | `declined` result | order -> `rejected` | 402 with reason |
| payment timeout | `unknown` result | order stays `pending`; reconcile | 503, retryable |
| orders write fails | database error | no payment call | 500, no order |

## Observability

- trace span: `checkout.place_order`
- key attributes: `order.id`, `payment.authorization_id`
- alert: pending orders older than 15 minutes

## Requirements

### REQ-FLOW-001: No confirmed order without an authorization

- **Priority:** must
- **Normative:** true
- **Given:** a checkout request
- **When:** the payment result is declined or unknown
- **Then:** the order is not confirmed and the caller receives a retryable or terminal reason

### REQ-FLOW-002: A timeout leaves a reconcilable order

- **Priority:** must
- **Normative:** true
- **Given:** `payments` times out
- **When:** the checkout returns
- **Then:** the order remains `pending` and appears in the reconciliation queue

## Open Questions

- [ ] Should checkout be asynchronous for large carts?
