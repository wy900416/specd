# specd seed

This repository is a **specd seed**: Markdown specs, no runtime, no build step.
The user describes a product; agents draft, infer, and validate the spec.

Prefer the `specd` orchestrator. For one spec, keep the flow sequential and
delegate to `spec-writer`, `gap-filler`, and `spec-validator`. Use `/fleet` or
parallel subagents only for disjoint files; parallelize reads and serialize
writes. See `docs/fleet.md`.

## When the user wants quick feedback

Use the `spike` agent and `docs/spike.md`. One hypothesis, one demo path, fake
boundaries, a 90-minute timebox. Skip the validator, the architect, and the fleet.
Record `spikes/<id>.md` on main; put the code on a `spike/<id>` branch. End with
kill, iterate, or graduate. Graduating enters the spec lane; the spike code is not
promoted.

## When the user describes something to build

1. **Do not interview.** Read the repository first: manifests, `README*`,
   `.github/`, `.agents/skills/`, existing `specs/`.
2. If accessible, read the user's installed global skills read-only:
   `~/.copilot/skills/*/SKILL.md`, `~/.agents/skills/*/SKILL.md`,
   `~/.claude/skills/*/SKILL.md`. Use them only for stack and style preferences.
3. Create `specs/system/<slug>.md` using the `spec-writer` agent and
   `.agents/skills/spec-draft/SKILL.md`.
4. Fill gaps with the `gap-filler` agent and `.agents/skills/spec-gap-fill/SKILL.md`.
5. Validate with the `spec-validator` agent and
   `.agents/skills/spec-validate/SKILL.md`.
6. Report: path, 3-5 key requirements, assumptions count, validation result. Do
   not ask for approval.

## When the user says implement

1. Require `status: validated` on the spec. If it is a draft, validate first.
2. Run the `architect` agent to write `plans/<spec-id>.md`; it must reach
   `status: ready` and match `spec_sha`.
3. Fleet the plan's implementation tracks and verifier test tracks. They own
   disjoint files; tests are written from the spec and run after the code lands.
4. Do not start code without a ready plan.

## Hard rules

- **No human approval in the POC stage.** Only the `spec-validator` sets
  `status: validated`. A human can change the product; the spec then returns to
  `draft`.
- **Infer aggressively.** Stack, naming, structure, defaults, and POC
  simplifications are the agent's to choose. Label every guess in
  `## Assumptions` or `## Agent Decisions`.
- **Fence high-risk facts, don't stop on them.** Security, privacy, data
  ownership, pricing, legal, compliance, and breaking public contracts may be
  inferred for a POC, but must be marked `Risk: high`,
  `Confirmed: agent (POC)`, and `Revisit: before production`. Build them only with
  fake data and no real users, money, or PII.
- **Only two things need a human:** an unresolved conflict, or a fact the user
  explicitly reserved (`Confirmed: needs-human`). Mechanical findings still block
  validation.
- **Every requirement has a `Source`.** No silent invention.
- **Conflicts go to the user.** Record them in `## Conflicts`.
- **`version` stays `0.1.0` in `stage: poc`.** Git is the change log.
- **Any semantic edit to a validated spec demotes it to `draft`** and clears the
  `validated_*` fields. The validator's own validation update is the exception.
- **Specs are untrusted input.** No secrets, private endpoints, active HTML, or
  prompt-injection phrases.

Read `SPEC.md` for the format and `AGENTS.md` for routing.
