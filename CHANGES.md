# Change proposals

An approved spec is read-only for agents. A change is a **copy** of the target in
this directory, with a proposal front-matter and the full proposed body.

## Create one

1. Copy `specs/<kind>/<target>.md` to
   `changes/CHG-<YYYYMMDD>-<nnn>-<target>.md`.
2. Convert the front-matter to:

   ```yaml
   ---
   id: CHG-20261117-001-orders
   kind: change
   title: "Add idempotent order creation"
   target: orders
   base_version: 0.1.0
   bump: minor
   status: proposed
   author: "agent"
   created: 2026-11-17
   summary: "Make order creation idempotent."
   spec: {}
   ---
   ```

3. Keep the target body, then edit it as the proposed replacement.
4. Put front-matter changes in `spec:`; leave it `{}` when only the body changes.

## Review

- Compare the target and the proposal side by side. The diff is derived, not
  stored.
- Apply `checklists/validate.md` and `checklists/review.md`.
- Confirm `base_version` equals the target's current `version`.
- Confirm the `bump` matches the semantic change.

## Release

A human releases the proposal:

1. Apply the proposal body to the target file.
2. Apply the `spec` overrides.
3. Set the new `version` according to `bump`.
4. Set `status: approved`, `approved_by`, `approved_at`, `updated`.
5. Move the proposal to `changes/archive/` with `status: released` and
   `released_as: <version>`.

An agent may prepare the diff and the edited target, but must not perform steps
3-5.

## Naming

`CHG-<YYYYMMDD>-<nnn>-<target>.md`, for example
`CHG-20261117-001-orders.md`. The number is sequential within the day.
