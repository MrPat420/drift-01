# User Profile & Unfinished Ideas Document

## 1. Communication Fingerprint

Direct patterns observed in your own phrasing across this thread:

- **"I guess" as a soft hedge before a real decision:** *"I guess we could just build the basic scaffolding,"* *"I could go ahead and run the house cleaning over there and then come back to this."*
- **"I think" prefacing self-assessment or a proposal:** *"I think I'm way ahead of the curve,"* *"I think I may have something already."*
- **Check-in tags at the end of an explanation, seeking confirmation of understanding:** *"does this make sense,"* *"you know what I'm saying,"* *"Do you understand what I'm getting at."*
- **Context-before-ask structure:** longer messages consistently lead with backstory/reasoning before landing on the actual request (e.g., the entire message explaining financial pressure and the 6-month remote-work goal before any explicit ask).
- **Self-assessed skill framing, stated plainly rather than implied:** *"my housekeeping and organizational skills are subpar,"* *"I'm really, really new to Linux to AI in general."*
- **"Yeah" as a message-opener,** frequently prefacing agreement, a pivot, or a new instruction.
- **Circling/looping language for returning to deferred topics:** *"let's circle that around,"* *"loop back around to the very beginning of this rabbit hole."*
- **Voice-to-text artifacts requiring contextual correction:** "jama 1" (GEM-01), "Jason" (JSON), "genetic AI" (agentic AI), "gat throttled" (got throttled) — run-on sentences with minimal punctuation, consistent with dictation rather than typing.

## 2. Implicit Preferences & Constraints

- **Accuracy over speed, stated explicitly, then acted on consistently:** *"I don't care how slow it is I would rather have accuracy instead of speed... it would be more harmful if we miss something than if we just saved one minute."* This wasn't just said once — it shaped the housekeeping prompt's design (strict one-at-a-time, later revised only after independent panel evidence, not on request).
- **Persuadable by evidence, not by assertion.** You reversed your own one-at-a-time preference specifically after cross-model research showed rubber-stamp risk — you didn't take my word for it initially, but did adjust once shown converging independent findings.
- **Wants the reasoning, not just the output:** *"I want you to do it so we can work through it and you can explain things to me so I learn more along the way — if I just have you make all the decisions and Claude codes it, it's not beneficial at the end of the day."*
- **Live verification over trusted claims, adopted as a running habit.** By the second half of the session you were independently requesting `grep`/`find` checks before accepting a claim as true, without being prompted to — this became self-directed, not just modeled.
- **Real discomfort with unearned confidence or too-tidy answers.** The multiple "pushback" exchanges (rejecting a fabricated-sounding message, pressing on whether "Overwatch" was real) show a consistent instinct to distrust anything that resolves too neatly without a checkable source.
- **Cost-consciousness, tied to a stated real constraint:** disabled-veteran fixed income (~$4,000/month), explicitly named — this surfaced directly in wanting real dollar costs for API tiers, not estimates.
- **Preference for durable, reusable artifacts over one-off answers.** Repeated requests to save things as files/templates (housekeeping prompt, routing protocol, session tracker) rather than leaving decisions in chat scrollback.
- **Explicit boundary once stated, never repeated:** the request that Claude not ask permission before proceeding through a list ("*you don't need to ask me what I want to do first*") — an implicit trust-delegation preference for routine/sequential work specifically.

## 3. Raw Unfinished Thoughts Log

Concepts, features, or tasks mentioned and not carried to completion:

1. `ideate.md` — content-gap/idea-generation prompt, referenced from the original source video, never built.
2. Automation layer — scheduled daily `translate.md` run, still fully manual.
3. Voice memo pipeline (Whisper → `/raw`) — never started.
4. File-watcher daemon (`watchdog`-based auto-trigger) — never started.
5. Broader input types (PDF, web articles) into MEMORY-ALPHA-01 — never tested.
6. Stale project datasheet — flagged multiple times as needing an update, never updated.
7. `sqlite-vec` addition for future semantic search — recommended, not installed.
8. PostgreSQL install as a freelance-skill investment — discussed at length, never actually run.
9. GEM-01's 10,096-item pending classification backlog — surfaced as a major finding, never worked through.
10. K-threshold calibration for cascade-tagging, scoped to the 173-entry long-tail subset — identified as the next real step, query never run.
11. The 45,741-word outlier entry in GEM-01's corpus — flagged as unidentified/unchecked against the manual-review list.
12. Cascade-tagging "Tier" rename (from "Layer," to avoid collision with architecture scheme) — recommended, never confirmed implemented in real code.
13. `ARCHITECTURE_LAYER_NAMING_SCHEME.md` upload into GEM-01's own knowledge base — identified as the literal missing piece, never confirmed done.
14. TOOLING-01's disambiguation note (LangGraph/Langfuse mix-up) — identified precisely, correction never applied.
15. `agentic_ai_infra` registry entry — confirmed missing, never created.
16. `verify_ingest` integration into `velocity_scraper.py`/`extractor.py` — explicitly deferred as "not yet done, the actual next step."
17. Mid-stage-resume gap in `seen_video_ids` logic — named as a real, narrow gap, never fixed.
18. The 6-month remote/freelance work transition — stated as a goal with real urgency, no concrete plan or first step built.
19. Productized offer / case-study idea for monetizing MEMORY-ALPHA-01 — suggested once, never developed further.
20. Y-TIP-COMMERCIAL container verification — actively unresolved at the point this analysis was requested (`docker ps -a` check pending).
21. Windows VM project (separate thread): audio routing final confirmation, CPU pinning, Windows activation status, second isolated Minecraft VM decision, and a founding document for that project — all left open.
22. `.desktop` file conversion for the VM launchers — offered, never actioned.
23. `gh` CLI installation on Kali — flagged as a nice-to-have, never installed.
