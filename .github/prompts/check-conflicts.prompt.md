---
mode: 'agent'
description: 'Check a spec against every other spec and record conflicts for the user to resolve.'
---

Check this spec for conflicts:

${input:spec}

1. Read the target spec and its requirements.
2. Read every other `specs/**/*.md` (use summaries and headings first; read the
   full body only for plausible overlaps).
3. Look for contradictions in: data ownership, write authority, contract shape,
   state machines, NFR thresholds, naming of shared entities, and scope.
4. Write or update `## Conflicts` in the target spec:

   | # | Other spec | Conflict | Options | Resolution |

5. Put plausible conflicts in the table with `Resolution: open`. Do not pick a
   winner.
6. Add the other spec ids to `conflicts_with` in the front-matter.
7. Report the conflicts in one short list and ask the user to choose an option
   only for the blocking ones.

A conflict with `Resolution: open` blocks validation.
