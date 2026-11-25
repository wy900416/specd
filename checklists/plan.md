# Plan checklist

The `architect` agent applies this before setting `status: ready`. A plan that
passes is safe to hand to a fleet: the file sets are disjoint, the test mapping is
complete, and the fenced assumptions are carried.

Mark every item `pass`, `warning`, or `block`.

## 1. Preconditions

- [ ] The target spec is `status: validated`. **block**
- [ ] `spec_sha` matches the spec's canonical hash (`SPEC.md` §9). **block**
- [ ] The plan has `plan`, `spec`, `status`, `created`, `updated`. **block**
- [ ] `status` is `draft` while checking. **block**

## 2. Scope and decision

- [ ] In-scope `REQ-` ids exist in the spec. **block**
- [ ] Out-of-scope is explicit. **warning**
- [ ] No requirement from the spec is silently dropped. **block**
- [ ] The plan states a recommendation (build, slice, wait), the smallest slice,
      and what would change the decision. **warning**

## 3. Architecture

- [ ] The shape is named (module / modular monolith / services). **block**
- [ ] Components have responsibilities and boundaries. **block**
- [ ] Data flow and storage are stated. **block**
- [ ] Interfaces are stated. **warning**
- [ ] A non-obvious choice has an alternative and a reason. **warning**
- [ ] The architecture fits the spec's non-goals. **block**

## 4. File map

- [ ] Every file to create or modify has a path and an action. **block**
- [ ] Every path is inside the repository. **block**
- [ ] Every path belongs to exactly one track. **block**
- [ ] No two tracks list the same file. **block**
- [ ] Shared files (`package.json`, lockfile, `tsconfig`, test config, schema
      registry) are in a setup track that finishes before the parallel tracks.
      **block**
- [ ] Dependencies between tracks form a DAG (no cycle). **block**

## 5. Work tracks

- [ ] Every track has an agent, a file set, a dependency list, and "done when".
      **block**
- [ ] Implementation tracks and test tracks own disjoint files. **block**
- [ ] Test tracks can run in parallel with implementation, but execution is after
      both. **warning**
- [ ] A track that needs another track's file declares the dependency or has a
      merge step. **block**

## 6. Test strategy

- [ ] Every in-scope `REQ-` maps to at least one test file. **block**
- [ ] The map names the level (unit / integration / black-box). **warning**
- [ ] The verifier owns the conformance tests; the implementer owns developer
      tests. **block**
- [ ] The verifier is given the spec and this table, not the architecture notes.
      **block**

## 7. Risks and fences

- [ ] Every `Risk: high` assumption from the spec appears. **block**
- [ ] The fake boundary is stated (data, provider, auth, money, PII). **block**
- [ ] No plan step would touch real users, money, or PII for a fenced fact.
      **block**
- [ ] An irreversible step is named and blocked on a human. **block**

## 8. Hygiene

- [ ] No `TODO` or `TBD` in a `ready` plan. **block**
- [ ] Every open question has an owner and blocks `ready`. **block**
- [ ] The verification command exists and matches the stack. **warning**
- [ ] The plan does not edit the spec. **block**

## Output

```md
## Plan check

- Spec: <id> (validated, sha match)
- Scope: pass
- Architecture: pass
- File map: pass (<n> files, <n> tracks, 0 overlaps)
- Test strategy: pass (<n> REQ mapped)
- Risks: pass
- Hygiene: pass
- Result: ready | blocked
```

On a block, list the exact fixes under `### Blocking`. Do not set
`status: ready` until every blocking item is clear.
