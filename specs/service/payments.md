---
id: payments
kind: service
title: "Payments Service"
summary: "Authorizes payments and records the authorization outcome."
version: 0.1.0
status: draft
owner: "payments-team"
domain: commerce
level: "L2"
created: 2026-11-17
updated: 2026-11-17
tags: [demo]
links:
  - rel: implements
    target: commerce
  - rel: exposes
    target: payments-api
  - rel: constrained-by
    target: security-baseline
  - rel: constrained-by
    target: latency-budget
---

# Payments Service

## Responsibility

Authorizes a payment for an order and records the authorization result. It never
stores raw card data; the provider returns an opaque reference.

## Data ownership

- `authorization`: only this service writes it.
- `provider_reference`: owned by this service, never exposed in logs.

## Interfaces

- Exposes `payments-api` for `orders`.
- Calls the external payment provider through an adapter.

## Dependencies

- External payment provider — synchronous, with a strict timeout.

## Behaviour and failure modes

- Authorize -> call provider -> persist the result -> return the authorization id.
- Provider timeout returns `unknown`, not `declined`; the caller must reconcile.
- A declined authorization is final for that attempt; a retry needs a new key.

## Requirements

### REQ-PAY-001: Distinguish decline from unknown

- **Priority:** must
- **Normative:** true
- **Given:** a payment authorization request
- **When:** the provider times out
- **Then:** the service returns `unknown` and does not record a decline

## Constraints

- `security-baseline` and `latency-budget` apply to this service.

## Open Questions

- [ ] How long should an `unknown` authorization be reconciled before it expires?
