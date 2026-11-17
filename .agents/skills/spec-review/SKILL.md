---
name: spec-review
description: "Review a spec or change proposal for completeness, consistency, impact, and version hygiene before approval or release."
whenToUse: "A draft is about to be approved, a proposal is about to be released, or a contract change needs cross-service impact review."
---

# Spec review

Review the **graph**, not just the file. A spec can be well written and still be
wrong: it can contradict a contract, miss a pinned standard, or bump the wrong
version.

## Procedure

1. Run the deterministic gates:
   ```bash
   ./specd.sh validate
   ./specd.sh fitness
   ./specd.sh scan --strict
   ```
2. For a proposal, read `./specd.sh diff <proposal>` and check that the body diff
   matches the stated summary.
3. For a contract change, run `./specd.sh impact <contract-id>` and list the
   consumers whose behaviour or version is affected.
4. Check the cross-spec questions:
   - Does every normative requirement have Given/When/Then?
   - Does every service implement exactly one domain, expose a contract, and link
     the standards that apply to it?
   - Does every flow reference at least two services and own the compensation?
   - Does every NFR declare `applies_to` and a measurement?
   - Are there approved specs with open questions?
   - Is a pinned standard still approved?
5. Check version hygiene:
   - `none` — editorial only, no semantic change.
   - `patch` — clarification that does not change behaviour.
   - `minor` — additive behaviour or contract field.
   - `major` — breaking contract or behaviour change.
   If the bump and the diff disagree, say so.
6. Produce a review packet.

## Review packet

```md
## Review
- target: <id>@<version> (<status>)
- gates: validate=<pass/fail>, fitness=<pass/fail>, scan=<pass/fail>
- blocking findings <n>
- non-blocking findings <n>
- impact: <consumers and affected versions>
- recommended bump: none | patch | minor | major
- open questions: <list>
- recommendation: approve | revise | reject
```

Order findings by severity, then by spec id. Every finding cites
`spec-id@version#REQ-ID` or a file path and line. Do not restate the whole spec.

## Rules

- Never edit a published spec. If a change is needed, create a proposal.
- Never approve or release. Recommend, then stop.
- A passing lint is not an approval: report what the gates cannot see
  (ambiguity, missing failure modes, unowned requirement).
- If the diff changes a contract, check the consumers before commenting on style.

The full rubric, severity definitions, and bump examples are in
`references/review-rubric.md`.
