---
mode: 'agent'
description: 'Create a specd spec from a description, fill the gaps, and validate it.'
---

Create a spec from this description:

${input:description}

Follow `AGENTS.md`, `SPEC.md`, and `.agents/skills/spec-draft/SKILL.md`.

1. Profile the repository (manifests, `README*`, `.github/`, `.agents/skills/`,
   existing `specs/`) and, if accessible, the user's global skills. Read-only.
2. Write `specs/system/<slug>.md` from `templates/system.md` with
   `status: draft`, `stage: poc`, `version: 0.1.0`.
3. Put the description verbatim in `## Source`. Write the requirements that trace
   to it with `Source: user`.
4. Write `## Goals` with `GOAL-` ids and a draft `## Acceptance` mapped to a goal
   or `REQ-`. Acceptance is what the user will try, not a test result.
5. Run the gap-fill procedure (`.agents/skills/spec-gap-fill/SKILL.md`): infer
   aggressively, record assumptions, surface conflicts.
6. Validate in a **separate** `spec-validator` run: invoke the agent with only the
   spec path and `checklists/validate.md`. Do not pass your draft summary. If the
   runner cannot spawn a subagent, stop and tell the user to run
   `/validate-spec` in a fresh session, or give a fresh agent only the spec path
   and `checklists/validate.md`.
7. If validation blocks, fix the blocking findings and re-run the validator once.
   Do not fake a pass.
8. Report: spec path, 3-5 key requirements, goals and acceptance criteria,
   assumptions, fenced high-risk facts, validation result. Do not ask for approval.
