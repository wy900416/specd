---
id: commerce
kind: domain
title: "Commerce"
summary: "Order lifecycle and payment authorization for the demo shop."
version: 0.1.0
status: draft
owner: "platform"
domain: commerce
level: "L1"
created: 2026-11-17
updated: 2026-11-17
tags: [demo]
links:
  - rel: part-of
    target: demo-shop
---

# Commerce

## Purpose

Owns the order lifecycle and the decision to authorize payment. It does not own
the payment provider relationship beyond the authorization call.

## Ubiquitous language

| Term | Meaning | Not to be confused with |
|---|---|---|
| Order | A customer's intent to buy, with a stable id | Cart |
| Authorization | A hold placed on a payment method | Capture |
| Confirmed order | An order whose payment was authorized | Paid order |

## Responsibilities

- Decide whether an order can be created.
- Own the order state machine.
- Request payment authorization and record the outcome.

## Services

- `orders` — order lifecycle.
- `payments` — payment authorization.

## Invariants

- An order never moves from `rejected` back to `confirmed`.
- A confirmed order always has exactly one successful authorization.

## Requirements

### REQ-COM-001: Order state transitions are explicit

- **Priority:** must
- **Normative:** true
- **Given:** an order in state `pending`
- **When:** authorization succeeds
- **Then:** the order moves to `confirmed` and the transition is recorded once

## Open Questions

- [ ] Is a partially authorized order a valid state, or always a failure?
