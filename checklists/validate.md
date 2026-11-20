# Validation checklist

Apply this before approving a draft. There is no linter: read the files, search the
repository, and record evidence. A finding without a file and line is not a
finding.

## 1. Front-matter

- [ ] Every `specs/**/*.md` starts with a closed YAML `---` block.
- [ ] Required fields exist: `id`, `kind`, `title`, `version`, `status`, `owner`.
- [ ] `id` is lower-kebab-case and matches the filename (`orders.md` -> `orders`).
- [ ] `kind` is one of `system`, `domain`, `service`, `contract`, `flow`, `nfr`,
      `adr`, `standard`.
- [ ] `version` is `MAJOR.MINOR.PATCH`.
- [ ] `status` is one of `draft`, `proposed`, `approved`, `deprecated`.
- [ ] `approved` has `approved_by` and `approved_at`.
- [ ] `draft` / `proposed` does not have `approved_by` or `approved_at`.
- [ ] `created` and `updated`, when present, start with `YYYY-MM-DD`.
- [ ] A contract declares `type`; an `openapi` / `asyncapi` contract declares a
      `path` that exists relative to the spec file.
- [ ] A `standard` with `pinned: true` declares `applies_to` and is `approved`.
- [ ] An `nfr` declares `applies_to`.

## 2. Identity and uniqueness

- [ ] No two specs share an `id`.
- [ ] No two specs share a requirement id.
- [ ] Requirement ids match `REQ-[A-Z][A-Z0-9]*-[0-9]{3,}`.
- [ ] A requirement id is not reused after a rename; create a new id instead.

## 3. Links

- [ ] Every `links[].target` exists as a spec id, or is an absolute URL.
- [ ] No spec links to itself.
- [ ] Every `rel` is one of: `implements`, `part-of`, `depends-on`, `exposes`,
      `publishes`, `consumes`, `constrained-by`, `decided-by`, `supersedes`,
      `superseded-by`, `documents`, `relates-to`, `owned-by`.
- [ ] An approved spec does not link to a `draft` or `deprecated` spec.
- [ ] The reverse edge is not duplicated by hand.

## 4. Requirements

- [ ] Every `### REQ-...` has a title after the colon.
- [ ] `Priority` is `must`, `should`, or `may`.
- [ ] `Normative: true` has all of Given, When, and Then.
- [ ] The Then clause is observable: a status, an event, a record, a metric, or a
      user-visible result.
- [ ] The requirement describes one behaviour, not a bundle.
- [ ] A `Traces` path, when present, exists in the implementation repo.

## 5. Decision provenance

- [ ] `decision_mode` is `human` or `agent-assisted`; missing means `human`.
- [ ] `agent-assisted` has a `## Agent Decisions` section and at least one inline
      marker.
- [ ] `human` has no `## Agent Decisions` rows and no inline markers.
- [ ] Every requirement is either human-decided or marked
      `**Decided by:** agent (POC)`.
- [ ] Every agent decision appears in `## Agent Decisions` with question, chosen,
      why, alternatives, reversible, and revisit trigger.
- [ ] No agent decision covers security, privacy, compliance, data ownership,
      pricing, legal, or a breaking public contract.
- [ ] An approved spec with agent decisions has a review note accepting them.
- [ ] A requirement with no provenance and no human answer is an error; do not
      infer that the agent decided it.

## 6. Kind rules

| Kind | Check |
|---|---|
| system | scope and non-goals are explicit; flows and system standards are linked |
| domain | `part-of` -> system; invariants are stated; services link back with `implements` |
| service | exactly one `implements` -> domain; at least one `exposes` / `publishes` / `consumes` -> contract; `constrained-by` -> applicable standards/NFRs; data ownership is explicit |
| contract | `part-of` -> service; `type` and `path`; consumers are named; compatibility policy exists |
| flow | at least two service targets via `part-of` / `relates-to`; happy path, failure, compensation, observability |
| nfr | `applies_to`; a measurement, window, and threshold; what degrades first |
| standard | `applies_to`; verification method; exception process; `pinned` only when mandatory |
| adr | context, decision, rejected alternatives, consequences |

## 7. Graph hygiene

- [ ] No dependency cycle among services (`depends-on`).
- [ ] Every contract has at least one service that exposes, publishes, or consumes
      it.
- [ ] Every service has at least one contract boundary.
- [ ] Every domain is `part-of` a system.
- [ ] Every flow references at least two services.
- [ ] No approved spec has open questions.
- [ ] No orphan spec: something links to every spec except `system` and
      `standard`.

## 8. Version hygiene

- [ ] An approved spec's body matches its released version.
- [ ] Any change to an approved spec has a proposal in `changes/` with a
      `base_version` equal to the current version.
- [ ] The proposed `bump` matches the semantic change (see
      `checklists/review.md`).
- [ ] An approved spec has not moved back to `draft` or `proposed`.
- [ ] If git history is available, compare the current file with the last release
      commit; otherwise record that drift could not be checked.

## 9. Security and hygiene

Search the spec and proposal text for:

- [ ] prompt-injection phrases: "ignore previous instructions", "you are now",
      "act as", "system prompt", "developer message";
- [ ] active HTML: `<script`, `<iframe`, `<object`, `<embed`;
- [ ] credentials: `AKIA...`, `ASIA...`, `BEGIN ... PRIVATE KEY`,
      `password:`, `secret:`, `api_key:`, `token:` followed by a value;
- [ ] private addresses: `localhost`, `127.0.0.1`, `10.x.x.x`, `.internal`,
      `.local`;
- [ ] unresolved placeholders in approved specs: `TODO`, `TBD`, `FIXME`;
- [ ] pipe-to-shell commands (`curl ... | sh`).

## 10. View freshness

- [ ] `GRAPH.md` matches the current ids, statuses, and versions, or is
      explicitly marked as stale.
- [ ] The graph in `GRAPH.md` matches the `links` in the specs, or is marked
      illustrative.

## Output

```md
## Validation
- scope: specs/ and changes/
- errors: <n>
- warnings: <n>
- findings:
  - [error] specs/service/orders.md:12 — service has no `exposes` link
  - [warning] specs/contract/orders-api.md:8 — consumer is not named
```

Block approval on errors. A warning is allowed only with a one-line explanation in
the review packet.
