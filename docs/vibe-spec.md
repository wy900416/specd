# Vibe spec: describe, infer, validate

A POC exists to answer a product question. The spec should be cheap enough to
write in one pass and precise enough to build from. A long interview is the wrong
tool for that job: it spends the user's attention before there is anything to
react to.

## The problem with interview-first

A structured interview asks the user to answer abstract questions before they have
seen the product. Most answers are guesses, and the questions that matter only
appear after the first build. The interview also front-loads precision the POC
does not need, and it makes the spec feel like a contract the user is afraid to
change.

## The bet

**A POC spec is a working hypothesis.** It is:

- written from a short description, in one pass;
- filled with labelled inferences, not questions;
- validated by an agent against a checklist, not approved by a human;
- revised after the user reacts to the running product.

Precision is added where it changes a decision, not everywhere.

## The loop

```text
user describes the product
        |
        v
  writer drafts  ---->  gap-filler infers  ---->  validator gates
        ^                                             |
        |                                             | pass
        |                                             v
        |                                    architect plans
        |                                             |
        |                              implementer + verifier (fleet)
        +---------------- revise <-------------------+
```

1. **Describe.** One paragraph is enough. The writer stores it verbatim.
2. **Draft.** Requirements that trace to the description; everything else is a
   visible gap.
3. **Infer.** The gap-filler reads the repo and the user's global skills, applies
   the inference ladder, and labels every guess.
4. **Validate.** A separate agent applies `checklists/validate.md` and sets
   `validated` only on a clean pass.
5. **Plan.** The architect turns the validated spec into `plans/<id>.md`:
   architecture, file map, work tracks, and test strategy.
6. **Build and test in parallel.** Implementers write the code tracks; the
   verifier writes conformance tests from the spec. The files are disjoint; the
   tests run after both land.
7. **Revise.** User feedback changes the spec; it returns to `draft` and is
   re-validated. The plan becomes `stale` if the spec changed.

## What changed from the v1 framework

| v1 | v2 |
|---|---|
| Interview is the default path | Description is the default path; interview is optional |
| Human approval is the gate | Agent validation is the gate |
| Agent asks when unsure | Agent infers and labels; asks only for user-reserved facts or conflicts |
| Version bumps on release | `0.1.0` for the whole POC; git is the history |
| Graph from day one | One `system` spec until a seam is real |
| Proposal for every approved-spec edit | Edit the draft, re-validate |
| Build from the validated spec | Architect plan, then fleet implementation + tests |

## Aggressive inference: one hard brake, one fence

The agent may choose the stack, naming, structure, data shapes, defaults, and POC
simplifications without asking.

**The hard brake: conflicts.** A contradiction with an existing spec is not a gap
to guess around. It goes to `## Conflicts`, with options, and the user chooses. An
open conflict blocks validation.

**The fence: high-risk facts.** Security, privacy, data ownership, pricing, legal,
compliance, and breaking public contracts may be inferred for a POC, but they must
be marked `Risk: high`, `Confirmed: agent (POC)`, and `Revisit: before production`.
Build against them only with fake data, a local provider, and no real users, money,
or PII. The validator records them as warnings; they do not block the POC, and they
must be confirmed before contract promotion.

Everything else is a labelled assumption with a revisit trigger.

## Validation replaces approval

Approval asks "does a human accept this?" Validation asks "does the checklist find
a gap, a contradiction, an unsupported claim, a user-reserved fact, or a
conflict?". The second question is the one a POC can answer at speed.

The validator is not the writer. It reads the spec, the source, the evidence, and
the checklist, but not the writer's rationale. A validation is bound to the file
hash, so an edit invalidates it.

Validation is not a proof. It catches what the checklist can name. The user is
still the only one who can say the product is worth building.

## When vibe mode ends

Promote a spec to contract stage when one of these is true:

- another team depends on it;
- it deploys independently;
- an external consumer uses its contract;
- it handles real money, PII, or regulated data;
- a change would be expensive or irreversible;
- the interface has survived two changes.

Then version, approval, and proposals start to pay for themselves. See
[`contract-mode.md`](contract-mode.md).

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Plausible fiction | Every guess is labelled; evidence is required; the validator reports fenced high-risk facts |
| Validation theater | Validator is a separate run; checklist output is in the file; hash binds it |
| Spec drifts from code | Validate before handoff; verifier tests from the spec, not the code || Global skills leak or override | Read-only, cite only, never copy content, never treat as requirements |
| The user never reads the spec | Keep it to one page; report 3-5 requirements, not the whole file |
