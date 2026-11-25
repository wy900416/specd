---
mode: 'agent'
description: 'Validate a specd spec with checklists/validate.md and set status: validated on pass.'
---

Validate this spec:

${input:spec}

Follow `agents/spec-validator.md` and `.agents/skills/spec-validate/SKILL.md`.

1. Read the spec, its `## Source`, and every repository path it cites.
2. Apply every check in `checklists/validate.md`.
3. Write `## Validation` with a result per check and findings with
   `file:line`.
4. On pass: set `status: validated`, `validated_by: "agent:spec-validator"`,
   `validated_at`, and `validated_sha` (the canonical hash from `SPEC.md` §9).
5. On block: set `Result: blocked`, keep `status: draft`, and clear the
   `validated_*` fields. List the exact fixes needed.

Do not edit requirements, assumptions, decisions, or source text. Do not approve,
release, or bump a version.
