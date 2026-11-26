# Framework fixtures

These are **not user specs**. They are conformance cases for the specd seed
itself. They exist so a change to the framework cannot silently break the rules it
asks every project to follow.

Run them with:

```bash
node scripts/framework-check.mjs
```

No dependencies. `node --version` should be 20 or newer; the checker uses only
`node:fs`, `node:path`, `node:crypto`, and `node:url`.

## Cases

| Case | Expect | What it locks |
|---|---|---|
| `valid-poc` | pass | A complete POC spec with a marker-delimited validation block and a matching `validated_sha` |
| `missing-source` | block | A requirement without `Source` |
| `missing-context` | block | A missing required `## Context` section |
| `open-question` | block | An unchecked item under `## Open Questions` |
| `open-conflict` | block | A `## Conflicts` row with `Resolution: open` |
| `validation-tamper` | block | Content appended after `<!-- END VALIDATION -->`; the hash must change |
| `approved-tamper` | block | An approved baseline whose `approved_sha` does not match its content |
| `valid-change` | pass | An approved target, `base_sha`, `proposal_sha`, `## Test Strategy`, `## Proposal validation`, and `## Review` |
| `change-tamper` | block | A proposed body edited without updating `proposal_sha` |
| `change-missing-review` | block | A change with no recorded review |
| `service-no-contract` | block | A service with no contract edge |
| `current-example` | pass | The shipped POC example stays conformant |
| `wrappers` | pass | Wrapper/brief links and the tool permissions the review fixes require |

The manifest at [`manifest.json`](manifest.json) is the source of truth for the
expected outcome. A block case must produce exactly the listed codes, so an
unrelated fixture bug shows up as a failure.

## Hashes

The checker uses the same canonical definition as `SPEC.md` §9:

- remove the marker-delimited validation block;
- remove the three `validated_*` lines and the `approved_sha` line;
- hash the rest.

```bash
node scripts/framework-check.mjs --hash fixtures/cases/valid-poc/specs/system/demo.md
node scripts/framework-check.mjs --proposal-hash fixtures/cases/valid-change/changes/CHG-20261127-001-demo.md
```

The documented `awk` commands must produce the same result. If you edit a fixture,
recompute its stored hash. A hash mismatch is a failing case, not a warning.

## What this is not

This is not the `spec-validator`, and it does not replace
`checklists/validate.md`. It checks the mechanical rules those fixtures exercise:
front-matter shape, ids, links, open conflicts, the validation block and hash
boundary, and the change review records. Semantic checks, evidence quality, and
judgement stay with the agent and the checklists.

Keep the fixture graph small. Add a case only when a framework rule has no coverage
and the rule is mechanical enough to check.
