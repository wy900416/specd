# Interview protocol

Detailed companion to `SKILL.md`. Read this when the first pass stalls, when the
user asks for a deeper interview, or when you need a question that fits the kind.

## Opening

Ask one question:

> What are we specifying, and what decision should this spec let someone make?

Then choose the kind and target. Do not start with a template dump.

## Question patterns

Use these instead of "tell me more":

- **Evidence, not adjectives** — "What does *fast* mean here? What number would
  count as a failure?"
- **Failure first** — "What is the most likely way this fails in production, and
  what should the caller see?"
- **Counterfactual** — "If we deleted this requirement, what would break? If
  nothing breaks, is it a requirement or a preference?"
- **Boundary** — "Who owns this data? Who may write it? Who may read it?"
- **Rejected alternatives** — "What did you consider and reject, and why?"
- **Observability** — "How would an operator know this happened, without reading
  the code?"
- **Compatibility** — "What change to this contract would break a consumer?"
- **Ownership** — "Which team is accountable when this is wrong?"

## Per kind

### system

- Who is the system for, and what is outside it?
- Which domains does it contain? Which domain owns each capability?
- What are the top three system-level requirements?
- Which NFRs and standards apply to the whole system?
- What decision would this system spec unlock for a new team?

### domain

- What business capability does this context own?
- Which terms are ambiguous across teams? Define them.
- What invariants must always hold?
- Which services implement it? Which service is the source of truth?
- What is explicitly outside this context?

### service

- What does this service own, and what does it explicitly not own?
- Which domain does it implement?
- Which contracts does it expose or consume?
- What happens when each dependency is unavailable?
- Where is the idempotency boundary?
- What data does it own, and who may write it?
- Which standards and NFRs constrain it?

### contract

- Who exposes it, and who consumes it?
- What is the compatibility policy for adding, changing, and removing fields?
- What is the error envelope, and which errors are retryable?
- Is there an idempotency key? What is its scope and lifetime?
- What happens to in-flight requests during a deploy?

### flow

- What triggers the flow: request, event, schedule, or human action?
- Which services participate, and which one owns the outcome?
- What is the happy path, step by step, with observable results?
- What is the compensation for each failure?
- What is the trace span and the alert condition?

### nfr

- Which kinds and tags does it apply to?
- How is it measured: metric, log, trace, audit, or review?
- What is the threshold and the window?
- What is degraded first when the budget is exhausted?
- Who is paged, and what is the escalation path?

### adr

- What forces make a decision necessary now?
- What alternatives were rejected, and why?
- What are the negative consequences, and who accepts them?
- What would cause this decision to be revisited?

### standard

- Which services and contracts must comply?
- Is it pinned, or only linked when relevant?
- How is compliance checked, and where is the check recorded?
- Who can grant an exception, and for how long?

## Handling unknowns

Never fill a gap with a plausible guess. Write it down:

```md
## Open Questions

- [ ] <question> — owner: <team> — needed before: approval
```

Then move on. A draft with honest open questions is more useful than a fluent
draft with invented answers.

## Stopping conditions

A draft is ready for review when:

- every required front-matter field is present;
- every normative requirement has Given / When / Then;
- every service links a domain, a contract, and its constraints;
- open questions have an owner and a "needed before" marker;
- `checklists/validate.md` is applied and every finding has a file, line, and
  one-line explanation;
- the user can state the decision this spec enables.

## Sample exchange

> **Agent:** What are we specifying, and what decision should this spec let someone make?
>
> **User:** Checkout. It should let us decide whether to build one service or two.
>
> **Agent:** Then the first useful spec is the flow, not the service. What starts
> checkout: a user request, an event, or a schedule?
>
> **User:** A user request.
>
> **Agent:** Which services participate today, even if one of them is only planned?
>
> **User:** Orders and payments.
>
> **Agent:** What should the customer see when payment authorization times out?

At each step, write the answer into the draft and show only the changed lines plus
the next question. Do not paste the whole file back.
