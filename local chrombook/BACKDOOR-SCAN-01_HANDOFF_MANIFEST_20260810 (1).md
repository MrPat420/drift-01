# BACKDOOR-SCAN-01 — Project Handoff Manifest
**Compiled:** 2026-08-10, for cross-AI bridging (target: Gemini, extrapolation/refinement pass)
**Compiled by:** Claude, from BACKDOOR-SCAN-01's own Project knowledge base only
**Scope limitation (read first):** This document is authoritative about BACKDOOR-SCAN-01 only. It draws exclusively from files stored in this Project's knowledge base. It cannot see other Claude Projects, the operator's actual disk state on the Lima Node, or any session outside this Project. Claims below are tagged `[VERIFIED — in KB]` (stated directly in a KB file), `[INFERRED]` (reasoned from KB content but not directly stated), or `[UNRESOLVED]` (a known open contradiction or gap). Do not treat `[INFERRED]` as fact without operator confirmation.

**Correction to framing, stated once:** This is not an "AI computer virus" project. It is a **defensive detection pipeline** built to catch backdoors, vulnerabilities, and malicious code that AI coding assistants (Claude Code, etc.) might introduce — deliberately or accidentally — into the operator's own AI-generated codebase. Nothing in this project's scope involves generating malicious code or offensive tooling.

---

## 1. CORE VISION & SYSTEM OBJECTIVES

**Purpose** `[VERIFIED — in KB]`: The operator is a solo, non-coder technical director who relies entirely on AI coding assistants for implementation across a multi-project software portfolio, and therefore cannot independently read or audit AI-generated code. BACKDOOR-SCAN-01 exists to build an automated substitute for the missing human code-review capability — one that does not depend on trusting any single AI model's judgment, since the same class of tool (AI) is both the risk and the proposed mitigation.

