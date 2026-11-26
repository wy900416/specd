# Spike lane: quick feedback

A POC is a **learning loop**, not a delivery pipeline. The spec lane is for
building the right thing durably. The spike lane is for learning what the right
thing is.

Use a spike when the question is "would this be useful?" and you need to see
something today. Use the spec lane when the spike says "keep going".

## The 90-minute loop

```text
0. Hypothesis        one sentence + the signal that proves it
1. Demo contract     one path, fake boundaries, one run command
2. Build             one agent, one vertical slice, no ceremony
3. Demo              at the timebox, even if broken
4. Feedback          3 questions, recorded
5. Decide            kill / iterate / graduate
```

## 0. Hypothesis

Write one sentence:

> We believe **<user>** will **<action>** because **<reason>**. We will know it
> worked if **<signal>**.

If you cannot name a signal, you are not ready to build; ask the user one
question.

## 1. Demo contract

Five lines, no more:

- **Path:** open the app, do one thing, see one result.
- **Fake:** in-memory data, fake auth, fake payment, no external integration.
- **Run:** the exact command that starts it.
- **Artifact:** a URL, a screenshot, or a 2-minute screen recording.
- **Out of scope:** everything else.

Write it in `spikes/<id>.md` before coding.

## 2. Build

- **One agent.** Do not run the spec validator, the architect, or a fleet.
- **One vertical slice.** A working path beats three half-built layers.
- **Simplest stack that runs.** Use the repo's stack if it exists; otherwise pick
  the smallest thing that can show the path.
- **No polish.** No design system, no settings page, no edge cases.
- **One check.** A smoke test or a manual run, not a conformance suite.

## 3. Demo

At the timebox, stop and show what exists. A broken demo is still information.
Do not extend the timebox without the user's explicit yes.

Demo script:

1. Here is the one path.
2. Here is what is fake.
3. Here is what works.
4. Here is what does not.

## 4. Feedback

Ask exactly three questions:

1. What did you expect to happen?
2. What surprised you?
3. Would you use this again, and for what?

Record the answers in `spikes/<id>.md`. Do not defend the demo; listen.

## 5. Decide

| Decision | Meaning | Next |
|---|---|---|
| **Kill** | The signal was not there | Archive the branch; keep the learnings |
| **Iterate** | The signal is promising, one thing is wrong | One change, one new demo, same timebox |
| **Graduate** | This should become real | Enter the spec lane |

## Rules

- **Timebox:** 90 minutes by default; 60 for a narrow demo.
- **Log on the main branch:** write `spikes/<id>.md` on the main branch before you
  branch, so the learnings survive if the code is deleted.
- **Code on a throwaway branch:** `spike/<id>`.
- **Fake everything external:** auth, payments, email, third-party APIs, PII.
- **No real users, money, or private data.**
- **No spec validation, no architect plan, no fleet, no conformance suite.**
- **No promotion of spike code.** Graduating means the spec lane, then a clean
  implementation. The spike is a reference, not the base.

## Graduate to the spec lane

1. Write the spec from what the demo taught you: `/new-spec` with the hypothesis,
   the demo path, and the feedback.
2. Validate it.
3. Run `/plan-implementation`.
4. Implement from the plan, not from the spike branch.
5. Keep `spikes/<id>.md` as the evidence for the first requirements.

## Why it is faster

- The first code is written in the first 15 minutes, not after four agent phases.
- The demo is the artifact; the spec is written from evidence, not guesses.
- The timebox prevents polishing a thing the user may not want.
- Fake boundaries remove the slowest dependencies.
- One agent removes handoff latency.

## When not to spike

- The change is a small edit to an existing, validated product.
- The risk is security, privacy, payments, or data loss.
- The user already knows exactly what to build and needs it durable.
- You cannot fake the external dependency and the real one is slow to obtain.

For those, use the spec lane.
