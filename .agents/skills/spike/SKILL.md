---
name: spike
description: "Run a timeboxed POC spike: one hypothesis, one demo path, fake boundaries, then feedback and a kill/iterate/graduate decision."
whenToUse: "The user wants to see something quickly, asks for a demo, or the question is would this be useful rather than what exactly to build."
---

# Spike

The fastest path from an idea to feedback. No spec validation, no architect plan,
no fleet, no conformance suite.

## Read first

- `docs/spike.md` — the loop and the rules.
- `templates/spike.md` — the log.
- `checklists/spike.md` — demo-ready checks.

## Procedure

1. **Hypothesis.** Write: we believe `<user>` will `<action>` because `<reason>`;
   we will know it worked if `<signal>`. If there is no signal, ask one question.
2. **Demo contract.** Five lines in `spikes/<id>.md` on the main branch, so the
   log survives the code:
   - one path: open, do one thing, see one result;
   - fake: data, auth, payments, integrations;
   - run: the exact command;
   - artifact: URL, screenshot, or recording;
   - out of scope: everything else.
3. **Branch.** `spike/<id>` for the code; keep the log on main.
4. **Build one vertical slice.** Use the repo's stack if it exists; otherwise the
   simplest thing that runs. One agent. No polish.
5. **Smoke test.** Run the one path. Fix only blockers.
6. **Demo at the timebox.** 90 minutes by default; 60 for a narrow demo. Stop and
   show it even if broken.
7. **Feedback.** Ask: what did you expect, what surprised you, would you use it
   again? Record the answers.
8. **Decide.** Kill, iterate once, or graduate. Record the decision and the next
   slice.

## Rules

- Fake auth, data, payments, email, and third-party APIs.
- No real users, money, PII, or secrets.
- No full spec, no validator, no architect, no fleet.
- No design system, settings page, or edge cases.
- One change per iteration; same timebox.
- Graduating means the bootstrap lane, not promoting the spike code.

## Output

```md
## Spike
- id: <id>
- branch: spike/<id>
- hypothesis: <one sentence>
- demo: <the one path>
- fake: <what is faked>
- run: <command>
- feedback: <3 answers>
- decision: kill | iterate | graduate
```
