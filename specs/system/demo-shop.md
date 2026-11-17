---
id: demo-shop
kind: system
title: "Demo Shop"
summary: "A small commerce system used to exercise the spec graph."
version: 0.1.0
status: draft
owner: "platform"
domain: ""
level: "L0"
created: 2026-11-17
updated: 2026-11-17
tags: [demo]
links:
  - rel: relates-to
    target: place-order
  - rel: constrained-by
    target: security-baseline
---

# Demo Shop

> Fixture system for `specd`. Replace it with the real system when you start.

## Context

A customer places an order and pays for it. The system is deliberately small: two
services, two contracts, one flow. It exists to exercise the spec graph and the
agent workflow, not to model a real shop.

## Goals

- A customer can place an order and receive a confirmed order id.
- Payment authorization is attempted before the order is confirmed.
- Every important behaviour is traceable to a stable requirement id.

## Non-goals

- Inventory reservation.
- A real payment provider integration.
- Customer accounts, refunds, and fulfilment.

## Actors

- Customer: places an order and expects a clear success or failure result.
- Operator: investigates failed payments and stuck orders.

## Domains

- `commerce` — order lifecycle and payment authorization.

## System requirements

### REQ-SYS-001: Place an order end to end

- **Priority:** must
- **Normative:** true
- **Given:** a customer with a non-empty cart
- **When:** the customer submits the cart to the checkout flow
- **Then:** the order is either confirmed with a payment authorization or rejected with a reason, and no partial order is left behind

### REQ-SYS-002: Every failure is observable

- **Priority:** should
- **Normative:** true
- **Given:** any failed checkout
- **When:** the failure is returned to the customer
- **Then:** the flow emits a trace with the order id, the failing step, and the reason

## Constraints

- `security-baseline` applies to every service.
- `latency-budget` applies to the synchronous checkout path.

## Decisions

- Payment authorization is synchronous for the first version. See `adr-001-sync-payment`.

## Open Questions

- [ ] Should a failed authorization retry automatically, or require a new checkout?
