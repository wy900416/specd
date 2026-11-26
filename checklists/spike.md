# Spike checklist

A spike is ready to demo when the one path runs and the feedback can be collected.
It does not need to be complete.

## Before building

- [ ] The hypothesis is one sentence with a signal.
- [ ] The demo contract has one path, fake boundaries, a run command, and an
      artifact.
- [ ] The timebox is set (90 minutes by default, 60 for narrow).
- [ ] The log is on the main branch; the code is on `spike/<id>`.

## Build

- [ ] One vertical slice, one agent.
- [ ] The simplest stack that runs; the repo's stack if it exists.
- [ ] Fake auth, data, payments, email, and third-party services.
- [ ] No real users, money, PII, or secrets.
- [ ] No spec validation, architect plan, fleet, or conformance suite.
- [ ] No settings page, design system, or edge cases.

## Demo

- [ ] Starts with one command.
- [ ] The one path works, or the broken point is known and shown.
- [ ] The four-line demo script is ready.
- [ ] The timebox was respected; no silent extension.

## Feedback and decision

- [ ] The three questions were asked.
- [ ] The answers are recorded in `spikes/<id>.md`.
- [ ] The decision is kill, iterate, or graduate.
- [ ] If iterate: exactly one change, same timebox.
- [ ] If graduate: the bootstrap lane is next; the spike code is not promoted.

## Blocked

- [ ] If the demo cannot run, record why and what would unblock it. A blocked
      spike is still a result.
