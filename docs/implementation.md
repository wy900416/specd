# Implementation: plan, then fleet

A validated spec (or an approved target with a released `CHG`) is not an
implementation plan. The architect designs the architecture and the parallel work
first.

## 1. Produce the plan

```text
/plan-implementation specs/system/url-shortener.md
```

The architect also writes `.context/url-shortener.md` (the bounded context pack).
The plan lives at `plans/url-shortener.md` and contains:

- **Decision:** build, build a slice, or wait;
- **Architecture** and data flow;
- **File map:** one owner per file;
- **Work tracks:** disjoint files, dependencies, done when;
- **Test strategy:** every in-scope `REQ-` mapped to a test file;
- **Risks and fences** carried from the spec.

The plan is bound to the spec's canonical hash (`spec_sha`): copy `validated_sha`
for a validated spec or `approved_sha` for an approved baseline. If the spec
changes, the plan is `stale` and must be re-planned.

## 2. Run the fleet

```text
/implement specs/system/url-shortener.md
```

Or, with `/fleet` in Copilot CLI/app:

```text
/fleet Implement plans/url-shortener.md.

Tracks:
1. T1 core — src/shorten/**, tests/unit/shorten/** — @implementer.agent.md
2. T2 API — src/api/**, tests/api/** — @implementer.agent.md
3. V1 conformance — tests/conformance/shorten.test.ts — @verifier.agent.md

Run T1, T2, V1 in parallel; the files are disjoint.
If the plan has a setup track, run it first.
After all finish, run `pnpm test` and report each REQ as pass/fail/blocked.
```

Each track receives `.context/url-shortener.md` and its plan row. The verifier
gets the `## Test Strategy` table as text, not the plan file.

## 3. What runs in parallel

- **Setup first:** dependencies, lockfile, shared config, schema, test config.
- **Implementation tracks and verifier test tracks in parallel.** Each owns
  disjoint files.
- **Tests run after both land.** The verifier writes from the spec and the
  `## Test Strategy` table, not from the implementation.
- **The verifier gets the Test Strategy table as text, not the plan file.** The
  plan also contains the architecture notes and file map it must not see.
- **The verifier never grades the implementer's own tests.**

## 4. Read the result

The verifier reports one row per in-scope `REQ-`: pass, fail, or blocked. Each
failure is classified as a **code bug**, a **spec ambiguity**, or a **harness
issue**. The plan is `done` only when every in-scope `REQ-` passes.

## 5. When not to fleet

If the plan has only one track total, run the implementer, then the verifier.
Fleet is for disjoint work, not for a single file.

For a **mature single-track change**, skip the plan and the fleet: run the
implementer, then regression plus contract tests. The verifier reads the CHG's
`## Test Strategy`, not a plan. The plan is for new builds and multi-track
changes.

## Full rules

Prompt patterns, unsafe parallel work, cost, and the verifier's independence are
in [`fleet.md`](fleet.md). The plan template is
[`../templates/plan.md`](../templates/plan.md).
