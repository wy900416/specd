---
id: demo
kind: system
title: "Demo"
summary: "A fixture spec used by the framework self-check."
version: 0.1.0
status: draft
stage: poc
owner: "platform"
domain: ""
level: "L1"
created: 2026-11-27
updated: 2026-11-27
tags: [fixture]
decision_mode: agent-assisted
source: chat
validated_by: ""
validated_at: ""
validated_sha: ""
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

