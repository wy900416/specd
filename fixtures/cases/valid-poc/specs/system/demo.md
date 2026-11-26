---
id: demo
kind: system
title: "Demo"
summary: "A fixture spec used by the framework self-check."
version: 0.1.0
status: validated
stage: poc
owner: "platform"
domain: ""
level: "L1"
created: 2026-11-27
updated: 2026-11-27
tags: [fixture]
decision_mode: agent-assisted
source: chat
validated_by: "agent:spec-validator"
validated_at: "2026-11-27T10:00:00+08:00"
validated_sha: "145c6bb27a25e9fddb98afc26bcc6395fefa38e993bf6a4fc2e03f48cd36ca3b"
approved_by: ""
approved_at: ""
approved_sha: ""
conflicts_with: []
links: []
---

# Demo

## Source

> 2026-11-27: Build a URL shortener for a small internal team.

## Repo Profile

| Area | Finding | Evidence |
|---|---|---|
| Language | not applicable | fixture |

## Context

A small internal team needs short links that expire.

## Goals

- A valid URL can be shortened and resolved.

## Non-goals

- Public multi-tenant hosting.

## Actors

- Team member: creates and follows links.

## Requirements

### REQ-SYS-001: Shorten a valid URL

- **Priority:** must
- **Normative:** true
- **Source:** user
- **Given:** a team member submits an absolute `http` or `https` URL
- **When:** they call the shorten endpoint
- **Then:** the response contains a short code that resolves to the same URL

## Assumptions

| # | Assumption | Basis | Risk | Confirmed | Revisit |
|---|---|---|---|---|---|
| 1 | Links are internal-only | no public sharing in the source | medium | agent (POC) | first feedback |

## Agent Decisions

| # | Question | Chosen | Why | Alternatives | Reversible | Revisit after |
|---|---|---|---|---|---|---|
| 1 | Storage | in-memory map | simplest POC | database | yes | first feedback |

## Open Questions

- None.

## Conflicts

| # | Other spec | Conflict | Options | Resolution |
|---|---|---|---|---|

<!-- BEGIN VALIDATION -->
## Validation

- Validated by: agent:spec-validator
- At: 2026-11-27T10:00:00+08:00
- Result: pass
- Checklist: checklists/validate.md
- Hash: 145c6bb27a25e9fddb98afc26bcc6395fefa38e993bf6a4fc2e03f48cd36ca3b

| # | Check | Result | Note |
|---|---|---|---|
| 1 | Front-matter and stage | pass | |
| 2 | Source | pass | |
| 3 | Requirements | pass | |
| 4 | Provenance | pass | |
| 5 | Conflicts | pass | none |
| 6 | Links and ids | pass | |
| 7 | Repository evidence | pass | |
| 8 | Security | pass | |
| 9 | Scope | pass | |
| 10 | Freshness | pass | hash matches |
| 11 | Index | pass | absent |
| 12 | Mature stage | n/a | stage: poc |
<!-- END VALIDATION -->
