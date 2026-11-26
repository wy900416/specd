---
applyTo: 'specs/**/*.md'
---

# Editing a spec

- Keep the YAML front-matter closed and valid. Required: `id`, `kind`, `title`,
  `version`, `status`, `owner`.
- In `stage: poc`, `version` MUST stay `0.1.0`. Do not bump it.
- Never write `status: validated` or the `validated_*` fields by hand. Only the
  `spec-validator` agent sets them, and only on a passing run.
- Never write `status: approved`, `approved_by`, `approved_at`, or `approved_sha`
  by hand. A human promotion or release sets them.
- Any semantic edit by a writer, gap-filler, or human MUST set `status: draft` and
  clear `validated_by`, `validated_at`, and `validated_sha`. The validator's own
  validation update is the exception.
- Every requirement keeps its stable `REQ-<PREFIX>-<NNN>` id and a
  `- **Source:** ...` line. New ids are never reused.
- Put guessed product facts in `## Assumptions`; put implementation choices in
  `## Agent Decisions`. Both need a basis and a revisit trigger.
- High-risk POC assumptions use `Risk: high`, `Confirmed: agent (POC)`, and
  `Revisit: before production`. A fact the user reserved uses
  `Confirmed: needs-human` and blocks validation.
- Do not delete `## Source` or rewrite it. Append a dated entry instead.
- Do not add credentials, private addresses, active HTML, or placeholders
  (`TODO`, `TBD`) to a validated spec.
