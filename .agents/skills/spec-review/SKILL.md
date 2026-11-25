---
name: spec-review
description: "Contract-stage review of a spec or change proposal: cross-service consistency, impact, and version hygiene. Not the POC validation gate."
whenToUse: "A spec is being promoted to contract stage, a contract change needs cross-service impact review, or a change proposal is about to be released."
---

# Spec review

Use this at **contract stage**, when a spec is no longer a POC hypothesis. For the
POC gate, use `spec-validate` instead. Review the **graph**, not just the file: a
spec can be well written and still contradict a contract, miss a pinned standard,
or bump the wrong version.

## Read first

- `SPEC.md` — the normative rules.
- `checklists/validate.md` — the mechanical checks.
- `checklists/review.md` — the judgement checks, severity, and bump guide.
- `docs/contract-mode.md` — promotion, proposals, and release.

## Procedure

1. **Apply `checklists/validate.md`.** Record every finding with a file and line.
   Do not summarise "looks fine".
2. **Apply `checklists/review.md`.** Focus on intent, behaviour, contract, data,
   NFR, traceability, security, versioning, and consistency.
3. **Check the diff**, for a proposal. Compare the target body with the proposal
   body side by side. The proposal is a full replacement body, not a diff.
4. **Scan impact**, for a contract or shared service. Search every
   `specs/**/*.md` for links whose `target` is the id; list the direct consumers
   and separate them from transitive noise.
5. **Check version hygiene.** `none` for editorial, `patch` for clarification,
   `minor` for additive, `major` for breaking. If the diff and the bump disagree,
   say so.
6. **Produce the review packet** in the format from `checklists/review.md`.

## Output

```md
## Review
- target: <id>@<version> (<status>)
- validation: <errors>, <warnings>
- blocking findings <n>
- non-blocking findings <n>
- impact: <direct consumers and affected versions>
- recommended bump: none | patch | minor | major
- open questions: <list>
- recommendation: approve | revise | reject
```

Order findings by severity, then by spec id. Every finding cites
`id@version#REQ-ID` or a file and line. Do not restate the whole spec.

## Rules

- Never edit an approved spec. If a change is needed, create a proposal.
- Never approve or release. Recommend, then stop.
- A passing checklist is not an approval: report what the checklist cannot see
  (ambiguity, missing failure modes, unowned requirement).
- If the change touches a contract, check the consumers before commenting on
  style.
- If validation and review disagree, trust the evidence, not the score.
