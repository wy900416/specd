---
name: spec-review
description: "Mature-stage review of a spec or change proposal: cross-service consistency, impact, and version hygiene. Not the POC validation gate."
whenToUse: "A spec is being promoted to mature stage, a contract change needs cross-service impact review, or a change proposal is about to be released."
---

# Spec review

Use this at **mature stage**, when a spec is no longer a POC hypothesis. For the
POC gate, use `spec-validate` instead. Review the **graph**, not just the file: a
spec can be well written and still contradict a contract, miss a pinned standard,
or bump the wrong version.

## Read first

- `SPEC.md` — the normative rules.
- `checklists/validate.md` — the mechanical checks.
- `mature/checklists/change.md` — the mature change gate.
- `mature/checklists/review.md` — the judgement checks, severity, and bump guide.
- `mature/docs/change-mode.md` — evolution, approval tiers, proposals, and release.

## Procedure

1. **Apply `mature/checklists/validate-proposal.md`** to the effective spec (target
   front-matter, `spec` overrides, and the proposed body). Record every finding
   with a file and line. Confirm `base_sha` and `proposal_sha`.
2. **Apply `mature/checklists/change.md` and `mature/checklists/review.md`.** Focus on impact,
   compatibility, contract, data, NFR, traceability, security, approvals, rollout,
   and versioning.
3. **Check the proposal.** Compare the target body with the proposed body between
   the markers. The proposal is a full replacement body, not a diff.
4. **Scan impact.** Search every `specs/**/*.md` for links whose `target` is the
   id; list the direct consumers and separate them from transitive noise. Check
   the `CHG`'s impact against the graph.
5. **Check the approval tier.** Owner for patch/minor, consumers for major,
   security/data for high risk. A missing sign-off blocks release.
6. **Check version hygiene.** `none` for editorial, `patch` for clarification,
   `minor` for additive, `major` for breaking. If the diff and the bump disagree,
   say so.
7. **Write the review packet** into the CHG's `## Review` section, in the format
   from `mature/checklists/review.md`.

## Output

```md
## Review
- target: <id>@<version> (<status>)
- change: <CHG id or "promotion">
- validation: <errors>, <warnings>
- blocking findings <n>
- non-blocking findings <n>
- impact: <direct consumers and affected versions>
- compatibility: backward | additive | breaking
- risk: low | medium | high
- approvals: owner / consumers / security-data
- rollout: direct | flag | canary; rollback: <yes/no>
- recommended bump: none | patch | minor | major
- open questions: <list>
- recommendation: ready to release | revise | reject
```

Order findings by severity, then by spec id. Every finding cites
`id@version#REQ-ID` or a file and line. Do not restate the whole spec.

## Rules

- Never edit an approved spec or its proposal. Report findings.
- Never approve or release. Recommend, then stop.
- A passing checklist is not an approval: report what the checklist cannot see
  (ambiguity, missing failure modes, unowned requirement).
- If the change touches a contract, check the consumers before commenting on
  style.
- Do not accept a `major` change without consumer sign-off and a migration.
- If validation and review disagree, trust the evidence, not the score.
