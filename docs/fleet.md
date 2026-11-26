# Fleet: implementation and test generation

Fleet is most useful in specd **after the plan**. The spec is written
sequentially; the implementation and the conformance tests are what parallelize.

## What is available

| Surface | What it gives you |
|---|---|
| `/fleet` in Copilot CLI / app | An orchestrator decomposes an objective into subagent tasks, runs independent ones in parallel, and merges results |
| Custom agents in `.github/agents/` | Selectable roles with their own tools and instructions (`specd`, `architect`, `implementer`, `verifier`, ...) |
| Subagents via the `agent` tool | An agent can delegate a bounded task to another agent with its own context |
| VS Code | Custom agents, plus subagent delegation where the build exposes the `agent` tool; `/fleet` itself is a CLI/app command |

Each subagent has its own context window and **shares the filesystem**. Subagents
cannot talk to each other; only the orchestrator coordinates.

## The rule

> Plan first. Parallelize reads and disjoint writes. Run tests after the last
> write.

The filesystem has no locking. If two agents write the same file, the last one
wins silently.

## Plan first

A fleet needs a `plans/<spec-id>.md` with:

- `status: ready`;
- a `spec_sha` that matches the validated spec;
- a **decision**: build, build a slice, or wait, plus the smallest slice;
- a **file map** where every file belongs to exactly one track;
- work tracks with dependencies and a "done when";
- a **test strategy** mapping every in-scope `REQ-` to a test file.

No plan, no fleet. The architect produces it; the orchestrator dispatches it. The
plan can also be a deliberate stop: run `/plan-implementation`, read the decision
and tracks, then run `/implement` when you are ready.

## Safe parallel work

- **Implementation tracks**, one disjoint file set each. Example:
  `src/shorten/**` and `src/api/**`.
- **Test tracks**, one test file (or directory) each. The verifier writes them
  from the spec while the implementer writes code.
- **Discovery scans** for a spec, one artifact each under `.context/<id>/`:
  repo profile, global skills preferences, conflict scan, contract impact.
  One writer merges them into `.context/<id>.md` before implementation.
- **One spec per agent** for a multi-spec POC, with disjoint paths.
- **Contract impact scans** across different consumer groups.

## Unsafe parallel work

- Two agents editing the same source file or the same test file.
- Two agents editing `package.json`, a lockfile, `tsconfig`, or the test config.
  Put those in a setup track that finishes before the fleet starts.
- The verifier reading the implementation while writing assertions (it should
  write from the spec first).
- Running tests before the implementation tracks finish.
- Generating `specs/INDEX.md` while specs are being added.
- Two agents appending to the same `## Conflicts` section without a merge step.
- Two agents writing the same `.context/<id>.md`; the discovery fragments are
  inputs, and one merge step produces the pack.
- Two change-analysts preparing a CHG for the same `target` and `base_version`,
  or two architects re-planning the same spec in place.

## Patterns

### Pattern 1: implementation + tests from a ready plan (primary)

```text
/fleet Implement plans/url-shortener.md.

Tracks from the plan:

1. T1 core shortening — src/shorten/**, tests/unit/shorten/**
   Use @implementer.agent.md.
2. T2 HTTP API — src/api/**, tests/api/**
   Use @implementer.agent.md.
3. V1 conformance — tests/conformance/shorten.test.ts
   Use @verifier.agent.md. Write from the spec and the Test Strategy table.
   Do not read T1/T2 implementation before writing assertions.

Each track gets .context/url-shortener.md and its plan row.

Run T1, T2, V1 in parallel. The files are disjoint.
If the plan has a setup track (dependencies, tsconfig, test config), run it first.
After all three finish, run `pnpm test` and report each REQ as pass/fail/blocked.
```

Pass the `## Test Strategy` table to the verifier as text, not the plan file.
The plan also contains the architecture notes and file map the verifier must not
see.

Why it works: the tests are written from the spec, in parallel with the code, and
executed only after both land. The verifier never grades the implementer's own
tests.

### Pattern 2: parallel discovery for one spec

```text
/fleet Profile the repository for specs/system/url-shortener.md.

1. .context/url-shortener/repo-profile.md — manifests, layout, test command
2. .context/url-shortener/preferences.md — global skills, conventions
3. .context/url-shortener/conflicts.md — conflicts with existing specs

Read-only subagents. Do not edit the spec. Report each artifact separately.
Then merge the three artifacts into `.context/url-shortener.md`; do not dispatch
implementation from the fragments.
```

### Pattern 3: several independent specs

```text
/fleet Create three independent POC specs. Use @spec-writer.agent.md per track and
keep the files disjoint:

1. specs/service/orders.md
2. specs/service/payments.md
3. specs/service/users.md

Run 1-3 in parallel. When all three files exist, run @spec-validator.agent.md on
each file sequentially. Report each track separately.
```

### Pattern 4: contract impact scans

```text
/fleet Scan consumers of orders-api@1.2.0.

1. services that list orders-api in links
2. tests that assert the old field names
3. docs that describe the old contract

Each track writes a separate file under .context/orders-api/impact/. Do not edit
the specs. Report the impact map.
```

## Prompt rules

- Name concrete artifacts: one path per work item.
- State dependencies explicitly ("run the tests after T1 and T2 finish").
- Set boundaries: "no changes outside `src/shorten/**`".
- Give each subagent everything it needs; it cannot see the orchestrator's chat.
- Use `@architect.agent.md`, `@implementer.agent.md`, or `@verifier.agent.md`
  per track when the job differs.
- Keep test files out of the implementation tracks; that is what makes the
  parallel write safe.

## Cost and when not to use it

Every subagent is an independent model interaction. Use a fleet when:

- the plan has two or more file-disjoint implementation tracks;
- conformance tests split cleanly by file;
- the POC has several independent specs;
- a contract change needs parallel impact scans.

Do not use it when:

- the plan has one track — sequential is faster;
- the spec is still a draft — validate first;
- the work is one file — writes will collide;
- you have no plan — the fleet will invent its own boundaries, badly.

## Independence

The verifier must run in a context that did not write the draft or the
implementation. In a fleet:

- give it the spec and the `## Test Strategy` table as text, not the plan file or
  the architecture notes;
- give it its own test files;
- run it after the implementation lands.

If the orchestrator passes a summary of the implementation, the independence is
gone.

## References

- [Delegating and parallelizing work with agents](https://docs.github.com/en/enterprise-cloud@latest/copilot/concepts/agent-capabilities/choosing-and-delegating-agent-work/delegating-and-parallelizing-work-with-agents)
- [Run multiple agents at once with /fleet in Copilot CLI](https://github.blog/ai-and-ml/github-copilot/run-multiple-agents-at-once-with-fleet-in-copilot-cli/)