**Foundational assumption** `[VERIFIED — in KB]`: A 6-model cross-jurisdiction panel (spanning US, Chinese, and Japanese AI vendors, deliberately, so no single jurisdiction's models are sole arbiter) converged unanimously on 5 design constraints before any code was written:
1. Per-file scanning is structurally blind to cross-file attacks.
2. LLMs are unreliable for factual lookups (CVEs, package existence, typosquats) — hallucination risk. Use deterministic tools for those.
3. "2+ models agree" is not statistical validation on its own — models share training-data blind spots.
4. Scanned code must be treated as untrusted data, never as instructions (prompt-injection resistance).
5. Sending code to third-party LLM APIs risks leaking the secrets the scan is trying to protect.

**Scope** `[VERIFIED — in KB]`: Applies across the operator's full AI-assisted software portfolio (named projects include HOUSEKEEP-DISPO-01, HOUSEKEEP-FORK-01, AGIMUS-01, RAG-SpinUp/KBSYNC-01, INSTSET-BUILDER, and others `[INFERRED — portfolio list from Claude's own memory of prior sessions, not from this Project's KB directly]`). Only **one** project has actually been scanned to date: **y-tip-pipeline** (FastAPI + Celery + PostgreSQL/psycopg2).

**Goal ordering** `[VERIFIED — in KB]`: Validate core detection methodology first; defer automation/unattended-operation design until Layer 2 exists and confirmed findings are fixed.

---

## 2. ARCHITECTURAL BLUEPRINT & CURRENT PROGRESS

### Layer 1 — Deterministic tooling
**Status:** BUILT, TESTED `[VERIFIED — in KB]`
- Tools: gitleaks, bandit, semgrep, pip-audit, cargo-audit (shellcheck also named in earlier handoff draft `[VERIFIED — in KB, backdoor_scan_project_handoff-1.md]` but not listed in the later registry entry — minor drift, not flagged as resolved either way).
- Script: `~/layer1_scan.sh`.
- Run against y-tip-pipeline (~7,700 files): found 5 duplicated real secrets in cache files (hygiene issue, not a backdoor) and one Dockerfile hardening gap (missing `USER` directive — fixed and confirmed).
- 279 raw findings collapsed to 3 real ones after excluding a stale vendored virtualenv scanned by mistake. Of those 3: 2 manually confirmed false positives, 1 real and fixed.
- Not yet run against any other project in the portfolio, and specifically not against a Rust-heavy project (cargo-audit untested in practice) or a legacy project.

### Layer 2 — Capability manifest diff + secret-to-sink taint trace
**Status:** DESIGNED ONLY, not built as working code `[VERIFIED — in KB]`
- Design consolidated from panel rounds: a per-project capability manifest declaring allowed network/filesystem/subprocess/env-var/dynamic-execution capabilities, diffed against actual code capabilities, plus secret-to-sink taint tracing. A FastAPI/Celery/psycopg2-specific sink checklist exists as supporting reference material, not the end goal.
- Capability manifest for y-tip-pipeline has been partially filled in (network, filesystem, subprocess, env-var, CI/CD sections), with explicit "not yet scanned" placeholders where coverage doesn't actually exist yet — an intentional honesty discipline per project rule #2.
- **Known unresolved wording gap** `[UNRESOLVED]`: the manifest's `dynamic_code_execution` field doesn't clearly distinguish in-process `eval`/`exec` from async task-queue dispatch (e.g. Celery's `.delay()`). DeepSeek, alone among the panel, read Celery dispatch as violating the field as currently worded — not wrong, just an interpretive gap that needs the template tightened before Layer 2 goes to production.

### Layer 3 — Multi-pass adversarial LLM review
**Status:** BUILT, TESTED, VALIDATED `[VERIFIED — in KB]`
- Script: `~/layer3_dry_test_panel.py` (hardened final version).
- Structure: 3-pass adversarial sequence — Pass A (assume malicious, find evidence), Pass B (skeptical benign-explanation review), Pass C (adjudication: classify each finding VERIFIED / LIKELY / SPECULATIVE, without letting Pass B auto-suppress Pass A's findings).
- INTENT DELTA question redesigned mid-project from binary yes/no (produced 3-way model disagreement on identical input) to graduated BENIGN DELTA / FLAGGED DELTA classification — resolved the disagreement.
- Reliability hardening applied (all confirmed working): retry-once-on-empty-content; `max_tokens` raised from 2000 to 6000; guard preventing a failed/incoherent Pass A from being fed into Pass B/C (this had previously caused a model to hallucinate nonexistent "prior agents"); coherence-check function (`is_coherent()`) to catch garbled-but-technically-non-empty output; incremental per-model disk writes so a crash mid-run doesn't erase completed results.

### Model panel (for Layer 3 specifically)
**Roster** `[VERIFIED — in KB]`: Claude (anthropic/claude-opus-4.1), GPT (openai/gpt-5.5), Qwen (qwen/qwen3-coder-plus), Sakana (sakana/fugu-ultra) — all via OpenRouter; DeepSeek (deepseek-chat, direct API — `DEEPSEEK_API_KEY`, not OpenRouter). **GLM (z-ai/glm-5.2) dropped** after 3/3 empty-content failures across 3 separate runs, despite retries and a 6000-token ceiling — documented as a real model-reliability finding, not a config issue.
- Effective panel size: **5 models** (started at 6, GLM dropped).

### `[UNRESOLVED — flagged, not resolved]` Panel composition mismatch
BACKDOOR-SCAN-01's own KB documents a 5-model Layer 3 panel (above). A separate document also present in this Project's KB, `OPERATOR_MASTER_BRIEF_20260710.md`, describes a different **4-model research panel** (Gemini 3.1 Pro, DeepSeek, GLM-5.2, GPT-OSS-120B) used for general operator research/grounding tasks — not specific to Layer 3 code review. These are two different panels for two different purposes, not a direct contradiction, but the Master Brief is **not native to this Project** (it's a portfolio-wide operator document that appears to have propagated into this KB) and should not be read as describing BACKDOOR-SCAN-01's own model roster. This mismatch has been noted internally as "VERIFIED on census" but is still functionally unresolved — worth stating plainly to Gemini rather than letting it read as one panel.

---

## 3. APPLIED FINDINGS — y-tip-pipeline (`api.py`)

Cross-validated across 2 full Layer 3 panel runs, 5 clean models. `[VERIFIED — in KB, ytip_layer3_findings_consolidated.md]`

**Resolved / closed (false positive):**
- SQL injection via `ORDER BY {order_col}` in `get_trending()` — confirmed false positive by 6+ independent model responses; `order_col` only ever takes a hardcoded, whitelisted value. Closed, no action needed.

**Confirmed — fix these (not yet applied to code):**
1. **Unbounded pagination** — `get_trending()` has no upper bound on `limit`/`offset`; `get_scripts()` and `get_calendar()` have no pagination at all. Strongest-consensus finding of the test.
2. **Unvalidated `video_id` before Celery dispatch** — `trigger_generate()` passes URL-path `video_id` straight into `.delay()` with no format check. Recommend `^[A-Za-z0-9_-]{11}$` validation.
3. **No rate limiting on `/api/login`** — no throttling/lockout/audit logging; also uses `!=` instead of `hmac.compare_digest` for password comparison (minor timing side-channel).
4. **Raw error/task-result disclosure** — `get_task_status()` and other endpoints return raw exception text to the client instead of sanitized messages.

**Needs manual verification before action:**
5. Possible missing transaction rollback in `update_calendar_status()` — raised by DeepSeek only, not yet cross-confirmed.
6. `/api/scripts` and `/api/scripts/{video_id}` scope question — raised independently by GPT and Sakana; these expose `topic_corpus.extraction_json` wholesale, outside the originally-specified endpoint surface. Not necessarily a problem — needs a factual check (does the frontend actually call these, does the field contain anything sensitive in practice).

**Process finding:**
7. Manifest `dynamic_code_execution` wording ambiguity (see Layer 2 section above).

---

## 4. OPEN ITEMS / ROADMAP (confirmed go-forward order)

`[VERIFIED — in KB, OPEN_ITEMS_TRACKER.md]` — deferred to next Kali (Lima Node) session:
1. Apply the 4 confirmed code fixes above to `y-tip-pipeline/api.py`.
2. Manually verify the 2 unconfirmed findings.
3. Build Layer 2 as actual working code (capability manifest diff + taint trace).
4. Cross-stack test — run Layer 1 against a second, differently-stacked project (Rust-heavy, to exercise `cargo-audit`; and/or a legacy project).
5. Fix the capability manifest's `dynamic_code_execution` wording ambiguity.
6. Analyze ESAA-Security (arXiv:2603.06365, github.com/elzobrito/ESAA-Security) — an event-sourced, replay-verifiable audit architecture flagged as a relevant formalization of this project's evidence-tiering discipline. Not yet analyzed; 5-step method already outlined (structural comparison table → per-overlap check → per-divergence relevance check → cross-check against this project's own panel → adopt-now/adopt-later/reject decision table).
7. Automation/unattended-operation design — deprioritized pending Layer 2. Open questions: what triggers a re-scan (CC session end / git hook / cron); how do UNKNOWN/needs-review findings surface to a non-coder operator without daily manual review; biggest automation failure mode to guard against.

**Also unresolved, not in the numbered build order:**
- Master registry entry for BACKDOOR-SCAN-01 not yet appended to the portfolio-wide registry.
- Instruction-set (`BACKDOOR-SCAN-01_RULES.md`) not finalized — two content gaps remain (a secrets-handling rule, and formal resolution text for the panel-composition mismatch above).
- SEV-CRIT file provenance: two `SEV-CRIT_*` documents landed in this Project's KB via portfolio-wide propagation from HOUSEKEEP-DISPO-01; whether their placement here was intentional is unconfirmed. `[UNRESOLVED]` — not treated as BACKDOOR-SCAN-01 content in this manifest.

**Explicitly deferred, not currently blocking anything:**
- Runtime sandbox with canary secrets (proposed Layer 4 candidate).
- Differential provenance anomaly detection — needs generation-time logging infrastructure that doesn't exist yet.
- Evaluation corpus (seeded benign/malicious test set) — build once Layer 2/3 are both working.

---

## 5. TAXONOMY / TERMINOLOGY / LOGIC FLOWS FOR GEMINI TO INGEST

**Layer terminology:**
- **Layer 1** = deterministic, non-LLM tooling. Cheapest, most reliable, catches obvious known-pattern issues.
- **Layer 2** = structural/capability analysis (manifest diff, taint tracing). Catches composition-based attacks Layer 1 is structurally blind to.
- **Layer 3** = narrow-scope adversarial LLM semantic review, evidence-scored not vote-counted.
- **Layer 4** (not started) = proposed runtime sandbox with canary secrets.

**Layer 3 pass structure:** Pass A (malicious-hypothesis) → Pass B (benign-skeptic) → Pass C (adjudication: VERIFIED / LIKELY / SPECULATIVE).

**INTENT DELTA classification:** BENIGN DELTA vs FLAGGED DELTA (replaced an earlier binary yes/no framing that caused model disagreement).

**Evidence-tiering discipline (project-wide rule):**
- A finding needs 3+ independent models/runs agreeing to be treated as solid.
- No finding is "resolved" without literal command + output — a verbal claim of "fixed/confirmed/verified" is not evidence.
- A "clean" scan result must state explicitly what was and wasn't checked — never silently default to "clean" by omission.

**Capability manifest fields (y-tip-pipeline instance):** network, filesystem, subprocess, env-var, dynamic-code-execution, CI/CD — with explicit not-yet-scanned placeholders where coverage is incomplete, by design.

**Model reliability notes carried forward for panel design:**
- Claude: least run-to-run consistent single model in this project's own testing — wobbled between LIKELY/SPECULATIVE/FALSE POSITIVE on identical input across runs; one run produced garbled output caught by the coherence guard.
- Sakana: most calibrated; best BENIGN/FLAGGED DELTA implementation.
- GPT: strongest single clean run; surfaced the `/api/scripts` scope question independently.
- DeepSeek: most thorough VERIFIED-tagged output; surfaced 2 genuinely new findings (transaction rollback, manifest ambiguity) no other model caught.
- GLM: dropped from panel (3/3 empty-content failures, 3 separate runs).

**Pipeline integrity rules to preserve in any Gemini-side extension:**
- A failed/incoherent model response must never be fed into the next pass (prevents hallucination-on-broken-input, observed once in testing).
- Results saved incrementally per model, not only at run's end.
- `max_tokens` minimum 4000 on every panel query (lower limits caused silent empty-content failures previously).

---

## 6. WHAT THIS DOCUMENT DELIBERATELY EXCLUDES

- Full text of the two `SEV-CRIT_*` documents present in this Project's KB — they originate from HOUSEKEEP-DISPO-01, not BACKDOOR-SCAN-01, and their relevance here is unconfirmed. If Gemini needs them, they should be sourced from HOUSEKEEP-DISPO-01 directly, not relayed secondhand through this manifest.
- Full text of `OPERATOR_MASTER_BRIEF_20260710.md` — portfolio-wide operator infrastructure document, not BACKDOOR-SCAN-01-specific; only the panel-composition conflict relevant to this project is excerpted above.
- Any claim about other portfolio projects' internal state — out of this Project's authority per standing cross-project boundary rule.

---

## Artifact status

| Artifact | Path | Status | Confirmed by operator? |
|---|---|---|---|
| This handoff manifest | `/mnt/user-data/outputs/BACKDOOR-SCAN-01_HANDOFF_MANIFEST_20260810.md` | `[FILE CREATED — LOCATION UNCONFIRMED]` | No |

Not yet in this Project's knowledge base or on the Lima Node. If you want this to persist beyond this chat, it needs manual upload/transfer — I can't push it there directly.
