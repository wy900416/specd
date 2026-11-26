# Design decisions

Each row is a default, the reason it exists, and what it costs. When a default
stops paying for itself, this table is where the argument starts.

| Decision | Why | Cost |
|---|---|---|
| Spike before spec | A POC needs feedback before precision | Spike code is throwaway |
| Describe, don't interview | The first useful answers come from a running product | The draft may be thin; labels expose it |
| Agent validation + tiered human approval | Speed in bootstrap, safety in evolution | More approval steps for major changes |
| Mature changes are proposals | An approved baseline is read-only; consumers need impact | A change record to write |
| Backfill before evolution | A mature project needs a baseline before changes | Time to reconstruct current behaviour |
| Small changes skip fleet | A one-file change does not need a plan or coordination | Large changes still need one |
| Plan before fleet | Parallel agents need disjoint files and a complete test map | One architect step |
| Aggressive, labelled inference | The user reacts to a default faster than to a question | More assumptions to review |
| High-risk facts are fenced | A POC can test with fake data without guessing production policy | Must be confirmed before promotion |
| `version` stays `0.1.0` in POC | A version that changes on every edit means nothing | Mature stage must start semver |
| `approved_sha` binds the baseline | An approved spec has no validation record to trust | One hash to write at release |
| Mature reviews are recorded in the CHG | A release needs evidence, not a chat summary | A review section to write |
| One active CHG per target | Concurrent proposals collide on the same base | Changes to one baseline serialize |
| One `system` spec first | Boundaries are hypotheses at POC stage | Split later on evidence |
| Separate validator | The writer cannot grade its own work | One more run |
| Global skills read-only | Preferences inform the stack; they are not requirements | Fewer personal details copied |
| No index until scale | A second list drifts | Agents read all specs while small |
| Plain Markdown | Portable, diffable, no runtime | No automated lint |

## Related reading

- Why describe-infer-validate: [`vibe-spec.md`](vibe-spec.md).
- Why one spec: [`one-big-spec.md`](one-big-spec.md).
- When an index earns its keep: [`index.md`](index.md).
- When to parallelize: [`fleet.md`](fleet.md).
