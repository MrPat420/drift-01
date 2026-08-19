# Project Housekeeping Protocol — v4.8

Authored by INSTSET-BUILDER (per confirmed routing — this version is not
drafted ad hoc elsewhere). Supersedes v4.7.1. Built from direct operating
experience running v4.7.1 twice in one session, not from re-reading v4.7.1's
own text. Five targeted changes below; everything else in v4.7.1 (Phase -1
Environment Declaration, the persistence gate, the Artifact Tracking Gate,
never-invent, auto-verify) carries forward unchanged.

## CHANGE 1 — Delta-gated recovery passes (replaces blanket Phase 1b/1c/1d)

Light-diff mode may be declared ONLY if all three conditions hold, checked
explicitly and shown in the response:

1. Time check: the prior Phase 4 close occurred in this same continuous
   chat session (not a new session) -- verified by the close being visible
   earlier in this same conversation's own context, not retrieved via search.
2. Session-count check: a recent_chats call (or equivalent) run at the start
   of this Phase 0 shows the total session count for this Project is
   unchanged from what was stated in the prior close's own Phase 1c report --
   meaning no new session has been created in the interim where undetected
   work could have happened.
3. No-consecutive-light-diff check: the immediately prior run was a
   FULL-diff run. Light-diff mode can never be used twice in a row,
   regardless of how short the gap is -- this prevents drift where a chain
   of short gaps quietly never gets a full recovery pass.

If any one of the three fails, or can't be checked (e.g., recent_chats
isn't called), default to full-diff mode -- no exceptions, no "probably
fine."

The response must show the three checks explicitly, e.g.:

Light-diff eligibility check:
1. Same continuous session as prior close? YES
2. Session count unchanged (recent_chats: N sessions, matches prior report's N)? YES
3. Prior run was full-diff? YES
-> Light-diff mode eligible.

This replaces any softer "stated reason" standard entirely -- a reason is
not sufficient, only a passed checklist is.

## CHANGE 2 — First-class false-claim category

A new finding type, distinct from stale scripts, pending decisions, or
security exposures: [FALSE-COMPLETION] -- any instance where the assistant
itself claimed something was done, logged, created, or confirmed without
contemporaneous evidence, later found to be inaccurate.

Required format when this occurs, every time, no exceptions:
- What was claimed, verbatim or close to it
- What evidence (if any) existed at the time of the claim -- usually none
- How it was actually discovered (operator catch, self-catch, follow-up
  verification)
- The corrected status, with real evidence this time

This gets its own row/section in the Phase 4 report, not folded into
general findings -- it's a report on the audit's own reliability, not on
the project being audited.

## CHANGE 3 — Explicit duplicate-effort check (Phase 1, new first step)

Before building the rest of the Phase 1 findings list, ask one standing
question: has any of this already been resolved elsewhere -- a different
Project, an earlier ad hoc session -- and simply not synced back here?
This isn't a deep investigation on every item; it's one pass, using
whatever search is available, specifically looking for signs of parallel
or duplicate work before treating something as a fresh open item.
State plainly what was checked and what wasn't reachable.

## CHANGE 4 — Defined item ontology (replaces ad hoc BLOCKING/NON-BLOCKING-only tagging)

Every Phase 1 finding gets exactly one tag, from a fixed list:
- TRACKABLE-BLOCKING -- live-verifiable conflict or fix, must resolve
  before this run closes
- TRACKABLE-NON-BLOCKING -- real, actionable, but doesn't gate closure
- HELD-PENDING-REVIEW -- genuinely open, operator has explicitly
  deferred it, not a blocker, not to be nagged about until they raise it
- PARKED -- someone else's decision, or blocked on something outside
  this Project's reach, not actionable right now
- INFORMATIONAL-ONLY -- noted for context, was never actionable, doesn't
  count toward any total

The Phase 1 compiled summary states the count per category explicitly, not
just a single BLOCKING/NON-BLOCKING split.

## CHANGE 5 — Governance-model line (not a new phase)

Phase 1's scope note gets one additional sentence, only when a cross-project
governance model is known to exist: state it in one line (e.g., "this
Project operates within a Trigger -> Action -> Architecture tier ->
Escalation -> Human model; findings here are scoped to the Architecture
tier's own work"). Nothing else changes -- no new machinery, no new gate.

## CHANGE 6 — Verification as a mandatory separate step, not a tense choice

Any response that takes an action (writes a file, runs a command, resolves
an item) must state the action and its result as two separate, sequential
claims -- never collapsed into one completed-tense sentence. "I wrote X" is
banned. Required instead: "Action taken: [X]. Verification: [not yet run /
shown output / unconfirmed]."

This applies even when confident the action succeeded -- confidence is not
evidence. This rule exists specifically because three false-completion
instances occurred in one live session, all stemming from skipping this
separation, not from dishonesty: a heredoc described as saved with no
execution shown, a placeholder bracket-text description run as if it were
real file content, and an ambiguous terminal-wrap result nearly accepted at
face value before an unambiguous check settled it. In each case the failure
was grammatical before it was factual -- completed-tense language was used
before completion was actually confirmed.

---

Everything else -- Phase -1 through Phase 5, the persistence gate, the
Artifact Tracking Gate, the standing rules -- carries forward from v4.7.1
unchanged.

## CHANGELOG

v4.8 -- Authored by INSTSET-BUILDER, 2026-07-15, per confirmed routing
decision that this version's authorship belongs here rather than being
drafted ad hoc elsewhere. Six changes: delta-gated recovery passes
(replacing blanket Phase 1b/1c/1d execution regardless of diff size),
a first-class false-completion finding category, an explicit duplicate-
effort check as Phase 1's new first step, a defined five-value item
ontology replacing ad hoc BLOCKING/NON-BLOCKING-only tagging, a
one-line governance-model acknowledgment in Phase 1's scope note, and a
mandatory action/verification separation rule banning completed-tense
claims about unconfirmed actions. All six changes are traceable to specific friction points experienced
running v4.7.1 twice in one live session (2026-07-15), not theoretical
additions. Supersedes v4.7.1.
