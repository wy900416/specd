---
mode: 'agent'
description: 'Validate a spec with checklists/validate.md, or a mature proposal with mature/checklists/validate-proposal.md.'
---

Validate this spec or change:

${input:spec}

Follow `agents/spec-validator.md` and `.agents/skills/spec-validate/SKILL.md`.

1. Read the target and, for a mature change, the `CHG` and its proposed body.
2. Apply every check in `checklists/validate.md` for a bootstrap spec, or
   `mature/checklists/validate-proposal.md` for a mature change. Record findings with
   `file:line`.
3. Write the result:
   - bootstrap: a marker-delimited `## Validation` block in the spec;
   - mature change: `## Proposal validation` in the CHG.
4. Bootstrap pass: set `status: validated`, `validated_by:
   "agent:spec-validator"`, `validated_at`, and `validated_sha` (the canonical
   hash from `SPEC.md` §9). Bootstrap block: `Result: blocked`, keep
   `status: draft`, clear `validated_*`, and list the exact fixes.
5. Mature change: record `base_sha`, `proposal_sha`, and `Result` in the CHG. Do
   not edit the target and do not set it to `status: validated`.

Do not edit requirements, assumptions, decisions, or source text. Do not approve,
release, or bump a version.
