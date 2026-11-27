---
mode: 'agent'
description: 'Design an implementation plan from a validated spec: architecture, file map, work tracks, and test strategy.'
---

Plan the implementation of this spec:

${input:spec}

Follow `agents/architect.md`, `templates/plan.md`, and `checklists/plan.md`.

1. Confirm the spec is `status: validated`, or `status: approved` with a released
   `CHG`, and that its canonical hash is current. If not, stop and send it to
   `/validate-spec`.
2. Build or refresh `.context/<spec-id>.md` per `checklists/context.md`; merge any
   discovery fragments. Read the spec, the pack, and the repository (layout,
   modules, test harness, conventions).
3. Write `plans/<spec-id>.md` with:
   - architecture and data flow;
   - a file map with one track per file set;
   - work tracks with disjoint files and dependencies;
   - a test strategy mapping every in-scope `REQ-` and every acceptance
     criterion to a test file;
   - the fenced high-risk assumptions;
   - `spec_sha` copied from `validated_sha` or `approved_sha`.
4. Run `checklists/plan.md`. On a clean pass, set `status: ready`; otherwise keep
   `draft` and list the fixes.
5. Report the tracks, the test mapping, and the open questions.

Do not write code, tests, or a migration. Do not edit the spec.
