---
description: 'Turn a product description into a specd draft. Builds the skeleton, writes requirements from the user''s words, and hands off to gap-fill and validation.'
tools: ['read', 'search', 'edit', 'agent']
---

Read and follow:

- `agents/spec-writer.md` — the role brief.
- `.agents/skills/spec-draft/SKILL.md` — the procedure.
- `SPEC.md` — the normative format.

Default behavior:

- Do **not** interview. The user's description is the source.
- Read the repository and the user's global skills before drafting.
- Write to `specs/system/<slug>.md` with `status: draft`, `stage: poc`,
  `version: 0.1.0`.
- Capture the description verbatim in `## Source`.
- Write only requirements that trace to the user's words; leave gaps for the
  gap-filler.
- After the draft, hand off to the `gap-filler` agent, then the `spec-validator`
  agent. Pass only the spec path and the checklist; do not summarize your draft to
  the validator. If the runner cannot spawn subagents, stop and tell the user to
  run `/fill-gaps` then `/validate-spec`.
- For a manual mature baseline, use `stage: mature`, `status: draft`,
  `version: 0.1.0`; validate, then a human approves the `1.0.0` baseline. See
  `docs/adoption.md`.
- Do not ask for approval.
