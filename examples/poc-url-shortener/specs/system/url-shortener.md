---
id: url-shortener
kind: system
title: "URL Shortener"
summary: "Short links for a small internal team, expiring after 30 days."
version: 0.1.0
status: draft
stage: poc
owner: "platform"
domain: ""
level: "L0"
created: 2026-11-27
updated: 2026-11-27
tags: [poc, example]
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

# URL Shortener

## Source

> 2026-11-27: Build a URL shortener for a small internal team. Links expire after
> 30 days, and I want a simple web page plus an API.

## Repo Profile

| Area | Finding | Evidence |
|---|---|---|
| Repository | new project; no stack chosen yet | not applicable |
| Global skills | not accessible in this example | not applicable |

## Context

A small internal team needs short links that stop resolving after 30 days. The
boundary is one web page and one HTTP API; public multi-tenant hosting and custom
domains are outside it.

## Goals

- A team member can shorten a URL and resolve it until it expires.

## Non-goals

- Public signup, custom domains, and analytics.

## Actors

- Team member: creates and follows short links.

## Requirements

### REQ-SYS-001: Shorten a valid URL

- **Priority:** must
- **Normative:** true
- **Source:** user
- **Given:** a team member submits an absolute `http` or `https` URL
- **When:** they call the shorten endpoint
- **Then:** the response contains a short code that resolves to the same URL

### REQ-SYS-002: Expire a short link

- **Priority:** must
- **Normative:** true
- **Source:** user
- **Given:** a short link created more than 30 days ago
- **When:** it is resolved
- **Then:** the resolver returns 410 and does not redirect

## Assumptions

| # | Assumption | Basis | Risk | Confirmed | Revisit |
|---|---|---|---|---|---|
| 1 | Links are internal-only | no public sharing in the source | medium | no | first feedback |
| 2 | Authentication uses the company SSO | company convention | high | agent (POC) | before production |

## Agent Decisions

| # | Question | Chosen | Why | Alternatives | Reversible | Revisit after |
|---|---|---|---|---|---|---|
| 1 | Code generation | random base62 | simple and enough collision space | hash of URL | yes | 10k links |
| 2 | Storage | in-memory map | smallest POC | database | yes | first restart test |

## Open Questions

- None.

## Conflicts

| # | Other spec | Conflict | Options | Resolution |
|---|---|---|---|---|

<!-- BEGIN VALIDATION -->
## Validation

<!-- The validator replaces this block. Keep END as the last line of the file.
     The canonical hash excludes everything between the two markers. -->
- Not run yet. The validator writes this section.
<!-- END VALIDATION -->
