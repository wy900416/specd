---
id: security-baseline
kind: standard
title: "Security Baseline"
summary: "Non-negotiable authentication and secret-handling rules for services."
version: 1.0.0
status: approved
owner: "security"
domain: ""
level: ""
pinned: true
applies_to: [service]
created: 2026-11-17
updated: 2026-11-17
tags: [security, baseline]
links: []
approved_by: "platform"
approved_at: 2026-11-17T00:00:00Z
---

# Security Baseline

This standard is pinned: every matching agent context receives it before any other
content, and it is never truncated by the context budget.

## Scope

Applies to every `service` spec in this system.

## Rules

### REQ-SEC-001: Authenticate service-to-service calls

- **Priority:** must
- **Normative:** true
- **Given:** a call from one service to another
- **When:** the caller has no valid workload identity
- **Then:** the callee rejects the call before reading the request body

### REQ-SEC-002: Keep credentials out of specs and examples

- **Priority:** must
- **Normative:** true
- **Given:** a spec or example that needs a credential
- **When:** the document is written or reviewed
- **Then:** it contains a placeholder reference, never a live value

## Verification

- `specd scan --strict` in CI for specs and proposals.
- A policy check in the service pipeline for workload identity.
- Review checklist item for credential placeholders.

## Exceptions

Exceptions require a written approval from the security owner and an expiry date
recorded in the service spec.
