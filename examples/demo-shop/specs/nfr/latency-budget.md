---
id: latency-budget
kind: nfr
title: "Checkout Latency Budget"
summary: "The synchronous checkout path must stay within its latency budget."
version: 0.1.0
status: draft
owner: "platform"
domain: ""
level: ""
applies_to: [service, flow]
created: 2026-11-17
updated: 2026-11-17
tags: [performance, slo]
links: []
---

# Checkout Latency Budget

## Applies to

- kinds: `service`, `flow`
- tags: `checkout`

## Requirement

### REQ-NFR-001: Checkout p95 stays under 300 ms

- **Priority:** must
- **Normative:** true
- **Given:** normal production load
- **When:** measured over a rolling 30-day window
- **Then:** the p95 latency of `POST /orders` is below 300 ms

## Measurement

- signal: HTTP server latency metric for `POST /orders`
- query: histogram quantile over the checkout route
- window: 30 days
- threshold: p95 < 300 ms

## Budget and response

When the budget is exhausted, checkout is degraded before other endpoints: the
service sheds non-essential enrichment and alerts the platform owner.

## Open Questions

- [ ] Is the budget per service or for the whole `place-order` flow?
