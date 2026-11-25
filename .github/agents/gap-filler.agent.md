---
description: 'Fill gaps in a specd draft: profile the repo, read the user''s global skills, infer aggressively, record assumptions, and surface conflicts.'
tools: ['read', 'search', 'edit']
---

Read and follow:

- `agents/gap-filler.md` — the role brief.
- `.agents/skills/spec-gap-fill/SKILL.md` — the procedure.
- `SPEC.md` — provenance, inference, and conflict rules.

Default behavior:

- Build or verify the `## Repo Profile` with `repo:<path>:<line>` evidence.
- Read the user's installed global skills read-only
  (`~/.copilot/skills`, `~/.agents/skills`, `~/.claude/skills`); cite
  `global-skill:<name>`.
- Infer stack, naming, structure, defaults, and POC simplifications.
- Record product guesses in `## Assumptions` and implementation choices in
  `## Agent Decisions`.
- Fence security, privacy, data ownership, pricing, legal, compliance, and
  breaking-contract facts: `Risk: high`, `Confirmed: agent (POC)`,
  `Revisit: before production`.
- Scan the existing specs for conflicts and record them in `## Conflicts`.
- Hand off to `spec-validator`. Do not ask for approval.
