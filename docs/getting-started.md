# Getting started

From an empty seed to a validated spec, then to code. For the reasoning, see
[`vibe-spec.md`](vibe-spec.md); for the lane in detail,
[`bootstrap-mode.md`](bootstrap-mode.md).

## Before you start

- **Git.**
- **One agent surface:**
  - GitHub Copilot in VS Code (custom agents, prompt files, skills);
  - GitHub Copilot CLI/app (custom agents, `/fleet`);
  - any agent that reads [`AGENTS.md`](../AGENTS.md) (DSH, Claude Code, Cursor).
- **A shell** for the validator's canonical hash. Without one, the validator
  cannot bind a validation to the file.
- **A repository to build in.** The seed is the starting point; clone it or copy
  the files into an existing repo. For a mature project, start with
  [`adoption.md`](../mature/docs/adoption.md).

Specs are inputs to agents. Do not paste credentials, private endpoints, or
untrusted instructions into a spec.

## 1. Get the seed

```bash
git clone https://github.com/wy900416/specd.git my-poc
cd my-poc
```

Or click **Use this template** on GitHub and clone your copy.

## 2. Open it with an agent

| Surface | What to do |
|---|---|
| VS Code + Copilot | Open the folder, open Copilot Chat, select the `specd` agent, and paste the description. If the picker does not show it, reload the window or run `/new-spec`. |
| Copilot CLI/app | Start in the folder and describe the product. Custom agents are in `.github/agents/`; `/fleet` is available for implementation. |
| Any other agent | Say: "Read `AGENTS.md` and follow `agents/orchestrator.md`." |

Prompt files such as `/new-spec` are IDE surfaces. In Copilot CLI/app or another
agent, describe the same step and name the agent. The full surface map, role list,
and command reference are in [`agents.md`](agents.md).

## 3. Describe the product

One paragraph is enough:

> Build a URL shortener for a small internal team. Links expire after 30 days, and
> I want a simple web page plus an API.

The agent reads the repo, drafts `specs/system/url-shortener.md`, fills gaps with
labelled inferences, and validates. You are not asked to answer a questionnaire
first.

## 4. Check the result

The agent reports:

- the requirements;
- the assumptions it made;
- any fenced high-risk fact;
- the validation result.

There is no approval step. If validation blocks, read `## Validation` in the
spec; the blocking list names the exact fix. Common blocks: a requirement has no
`Source`, a user-reserved fact is still `needs-human`, a conflict is open, the
content hash is stale, or content follows the end of the validation block.

## 5. Implement

Say **implement**. The architect writes `plans/url-shortener.md` first, then the
fleet implements the code and writes the conformance tests in parallel.

To read the plan before any code is written:

```text
/plan-implementation specs/system/url-shortener.md
```

then:

```text
/implement specs/system/url-shortener.md
```

The plan, the fleet rules, and the pass/fail report are in
[`implementation.md`](implementation.md).

## 6. If the project is mature

Do not edit an approved spec. Run:

```text
/change specs/service/orders.md "Add idempotent order creation"
```

Review the impact, compatibility, rollout, rollback, and the approvals needed. A
human releases; a small change goes straight to the implementer, a multi-track
change uses the architect plan and fleet.

Full method: [`change-mode.md`](../mature/docs/change-mode.md).

## Where next

| If... | Read |
|---|---|
| You are unsure the product is worth building | [`spike.md`](spike.md) — demo first |
| You want to know what the spec format requires | [`../SPEC.md`](../SPEC.md) |
| You want to know why there is no interview | [`vibe-spec.md`](vibe-spec.md) |
| You are importing specd into an existing repo | [`adoption.md`](../mature/docs/adoption.md) |
| Something is stuck | [`troubleshooting.md`](troubleshooting.md) |
