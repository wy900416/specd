# Agents, prompts, and surfaces

The role briefs in `agents/` are the source of truth. The Copilot files are thin
wrappers, so the same procedure works in DSH, Claude Code, Cursor, or a custom
loop.

## Surfaces

| Surface | Path |
|---|---|
| Always-on instructions | `.github/copilot-instructions.md` |
| Path instructions | `.github/instructions/*.instructions.md` |
| Selectable agents | `.github/agents/*.agent.md` |
| Slash commands | `.github/prompts/*.prompt.md` |
| Skills | `.agents/skills/*/SKILL.md` (auto-discovered) |
| Cross-tool entry | [`AGENTS.md`](../AGENTS.md) |

Custom agents use `.github/agents/*.agent.md`; the older
`.github/chatmodes/*.chatmode.md` format has been superseded. Skills live in
`.agents/skills/` and are auto-discovered by Copilot; other agents can read the
same files.

## Which agent?

### Core

| Task | Agent | Why |
|---|---|---|
| Quick feedback / a demo | `spike` | one path, fake data, 90 minutes |
| New spec, end to end | `specd` | routes writer -> gap-filler -> validator |
| Draft only | `spec-writer` | no gap-fill or validation |
| Fill gaps on an existing draft | `gap-filler` | repo + global-skill inference |
| Validate only | `spec-validator` | independent gate; sets `validated` |
| Plan implementation | `architect` | architecture, file map, tracks, test strategy |
| Implement a planned track | `implementer` | one disjoint file set |
| Conformance + acceptance tests | `verifier` | tests from the spec, not the code |
| Several independent specs | `/fleet` + `specd` or `spec-writer` per file | disjoint files only |
| Implementation + tests | `/fleet` + `implementer` / `verifier` per track | plan must be ready first |

### Mature only

Do not pick these for a new build. See [`mature/README.md`](../mature/README.md).

| Task | Agent | Why |
|---|---|---|
| Change a mature spec | `change-analyst` | impact, compatibility, proposal, approvals |
| Adopt a mature project | `backfiller` | draft baseline from code and tests |
| Change review | `spec-reviewer` | graph consistency, impact, version hygiene |

You do not need to switch agents for the normal flow: select `specd` once, or run
`/new-spec`. Switch manually when you want to force a role, such as a second
independent validation or a draft-only pass.

## Prompt reference

Prompt files live in `.github/prompts/` and work in VS Code, Visual Studio, and
JetBrains. In Copilot CLI/app, describe the same step in natural language and name
the agent.

Core:

| Command | Input | What it does |
|---|---|---|
| `/spike` | a description | 90-minute demo, feedback, decision |
| `/new-spec` | a description | draft, gap-fill, validate |
| `/fill-gaps` | spec path | repo profile, assumptions, decisions, conflicts |
| `/validate-spec` | spec path | bootstrap validation, sets `status: validated` |
| `/check-conflicts` | spec path | writes `## Conflicts` for the user to resolve |
| `/plan-implementation` | spec path | `plans/<id>.md` with architecture, tracks, tests |
| `/implement` | spec path | fleet implementation and conformance tests |
| `/build-index` | none | `specs/INDEX.md` when the trigger is met |

Mature only:

| Command | Input | What it does |
|---|---|---|
| `/change` | target + change | impact, proposal, approvals for a mature spec |
| `/backfill` | a boundary | draft baseline from existing code |
| `/validate-spec <CHG>` | CHG path | proposal review recorded in the CHG |

## Global skills

The gap-filler also reads the user's installed global skills, if the runtime
exposes them:

```text
~/.copilot/skills/*/SKILL.md
~/.agents/skills/*/SKILL.md
~/.claude/skills/*/SKILL.md
```

Read-only. It cites `global-skill:<name>` and never copies their content into the
spec. If the runtime does not expose them, the gap-filler records "not accessible"
in `## Repo Profile` and continues.

## Where the rules live

| File | Role |
|---|---|
| [`../AGENTS.md`](../AGENTS.md) | Routing and hard rules |
| [`../SPEC.md`](../SPEC.md) | Normative format and lifecycle |
| [`../agents/`](../agents/) | Role briefs (source of truth) |
| [`../checklists/`](../checklists/) | Pass/fail gates |
| [`../templates/`](../templates/) | Core spec and plan skeletons |
| [`../mature/`](../mature/) | Opt-in mature docs, checklists, and templates |
