---
title: "Chromebook GCP Environment — Master Handoff (gws-cli-local-505120)"
kb_type: wiki
topic: infrastructure
environment: ChromeOS Crostini (Debian container / penguin)
gcp_project: gws-cli-local-505120
account: simian420@gmail.com
captured: 2026-08-10
revised: 2026-08-11
status: active-secondary-environment
companion-docs: [CHROMEBOOK-INSTALL-SNAPSHOT-2026-08-10.md, "AI-Agent Development Stack on ChromeOS Crostini (research report)"]
tags: [chromebook, crostini, gcp, firestore, web2md, gws-cli, antigravity, gemini, simian420]
---

# Chromebook GCP Environment — Master Handoff

Secondary development environment, separate from the Kali workstation. ChromeOS Linux container (Crostini, Debian-based / `penguin`), bash-driven, operated via step-by-step terminal commands and raw JSON/REST payloads.

**Document roles:** this file = identity, security, guidelines, pending work. Install inventory lives in **CHROMEBOOK-INSTALL-SNAPSHOT-2026-08-10.md**. Tool deep-dives live in the **AI-Agent Development Stack research report**.

## Identity & project

- **GCP project:** `gws-cli-local-505120`
- **Account:** `simian420@gmail.com` (also a GEM-01 ingest account)
- **Auth:** user OAuth in file-backed keyring (gws CLI); Application Default Credentials planned for code execution identity

## Verified active infrastructure

**GCP APIs enabled:** cloudfunctions, run, cloudscheduler, secretmanager, documentai, admin.

**gws CLI (Google Workspace):** authenticated, granular scopes for Drive, Calendar, Sheets, Docs, Tasks, Keep, Forms, Gmail read/compose. **Security lock: `gmail.send` deliberately excluded** — no automated email sending.

**Live verified artifacts:**

| Artifact | ID / evidence |
| --- | --- |
| Google Doc "Agent Ideas Scratchpad" | `19BKQ8lHv8HU99rYdLXH1VS4oDFEXyzu9vsuy7RvK4VY` |
| Google Sheet "Agent Database Test" | `1HYaxKOKL5zBylG_AfWTai3GcVCubP_4D5ThhuoXbtDo` — row appends verified |
| Google Tasks | test insertion verified (`SU1GUkhhcWVyNUlzcF9GVQ`) |
| Secret Manager | `test-agent-key` provisioned |
| Document AI | endpoint routing verified via direct REST call |

## web2md-toolkit (primary project on this box)

Agent utility: ingest web content → structured Markdown → Gemini analysis → stateful memory in Firestore.

- **Pipeline:** `web2md_agent.py` in `~/projects/` — loads `google.cloud.firestore` + `google.genai` clients, infers with `gemini-3.6-flash`, persists to `web2md_artifacts` Firestore collection.
- **Scripts:** see install snapshot §3 for the full script inventory.
- **Config:** `firebase.json`, `firestore.rules`, `firestore.indexes.json`, `~/.config/gws-agent/env.sh` (loads `GEMINI_API_KEY`, GCP project vars).

## ⚠ Open security item

`firestore.rules` currently `read, write: if true` — wide open. Hardening required before anything production-adjacent. Standing task, not yet done.

## Development guidelines (standing, for AI executors on this box)

1. All Python inside `~/projects/venv`.
2. Assume `GEMINI_API_KEY` and `GCP_PROJECT` must be set per session.
3. Prefer explicit CLI linking (`firebase use --add`, `gcloud services enable`) over interactive wizards.
4. Every future implementation carries the firestore.rules hardening task.
5. New packages must be compatible with Python 3.13.5 / Node 22.

## Pending stack (not yet implemented)

- **Tooling:** ~~Android Studio (Quail)~~ ✅ installed 2026-08-10 (Quail 3, first-run wizard pending — see install snapshot), Antigravity + CLI expansion, AI Studio SDK bindings, Builders Hub/Firebase integration, Web2MD Markdown processor integration
- **Identity:** ADC login, headless service account, Domain-Wide Delegation
- **Agent core:** Vertex AI / Generative Language APIs, Firestore + BigQuery state memory, Document AI processor instance, Pub/Sub Eventarc triggers
- **Resiliency:** Terraform IaC, FinOps billing kill-switch Cloud Function, Pub/Sub DLQs with exponential backoff for Sheets 429s, kernel tuning `fs.inotify.max_user_watches=524288`
- **Task list:** robust web→md fetcher (BeautifulSoup/trafilatura), programmatic budget alerts, input sanitization layer expansion, Terraform migration

## Cross-references

- GEM-01 — simian420 is an ingest account in the PAIR pipeline
- Web2md concept overlaps MEMORY-ALPHA-01 raw-capture workflow — potential convergence or dedup decision needed
- Google Developer Program enrollment offers noted in source (Cloud/Firebase + AI Studio data-read consents) — no action recorded
