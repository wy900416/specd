# Troubleshooting

| Symptom | Fix |
|---|---|
| The delivery flow feels slow | That is the bootstrap lane. Use `/spike` for a 90-minute demo first. In a mature project, small changes skip the plan and fleet. |
| `specd` is not in the agent picker | Reload the window. Confirm `.github/agents/specd.agent.md` exists. Use `/new-spec` as a fallback. |
| `/fleet` is missing | `/fleet` is a Copilot CLI/app command. In VS Code, use the custom agents and subagents, or run `/plan-implementation` then `/implement`. |
| Prompt files do not appear on github.com | Prompt files are an IDE surface. Use the custom agents there, or describe the step. |
| `/spike` or `/new-spec` does nothing outside VS Code | Prompt files are IDE-only. Describe the same step and name the agent; `/fleet` is the CLI/app command. |
| The runner cannot spawn subagents | Validate in a fresh session with only the spec path and checklist. Do not validate the draft in the same pass that wrote it. |
| The gap-filler found no global skills | Normal. It records "not accessible" in `## Repo Profile` and continues. |
| Validation is blocked | Read `## Validation`; the blocking list names the fix. Common: a requirement has no `Source`; a user-reserved fact is still `needs-human`; a conflict is open; the hash is stale; content follows `<!-- END VALIDATION -->`. |
| `approved_sha` does not match | The approved baseline was edited in place. Restore it from git; do not "fix" the hash. A change must be a `CHG`. |
| A mature change has no `## Proposal validation` | The validator has not reviewed the effective spec. Run `/validate-spec <CHG>`; release is blocked until it records a pass. |
| Validation blocks a `service` or `contract` | A kind-required edge is missing. Check SPEC §4 and the front-matter `links`. |
| Validation blocks `## Open Questions` | Resolve each unchecked item, or move it to `## Assumptions` as `Confirmed: needs-human`; revalidate. |
| The version is still `0.1.0` | Intentional in `stage: poc`. Semver starts when the spec is approved as a mature baseline. |
| I need to change an approved spec | Never edit it. Run `/change`, review impact and approvals, and let a human release. See [`change-mode.md`](../mature/docs/change-mode.md). |
| A mature project has no specs | Backfill one boundary with `/backfill`, or write the manual baseline in [`adoption.md`](../mature/docs/adoption.md). |
| A mature change is blocked | Check [`../mature/checklists/change.md`](../mature/checklists/change.md): missing consumer, major without sign-off, no migration/rollback, or a high-risk change without the security/data owner. |
| The plan says `stale` | The spec changed. Re-run `/plan-implementation`; do not reuse the old file map. |
| Two agents overwrote each other | The plan assigned one file to two tracks. Fix the file map, then re-run. |
| The spec is too large | Keep one system spec; split only on evidence. See [`one-big-spec.md`](one-big-spec.md). |
| I want no human approval | Bootstrap is agent-validated. Mature changes are tiered by design; a major change needs consumers. |
| I want a human approval gate on bootstrap | Add your own review step; the validator is the built-in gate. |

## First checks

1. **Read the file the agent wrote.** `## Validation` and `## Assumptions` explain
   most surprises.
2. **Confirm the status.** A validated spec is read-only until an edit demotes it
   to `draft`.
3. **Confirm the hash.** A plan or validation that no longer matches the spec is
   stale, not wrong.
4. **Check the lane.** Spike, bootstrap, and evolution have different rules; a fix
   from one lane may be an anti-pattern in another.
