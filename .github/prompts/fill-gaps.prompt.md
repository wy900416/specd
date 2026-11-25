---
mode: 'agent'
description: 'Fill gaps in an existing specd spec: repo profile, inference, assumptions, conflicts.'
---

Fill gaps in this spec:

${input:spec}

Follow `agents/gap-filler.md` and `.agents/skills/spec-gap-fill/SKILL.md`.

1. Read the spec and its `## Source`.
2. Verify or rebuild `## Repo Profile` with `repo:<path>:<line>` evidence.
3. Read the user's global skills if accessible; cite `global-skill:<name>`.
4. Infer stack, naming, structure, defaults, and POC simplifications.
5. Record product guesses in `## Assumptions` and implementation choices in
   `## Agent Decisions`. Every row needs a basis, a risk, and a revisit trigger.
6. Fence high-risk facts: `Risk: high`, `Confirmed: agent (POC)`,
   `Revisit: before production`, fake data, no real users, money, or PII. A
   user-reserved fact is `Confirmed: needs-human` and blocks.
7. Scan every other spec for conflicts; write `## Conflicts`.
8. Hand off to `spec-validator`. Do not ask for approval.
